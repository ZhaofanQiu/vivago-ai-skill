#!/usr/bin/env python3
"""
vivago_client.py 新的 upload_image 实现 (v2)
使用 Vivago 新提供的上传方式
"""

import cv2
import uuid
import requests
from typing import Optional, Tuple

def upload_image_v2(self, image_path: str, max_side: int = 1024, quality: int = 80) -> str:
    """
    上传图片到 Vivago 存储 (v2 - 新方式)
    
    新流程:
    1. GET /prod-api/user/google_key/hidreamai-image → 获取预签名 URL
    2. PUT 预签名 URL + 图片二进制数据 → 完成上传
    
    Args:
        image_path: 图片文件路径
        max_side: 图片最大边长，超过则缩放 (默认1024)
        quality: JPEG 压缩质量 (默认80)
        
    Returns:
        image_uuid: 上传后的图片 UUID (格式: j_xxxx)
        
    Raises:
        ImageUploadError: 上传失败
    """
    import os
    
    # 生成唯一的图片 UUID
    image_uuid = f"j_{uuid.uuid4()}"
    logger.info(f"Uploading image {image_path} -> {image_uuid} (v2)")
    
    # 步骤1: 读取并处理图片
    image = cv2.imread(image_path)
    if image is None:
        raise ImageUploadError(image_path, "Failed to read image file")
    
    # 缩放图片
    height, width = image.shape[:2]
    if height > width:
        scale = max_side / height
    else:
        scale = max_side / width
    
    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        logger.info(f"Resized image to {new_width}x{new_height}")
    
    # JPEG 压缩
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    _, encoded_image = cv2.imencode('.jpg', image, compression_params)
    image_data = encoded_image.tobytes()
    
    # 步骤2: 获取预签名上传 URL
    base_url = "https://vivago.ai"
    endpoint = "/prod-api/user/google_key/hidreamai-image"
    
    headers = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "filename": image_uuid,
        "content_type": "image/jpeg"
    }
    
    try:
        response = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get('code') != 0:
            raise ImageUploadError(
                image_path, 
                f"Failed to get upload URL: {result.get('message')}"
            )
        
        presigned_url = result.get('result')
        if not presigned_url:
            raise ImageUploadError(image_path, "No presigned URL in response")
        
        logger.info(f"Got presigned URL (length: {len(presigned_url)})")
        
    except requests.RequestException as e:
        raise ImageUploadError(image_path, f"Failed to get upload URL: {e}")
    
    # 步骤3: 使用预签名 URL 上传图片
    try:
        upload_response = requests.put(
            presigned_url,
            data=image_data,
            headers={"Content-Type": "image/jpeg"},
            timeout=60
        )
        upload_response.raise_for_status()
        
        logger.info(f"Image uploaded successfully: {image_uuid}")
        return image_uuid
        
    except requests.RequestException as e:
        raise ImageUploadError(image_path, f"Failed to upload image: {e}")


def preprocess_and_upload_v2(self, image_path: str, target_ratio: str = None) -> Tuple[str, str]:
    """
    预处理图片并上传 (v2 - 使用新上传方式)
    
    Args:
        image_path: 原始图片路径
        target_ratio: 指定的目标比例（如 '1:1', '16:9' 等）
        
    Returns:
        (image_uuid, actual_wh_ratio): 上传后的图片UUID和实际使用的宽高比
    """
    import cv2
    import numpy as np
    
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ImageUploadError(image_path, "Failed to read image file")
    
    height, width = image.shape[:2]
    actual_ratio = width / height
    
    # 确定目标比例
    if target_ratio and target_ratio in SUPPORTED_RATIOS:
        closest_ratio = target_ratio
    else:
        closest_ratio = find_closest_ratio(actual_ratio)
    
    target_ratio_val = parse_ratio(closest_ratio)
    
    # 裁剪或缩放图片以匹配目标比例
    current_ratio = width / height
    if abs(current_ratio - target_ratio_val) > 0.01:  # 允许1%误差
        if current_ratio > target_ratio_val:
            # 图片太宽，裁剪左右
            new_width = int(height * target_ratio_val)
            offset = (width - new_width) // 2
            image = image[:, offset:offset+new_width]
        else:
            # 图片太高，裁剪上下
            new_height = int(width / target_ratio_val)
            offset = (height - new_height) // 2
            image = image[offset:offset+new_height, :]
        
        logger.info(f"Cropped image to ratio {closest_ratio}: {image.shape[1]}x{image.shape[0]}")
    
    # 保存临时文件
    temp_path = f"/tmp/vivago_upload_{uuid.uuid4()}.jpg"
    cv2.imwrite(temp_path, image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    try:
        # 使用 v2 上传
        image_uuid = self.upload_image_v2(temp_path)
        return image_uuid, closest_ratio
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
