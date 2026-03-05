#!/usr/bin/env python3
"""
生成视频并通过飞书发送 - Feishu专用版本
"""
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from vivago_client import create_client


def generate_and_send_video(prompt: str, port: str = 'v3L', wh_ratio: str = '16:9', duration: int = 5):
    """
    生成视频并保存到本地，返回文件路径供飞书发送
    
    Returns:
        tuple: (success: bool, file_paths: list, message: str)
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
            return False, [], "生成失败"
        
        # 下载视频
        saved_files = []
        for result in results:
            video_id = result.get('video')
            if not video_id:
                continue
            
            print(f"📥 正在下载视频...")
            
            output_path = f"/tmp/{video_id}"
            downloaded_path = client.download_video(video_id, output_path)
            
            if downloaded_path and os.path.exists(downloaded_path):
                file_size = os.path.getsize(downloaded_path)
                print(f"   ✅ 已保存: {downloaded_path} ({file_size/1024/1024:.1f} MB)")
                saved_files.append(downloaded_path)
            else:
                print(f"   ❌ 下载失败")
        
        if saved_files:
            return True, saved_files, f"成功生成 {len(saved_files)} 个视频"
        else:
            return False, [], "视频下载失败"
            
    except Exception as e:
        return False, [], f"错误: {str(e)}"


if __name__ == '__main__':
    # 命令行调用，输出文件路径
    if len(sys.argv) < 2:
        print("Usage: python generate_video_for_feishu.py <prompt> [port] [ratio] [duration]")
        print("  port: v3L (fast), v3Pro (quality), kling-video")
        print("  duration: 5 or 10")
        sys.exit(1)
    
    prompt = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 'v3L'
    ratio = sys.argv[3] if len(sys.argv) > 3 else '16:9'
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    
    success, files, message = generate_and_send_video(prompt, port, ratio, duration)
    
    # 输出文件路径到 stdout，供外部读取
    if success and files:
        for f in files:
            print(f)
    else:
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)
