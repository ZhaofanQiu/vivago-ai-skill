#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vivago AI API Client - v0.2.0
支持层级架构：一级功能 -> 二级端口
"""

import json
import os
import time
import uuid
import logging
from typing import Optional, Dict, Any, List, Tuple
import requests
import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)


class VivagoClient:
    """
    Vivago AI API Client
    
    层级架构：
    - 一级功能：text_to_image, image_to_video, image_to_image 等
    - 二级端口：kling-image, v3Pro, img2img 等具体API端点
    """
    
    # Storage configuration
    STORAGE_ENDPOINT = "http://storage.googleapis.com"
    STORAGE_BUCKET = "hidreamai-image"
    
    def __init__(
        self, 
        token: str, 
        storage_ak: Optional[str] = None, 
        storage_sk: Optional[str] = None,
        ports_config_path: Optional[str] = None
    ):
        """
        Initialize Vivago client.
        
        Args:
            token: Vivago API Bearer token
            storage_ak: Storage access key for image upload (optional)
            storage_sk: Storage secret key for image upload (optional)
            ports_config_path: Path to api_ports.json (optional)
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-accept-language": "en",
        }
        
        # Load ports configuration
        self.ports_config = self._load_ports_config(ports_config_path)
        self.base_url = self.ports_config.get("base_url", "https://vivago.ai/api/gw")
        
        # Initialize S3 client if credentials provided
        self.s3_client = None
        if storage_ak and storage_sk:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.STORAGE_ENDPOINT,
                aws_access_key_id=storage_ak,
                aws_secret_access_key=storage_sk,
                config=Config(s3={'addressing_style': 'virtual'})
            )
    
    def _load_ports_config(self, config_path: Optional[str] = None) -> Dict:
        """Load API ports configuration"""
        if config_path is None:
            # Default to same directory as this file
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "api_ports.json"
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load ports config: {e}, using defaults")
            return self._default_ports_config()
    
    def _default_ports_config(self) -> Dict:
        """Default ports configuration"""
        return {
            "base_url": "https://vivago.ai/api/gw",
            "categories": {
                "text_to_image": {
                    "default_port": "kling-image",
                    "ports": {
                        "kling-image": {
                            "endpoint": "/v3/image/image_gen_kling/async",
                            "result_endpoint": "/v3/image/txt2img/async/results",
                            "version": "kling-image-o1"
                        }
                    }
                },
                "image_to_video": {
                    "default_port": "v3Pro",
                    "ports": {
                        "v3Pro": {
                            "endpoint": "/v3/video/video_diffusion_img2vid/async",
                            "result_endpoint": "/v3/video/video_diffusion/async/results",
                            "version": "v3Pro"
                        }
                    }
                }
            }
        }
    
    def _get_port_config(self, category: str, port: Optional[str] = None) -> Tuple[Dict, str]:
        """
        Get port configuration for a category.
        
        Args:
            category: 一级功能名称，如 "text_to_image"
            port: 二级端口名称，如 "kling-image" (None则使用默认)
            
        Returns:
            (port_config, port_name)
        """
        cat_config = self.ports_config.get("categories", {}).get(category)
        if not cat_config:
            raise ValueError(f"Unknown category: {category}")
        
        ports = cat_config.get("ports", {})
        
        if port is None:
            port = cat_config.get("default_port")
            if not port:
                raise ValueError(f"No default port for category: {category}")
        
        if port not in ports:
            available = ", ".join(ports.keys())
            raise ValueError(f"Unknown port '{port}' for {category}. Available: {available}")
        
        return ports[port], port
    
    def list_categories(self) -> Dict[str, str]:
        """List all available categories (一级功能)"""
        categories = {}
        for cat_id, config in self.ports_config.get("categories", {}).items():
            categories[cat_id] = {
                "name": config.get("name", cat_id),
                "name_en": config.get("name_en", cat_id),
                "status": config.get("status", "unknown"),
                "default_port": config.get("default_port"),
                "description": config.get("description", "")
            }
        return categories
    
    def list_ports(self, category: str) -> Dict[str, Any]:
        """List all available ports for a category (二级端口)"""
        cat_config = self.ports_config.get("categories", {}).get(category)
        if not cat_config:
            raise ValueError(f"Unknown category: {category}")
        
        ports = {}
        for port_id, config in cat_config.get("ports", {}).items():
            ports[port_id] = {
                "name": config.get("name", port_id),
                "display_name": config.get("display_name", port_id),
                "status": config.get("status", "unknown"),
                "tested": config.get("tested", False),
                "speed": config.get("speed", "unknown"),
                "quality": config.get("quality", "unknown"),
                "notes": config.get("notes", "")
            }
        return ports
    
    # ==================== File Upload ====================
    
    def upload_image(self, image_path: str) -> str:
        """Upload image to Vivago storage"""
        if not self.s3_client:
            raise ValueError("Storage credentials not provided. Cannot upload images.")
        
        import cv2
        
        image_uuid = f"j_{uuid.uuid4()}"
        logger.info(f"Uploading image {image_path} -> {image_uuid}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image: {image_path}")
        
        height, width = image.shape[:2]
        max_side = 1024
        
        if height > width:
            scale = max_side / height
        else:
            scale = max_side / width
        
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, 80]
        _, encoded_image = cv2.imencode('.jpg', image, compression_params)
        
        self.s3_client.put_object(
            Body=encoded_image.tobytes(),
            Bucket=self.STORAGE_BUCKET,
            Key=image_uuid,
            ContentType='image/jpeg'
        )
        
        return image_uuid
    
    # ==================== Core API Call ====================
    
    def call_api(
        self,
        endpoint: str,
        data: Dict[str, Any],
        result_endpoint: str,
        max_retries: int = 60,
        retry_delay: int = 3
    ) -> Optional[List[Dict]]:
        """
        Generic API call with async task submission and polling.
        
        Args:
            endpoint: API submission endpoint
            data: Request body
            result_endpoint: Result polling endpoint
            max_retries: Maximum polling attempts
            retry_delay: Delay between polls (seconds)
        """
        try:
            url = f"{self.base_url}{endpoint}"
            headers_post = {**self.headers, "Content-Type": "application/json"}
            
            response = requests.post(url, json=data, headers=headers_post)
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            
            if result.get("code") != 0:
                logger.error(f"API error: {result.get('message')}")
                return result
            
            task_id = result.get("result", {}).get("task_id")
            if not task_id:
                logger.error("No task_id in response")
                return None
            
            logger.info(f"Task submitted: {task_id}")
            
            return self._poll_results(task_id, result_endpoint, max_retries, retry_delay)
            
        except Exception as e:
            logger.error(f"API call error: {e}")
            return None
    
    def _poll_results(
        self,
        task_id: str,
        result_endpoint: str,
        max_retries: int = 60,
        retry_delay: int = 3
    ) -> Optional[List[Dict]]:
        """Poll for task completion"""
        url = f"{self.base_url}{result_endpoint}?task_id={task_id}"
        headers_get = {"Authorization": self.headers["Authorization"]}
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers_get)
                
                if response.status_code != 200:
                    logger.warning(f"Poll failed: {response.status_code}")
                    time.sleep(retry_delay)
                    continue
                
                result = response.json()
                
                if result.get("code") != 0:
                    logger.error(f"API error: {result.get('message')}")
                    return None
                
                sub_results = result.get("result", {}).get("sub_task_results", [])
                
                if sub_results and all(
                    r.get("task_status") in {1, 3, 4} for r in sub_results
                ):
                    status = sub_results[0].get("task_status")
                    if status == 1:
                        logger.info(f"Task completed: {task_id}")
                    elif status == 3:
                        logger.warning(f"Task failed: {task_id}")
                    elif status == 4:
                        logger.warning(f"Task rejected: {task_id}")
                    return sub_results
                
                logger.debug(f"Task {task_id} processing (attempt {attempt + 1})")
                time.sleep(retry_delay)
                
            except Exception as e:
                logger.warning(f"Poll error: {e}")
                time.sleep(retry_delay)
        
        logger.error(f"Task timeout: {task_id}")
        return None
    
    # ==================== Text to Image ====================
    
    def text_to_image(
        self,
        prompt: str,
        port: Optional[str] = None,
        negative_prompt: str = "",
        wh_ratio: str = "16:9",
        batch_size: int = 1,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        文生图 - 支持多端口选择
        
        Args:
            prompt: 提示词
            port: 二级端口 (None=使用默认)
            negative_prompt: 负面提示词
            wh_ratio: 宽高比
            batch_size: 生成数量 (1-4)
            **kwargs: 额外参数
        """
        port_config, port_name = self._get_port_config("text_to_image", port)
        
        # 根据端点推断 module 名称
        endpoint = port_config["endpoint"]
        if "image_gen_kling" in endpoint:
            module = "image_gen_kling"
        elif "image_gen_std" in endpoint:
            module = "image_gen_std"
        else:
            module = "txt2img"
        
        display_name = port_config.get("display_name", port_name)
        
        data = {
            "app": None,
            "image": None,
            "mask": None,
            "module": module,
            "negative_prompt": negative_prompt,
            "prompt": prompt,
            "params": {
                "batch_count": 1,
                "batch_size": batch_size,
                "guidance_scale": kwargs.get("guidance_scale", 7.5),
                "height": kwargs.get("height", 512),
                "image_guidance_scale": kwargs.get("image_guidance_scale", 1.5),
                "sample_steps": kwargs.get("sample_steps", 40),
                "sampler": kwargs.get("sampler", "Euler a"),
                "seed": kwargs.get("seed", -1),
                "strength": kwargs.get("strength", 0.8),
                "style": kwargs.get("style", "default"),
                "wh_ratio": wh_ratio,
                "width": kwargs.get("width", 512),
                "relevance": kwargs.get("relevance", []),
                "custom_params": {
                    "enhance": kwargs.get("enhance", "1k"),
                    "wh_ratio": wh_ratio
                }
            },
            "role": kwargs.get("role", "general"),
            "version": port_config.get("version", "kling-image-o1"),
            "images": [],
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "audios": [],
            "videos": [],
            "request_id": str(uuid.uuid4())
        }
        
        logger.info(f"Using port: {port_name} ({display_name})")
        
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"],
            max_retries=kwargs.get("max_retries", 30),
            retry_delay=kwargs.get("retry_delay", 2)
        )
    
    # ==================== Image to Video ====================
    
    def image_to_video(
        self,
        prompt: str,
        image_uuid: str,
        port: Optional[str] = None,
        wh_ratio: str = "16:9",
        duration: int = 5,
        mode: str = "Slow",
        fast_mode: bool = False,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        图生视频 - 支持多端口选择
        
        ⚠️ 注意：视频生成需要 2-3 分钟，请谨慎调用
        
        Args:
            prompt: 视频动作描述
            image_uuid: 参考图片UUID
            port: 二级端口 (v3Pro/v3L/kling-video, None=使用默认)
            wh_ratio: 宽高比
            duration: 视频时长 (5或10秒)
            mode: 生成模式 (Slow/Fast)
            fast_mode: 快速模式
            **kwargs: 额外参数
        """
        port_config, port_name = self._get_port_config("image_to_video", port)
        
        display_name = port_config.get("display_name", port_name)
        
        data = {
            "image": None,
            "module": "video_diffusion_img2vid",
            "params": {
                "batch_size": 1,
                "guidance_scale": kwargs.get("guidance_scale", 7),
                "sample_steps": kwargs.get("sample_steps", 80),
                "width": kwargs.get("width", 1920),
                "height": kwargs.get("height", 1080),
                "fast_mode": fast_mode,
                "frame_num": kwargs.get("frame_num", 16),
                "seed": kwargs.get("seed", -1),
                "motion_strength": kwargs.get("motion_strength", 9),
                "max_width": kwargs.get("max_width", 1024),
                "wh_ratio": "keep",
                "cm_x": kwargs.get("cm_x", 0),
                "cm_y": kwargs.get("cm_y", 0),
                "cm_d": kwargs.get("cm_d", 0),
                "custom_params": {
                    "wh_ratio": wh_ratio
                },
                "mode": mode,
                "duration": duration,
                "x": kwargs.get("x", 0),
                "y": kwargs.get("y", 0),
                "z": kwargs.get("z", 0),
                "style": kwargs.get("style", "default")
            },
            "prompt": prompt,
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "role": kwargs.get("role", "general"),
            "style": kwargs.get("style", "default"),
            "wh_ratio": wh_ratio,
            "version": port_config.get("version", "v3Pro"),
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "images": [image_uuid],
            "videos": [],
            "audios": [],
            "request_id": str(uuid.uuid4())
        }
        
        logger.info(f"Using port: {port_name} ({display_name}) ⚠️ 2-3 minutes")
        
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"],
            max_retries=kwargs.get("max_retries", 60),  # 视频需要更多重试
            retry_delay=kwargs.get("retry_delay", 3)     # 视频间隔更长
        )


def create_client(
    token: Optional[str] = None,
    storage_ak: Optional[str] = None,
    storage_sk: Optional[str] = None,
    ports_config_path: Optional[str] = None
) -> VivagoClient:
    """
    Create Vivago client from environment or parameters.
    
    Environment variables:
        HIDREAM_TOKEN: API token
        STORAGE_AK: Storage access key
        STORAGE_SK: Storage secret key
    """
    token = token or os.environ.get("HIDREAM_TOKEN")
    storage_ak = storage_ak or os.environ.get("STORAGE_AK")
    storage_sk = storage_sk or os.environ.get("STORAGE_SK")
    
    if not token:
        raise ValueError("Token required. Set HIDREAM_TOKEN env var or pass token parameter.")
    
    return VivagoClient(token, storage_ak, storage_sk, ports_config_path)


if __name__ == "__main__":
    # 示例：查看可用端口
    logging.basicConfig(level=logging.INFO)
    
    client = create_client()
    
    print("\n=== 可用一级功能 ===")
    for cat_id, info in client.list_categories().items():
        print(f"{cat_id}: {info['name']} ({info['name_en']}) - {info['status']}")
    
    print("\n=== 文生图可用端口 ===")
    for port_id, info in client.list_ports("text_to_image").items():
        print(f"  {port_id}: {info['name']} - {'✅' if info['tested'] else '⏳'}")
    
    print("\n=== 图生视频可用端口 ===")
    for port_id, info in client.list_ports("image_to_video").items():
        print(f"  {port_id}: {info['name']} - {'✅' if info['tested'] else '⏳'}")
