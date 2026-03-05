#!/usr/bin/env python3
"""
生成图片并保存到本地 - 修复版
"""
import os
import sys
import argparse

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from vivago_client import create_client


def main():
    parser = argparse.ArgumentParser(description='Generate image using Vivago AI')
    parser.add_argument('prompt', help='Image description')
    parser.add_argument('--port', default='kling-image', help='Model port (kling-image, hidream-txt2img, nano-banana)')
    parser.add_argument('--ratio', default='16:9', help='Aspect ratio (1:1, 4:3, 3:4, 16:9, 9:16)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--batch-size', type=int, default=1, help='Number of images to generate (1-4)')
    
    args = parser.parse_args()
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {args.prompt}")
    print(f"   Model: {args.port}")
    print(f"   Ratio: {args.ratio}")
    print()
    
    try:
        client = create_client()
        
        # 生成图片
        results = client.text_to_image(
            prompt=args.prompt,
            port=args.port,
            wh_ratio=args.ratio,
            batch_size=args.batch_size
        )
        
        if not results:
            print("❌ Generation failed")
            return 1
        
        # 下载并保存每张图片
        saved_files = []
        image_results = []
        for i, result in enumerate(results):
            image_id = result.get('image')
            if not image_id:
                continue
            
            print(f"📥 Processing image {i+1}/{len(results)}: {image_id}")
            
            # 尝试下载
            output_path = f"/tmp/{image_id}.png"
            downloaded_path = client.download_image(image_id, output_path)
            
            image_info = {
                "index": i + 1,
                "image_id": image_id,
                "vivago_url": f"https://vivago.ai/history/image",
                "storage_url": f"https://storage.vivago.ai/image/{image_id}.jpg",
                "local_path": downloaded_path if downloaded_path else None,
                "downloaded": os.path.exists(downloaded_path) if downloaded_path else False
            }
            image_results.append(image_info)
            
            if downloaded_path and os.path.exists(downloaded_path):
                file_size = os.path.getsize(downloaded_path)
                print(f"   ✅ Downloaded: {downloaded_path} ({file_size} bytes)")
                saved_files.append(downloaded_path)
            else:
                print(f"   ⚠️  Download blocked by Vivago")
                print(f"   🌐 View at: https://vivago.ai/history/image")
                print(f"   📋 Image ID: {image_id}")
        
        print()
        print("=" * 60)
        print(f"✅ Generated: {len(results)} images")
        print(f"💾 Downloaded: {len(saved_files)} images")
        print()
        
        # 输出详细结果
        for info in image_results:
            print(f"Image {info['index']}:")
            print(f"  ID: {info['image_id']}")
            print(f"  Vivago URL: {info['vivago_url']}")
            if info['downloaded']:
                print(f"  Local File: {info['local_path']}")
            print()
        
        # 输出JSON结果供其他工具使用
        import json
        result_json = {
            "success": True,
            "count": len(results),
            "saved": len(saved_files),
            "files": saved_files,
            "results": results
        }
        
        # 保存JSON结果
        json_path = "/tmp/vivago_result.json"
        with open(json_path, 'w') as f:
            json.dump(result_json, f, indent=2)
        print(f"📄 Result JSON: {json_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
