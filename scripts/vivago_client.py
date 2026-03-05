#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vivago AI API Client
Core client for interacting with Vivago AI image and video generation APIs.
"""

import json
import time
import uuid
import logging
from typing import Optional, Dict, Any, List
import requests
import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)


class VivagoClient:
    """Vivago AI API Client"""
    
    # API Endpoints
    BASE_URL = "https://vivago.ai/api/gw"
    IMAGE_RESULT_URL = f"{BASE_URL}/v3/image/image/async/results"
    VIDEO_RESULT_URL = f"{BASE_URL}/v3/video/video_diffusion/async/results"
    
    # Storage configuration
    STORAGE_ENDPOINT = "http://storage.googleapis.com"
    STORAGE_BUCKET = "hidreamai-image"
    
    # Supported aspect ratios
    WH_RATIOS = ["1:1", "4:3", "3:4", "16:9", "9:16"]
    
    def __init__(
        self, 
        token: str, 
        storage_ak: Optional[str] = None, 
        storage_sk: Optional[str] = None
    ):
        """
        Initialize Vivago client.
        
        Args:
            token: Vivago API Bearer token
            storage_ak: Storage access key for image upload (optional)
            storage_sk: Storage secret key for image upload (optional)
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-accept-language": "en",
        }
        
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
    
    def upload_image(self, image_path: str) -> str:
        """
        Upload image to Vivago storage.
        
        Args:
            image_path: Path to local image file
            
        Returns:
            image_uuid: Uploaded image identifier
        """
        if not self.s3_client:
            raise ValueError("Storage credentials not provided. Cannot upload images.")
        
        import cv2
        import numpy as np
        
        image_uuid = f"j_{uuid.uuid4()}"
        logger.info(f"Uploading image {image_path} -> {image_uuid}")
        
        # Read and resize image
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
        
        # Compress and upload
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, 80]
        _, encoded_image = cv2.imencode('.jpg', image, compression_params)
        
        self.s3_client.put_object(
            Body=encoded_image.tobytes(),
            Bucket=self.STORAGE_BUCKET,
            Key=image_uuid,
            ContentType='image/jpeg'
        )
        
        return image_uuid
    
    def call_api(
        self, 
        task_name: str, 
        url: str, 
        data: Dict[str, Any], 
        result_url: str,
        max_retries: int = 20,
        retry_delay: int = 1
    ) -> Optional[List[Dict]]:
        """
        Generic API call with async task submission and polling.
        
        Args:
            task_name: Name of the task for logging
            url: API endpoint URL
            data: Request body
            result_url: URL for polling results
            max_retries: Maximum polling attempts
            retry_delay: Delay between polls in seconds
            
        Returns:
            List of sub-task results or None if failed
        """
        try:
            logger.info(f"Starting {task_name}")
            
            # Submit async task
            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            
            if "result" not in result or not result.get("result"):
                logger.error(f"Invalid response: {result}")
                return result if isinstance(result, dict) else None
            
            task_id = result.get("result", {}).get("task_id")
            if not task_id:
                logger.error("No task_id in response")
                return None
            
            logger.info(f"Task submitted: {task_id}")
            
            # Poll for results
            return self._poll_results(task_id, result_url, max_retries, retry_delay)
            
        except Exception as e:
            logger.error(f"Error in {task_name}: {e}")
            return None
    
    def _poll_results(
        self, 
        task_id: str, 
        result_url: str, 
        max_retries: int = 20, 
        retry_delay: int = 1
    ) -> Optional[List[Dict]]:
        """
        Poll for task completion.
        
        Args:
            task_id: Task identifier
            result_url: URL for polling
            max_retries: Maximum polling attempts
            retry_delay: Delay between polls
            
        Returns:
            List of sub-task results or None
        """
        url = f"{result_url}?task_id={task_id}"
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers)
                
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
                    logger.info(f"Task completed: {task_id}")
                    return sub_results
                
                # Task still processing
                logger.debug(f"Task {task_id} still processing (attempt {attempt + 1})")
                time.sleep(retry_delay)
                
            except Exception as e:
                logger.warning(f"Poll error: {e}")
                time.sleep(retry_delay)
        
        logger.error(f"Task timeout: {task_id}")
        return None
    
    # ==================== Image Generation ====================
    
    def text_to_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        wh_ratio: str = "16:9",
        batch_size: int = 1,
        version: str = "kling-image-o1",
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        Generate images from text prompt.
        
        Args:
            prompt: Text description of desired image
            negative_prompt: What to avoid in generation
            wh_ratio: Aspect ratio (1:1, 4:3, 3:4, 16:9, 9:16)
            batch_size: Number of images (1-4)
            version: Model version
            **kwargs: Additional parameters
            
        Returns:
            List of generated image results
        """
        if wh_ratio not in self.WH_RATIOS:
            raise ValueError(f"Invalid wh_ratio. Choose from: {self.WH_RATIOS}")
        
        url = f"{self.BASE_URL}/v3/image/image_gen_kling/async"
        
        data = {
            "app": None,
            "image": None,
            "mask": None,
            "module": "image_gen_kling",
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
            "version": version,
            "images": [],
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "audios": [],
            "videos": [],
            "request_id": str(uuid.uuid4())
        }
        
        return self.call_api("text_to_image", url, data, self.IMAGE_RESULT_URL)
    
    def image_to_image(
        self,
        prompt: str,
        image_uuid: str,
        wh_ratio: str = "1:1",
        batch_size: int = 1,
        version: str = "v1",
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        Transform existing image based on prompt.
        
        Args:
            prompt: Text description of transformation
            image_uuid: Source image identifier
            wh_ratio: Aspect ratio
            batch_size: Number of outputs
            version: Model version
            
        Returns:
            List of transformed image results
        """
        url = f"{self.BASE_URL}/v3/image/img2img/async"
        
        data = {
            "module": "img2img",
            "prompt": prompt,
            "images": [image_uuid],
            "params": {
                "batch_size": batch_size,
                "wh_ratio": wh_ratio,
                "custom_params": {
                    "relevance": kwargs.get("relevance", [1.0] * batch_size)
                }
            },
            "version": version,
            "request_id": str(uuid.uuid4())
        }
        
        return self.call_api("image_to_image", url, data, self.IMAGE_RESULT_URL)
    
    def image_edit(
        self,
        prompt: str,
        image_uuid: str,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        Edit image with easy edit mode.
        
        Args:
            prompt: Edit instruction
            image_uuid: Image to edit
            
        Returns:
            List of edited image results
        """
        url = f"{self.BASE_URL}/v2/image/image_easy_edit/async"
        
        data = {
            "module": "image_easy_edit",
            "prompt": prompt,
            "image_uuid": image_uuid,
            "params": kwargs.get("params", {}),
            "request_id": str(uuid.uuid4())
        }
        
        return self.call_api("image_edit", url, data, self.IMAGE_RESULT_URL)
    
    # ==================== Video Generation ====================
    
    def image_to_video(
        self,
        prompt: str,
        image_uuid: str,
        wh_ratio: str = "16:9",
        version: str = "v3Pro",
        duration: int = 5,
        mode: str = "Slow",
        fast_mode: bool = False,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        Generate video from image.
        
        Args:
            prompt: Text description of video motion
            image_uuid: Source image identifier
            wh_ratio: Aspect ratio
            version: Model version (v3Pro, v3L, kling-video-o1)
            duration: Video duration in seconds
            mode: Generation mode (Slow, Fast)
            fast_mode: Use fast mode
            **kwargs: Additional parameters
            
        Returns:
            List of generated video results
        """
        url = f"{self.BASE_URL}/v3/video/video_diffusion_img2vid/async"
        
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
            "version": version,
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "images": [image_uuid],
            "videos": [],
            "audios": [],
            "request_id": str(uuid.uuid4())
        }
        
        return self.call_api("image_to_video", url, data, self.VIDEO_RESULT_URL)
    
    def retry_call(
        self,
        func,
        max_attempts: int = 20,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """
        Retry API call multiple times.
        
        Args:
            func: Function to call
            max_attempts: Maximum retry attempts
            *args, **kwargs: Arguments for function
            
        Returns:
            Function result or None
        """
        for attempt in range(max_attempts):
            result = func(*args, **kwargs)
            if result is not None:
                return result
            logger.warning(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(1)
        
        logger.error(f"All {max_attempts} attempts failed")
        return None


# Convenience functions for direct usage
def create_client(
    token: Optional[str] = None,
    storage_ak: Optional[str] = None,
    storage_sk: Optional[str] = None
) -> VivagoClient:
    """
    Create Vivago client from environment or parameters.
    
    Environment variables:
        HIDREAM_TOKEN: API token
        STORAGE_AK: Storage access key
        STORAGE_SK: Storage secret key
    """
    import os
    
    token = token or os.environ.get("HIDREAM_TOKEN")
    storage_ak = storage_ak or os.environ.get("STORAGE_AK")
    storage_sk = storage_sk or os.environ.get("STORAGE_SK")
    
    if not token:
        raise ValueError("Token required. Set HIDREAM_TOKEN env var or pass token parameter.")
    
    return VivagoClient(token, storage_ak, storage_sk)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    client = create_client()
    
    # Example: Text to image
    results = client.text_to_image(
        prompt="a beautiful sunset over mountains",
        wh_ratio="16:9",
        batch_size=2
    )
    
    if results:
        for r in results:
            print(f"Status: {r.get('task_status')}, URL: {r.get('image')}")
