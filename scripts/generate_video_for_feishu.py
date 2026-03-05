#!/usr/bin/env python3
"""
生成视频 - Feishu专用版本 (发送视频URL)
"""
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from vivago_client import create_client


def generate_video(prompt: str, port: str = 'v3L', wh_ratio: str = '16:9', duration: int = 5):
    """
    生成视频，返回视频URL供飞书发送
    
    Returns:
        tuple: (success: bool, video_info: dict, message: str)
    """
    try:
        client = create_client()
        
        print(f"🎬 正在生成视频...")
        print(f"   Prompt: {prompt}")
        print(f"   模型: {port}")
        print(f"   时长: {duration}秒")
        print(f"   预计需要 2-3 分钟...")
        print()
        
        # 生成视频
        results = client.text_to_video(
            prompt=prompt,
            port=port,
            wh_ratio=wh_ratio,
            duration=duration,
            mode='Fast' if port == 'v3L' else 'Slow'
        )
        
        if not results:
            return False, {}, "生成失败"
        
        # 获取视频信息
        video_info = results[0]
        video_id = video_info.get('video')
        
        if not video_id:
            return False, {}, "未获取到视频ID"
        
        # 构建视频信息
        video_data = {
            'video_id': video_id,
            'video_url': f"https://media.vivago.ai/{video_id}",
            'prompt': prompt,
            'port': port,
            'duration': duration,
            'algo_version': video_info.get('algo_version'),
            'seed': video_info.get('seed')
        }
        
        return True, video_data, "视频生成成功"
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, {}, f"错误: {str(e)}"


if __name__ == '__main__':
    # 命令行调用
    if len(sys.argv) < 2:
        print("Usage: python generate_video_for_feishu.py <prompt> [port] [ratio] [duration]")
        print("  port: v3L (fast), v3Pro (quality), kling-video")
        print("  duration: 5 or 10")
        sys.exit(1)
    
    prompt = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 'v3L'
    ratio = sys.argv[3] if len(sys.argv) > 3 else '16:9'
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    
    success, video_data, message = generate_video(prompt, port, ratio, duration)
    
    if success and video_data:
        # 输出视频URL供外部读取
        print(f"VIDEO_URL:{video_data['video_url']}")
        print(f"VIDEO_ID:{video_data['video_id']}")
        print(f"PROMPT:{video_data['prompt']}")
        print(f"PORT:{video_data['port']}")
        print(f"DURATION:{video_data['duration']}")
    else:
        print(f"ERROR:{message}", file=sys.stderr)
        sys.exit(1)
