---
name: vivago-ai
description: Generate images and videos using Vivago AI (智小象) platform. Supports text-to-image, image-to-image, image editing, and image-to-video generation. Use when the user wants to create AI-generated images or videos, transform existing images, or perform image editing tasks through the Vivago AI API.
---

# Vivago AI Skill

Integration with Vivago AI (智小象) platform for AI-powered image and video generation.

## Supported Features

### Image Generation
- **Text to Image** (`txt2img`): Generate images from text descriptions
- **Image to Image** (`img2img`): Transform existing images based on prompts
- **Image Edit** (`image_easy_edit`): Edit images with easy edit mode

### Video Generation
- **Text to Video** (`txt2vid`): Generate videos from text descriptions
- **Image to Video** (`img2vid`): Generate videos from static images
- Supports multiple model versions (v3Pro, v3L, kling-video-o1)

### Additional Features
- Image upload to Vivago storage
- Batch generation (up to 4 images)
- Multiple aspect ratios (1:1, 4:3, 3:4, 16:9, 9:16)
- Automatic retry with polling

## Setup

### Environment Variables

```bash
export HIDREAM_TOKEN="your_vivago_api_token"
export STORAGE_AK="your_storage_access_key"
export STORAGE_SK="your_storage_secret_key"
```

### Installation

```bash
pip install -r requirements.txt
```

## Usage

### Python API

```python
from scripts.vivago_client import create_client

# Create client
client = create_client()

# Text to image
results = client.text_to_image(
    prompt="a beautiful sunset over mountains",
    wh_ratio="16:9",
    batch_size=2
)

# Image to video (using local image)
results = client.image_to_video(
    prompt="camera slowly zooming out",
    image_uuid=client.upload_image("/path/to/image.jpg"),
    wh_ratio="16:9",
    duration=5
)
```

### Command Line

**Text to Image:**
```bash
python scripts/txt2img.py \
  --prompt "a futuristic city" \
  --wh-ratio 16:9 \
  --batch-size 2 \
  --output results.json
```

**Image to Video:**
```bash
python scripts/img2video.py \
  --prompt "slow motion falling leaves" \
  --image /path/to/image.jpg \
  --version v3Pro \
  --duration 5 \
  --output video.json
```

## API Reference

### Models

| Feature | Available Versions | Default |
|---------|-------------------|---------|
| Text to Image | kling-image-o1 | kling-image-o1 |
| Image to Video | v3Pro, v3L, kling-video-o1 | v3Pro |

### Aspect Ratios

- `1:1` - Square
- `4:3` - Standard
- `3:4` - Portrait
- `16:9` - Widescreen
- `9:16` - Mobile/Vertical

### Task Status Codes

- `0` - Pending
- `1` - Completed
- `2` - Processing
- `3` - Failed
- `4` - Rejected (content review)

## File Structure

```
vivago-ai-skill/
├── scripts/
│   ├── vivago_client.py    # Core API client
│   ├── txt2img.py          # Text to image CLI
│   └── img2video.py        # Image to video CLI
├── requirements.txt        # Dependencies
└── SKILL.md               # This file
```

## Important Notes

### Image Download Limitation

⚠️ **Vivago AI images have access restrictions**: Due to hotlink protection, generated images cannot be directly downloaded via API.

**Workaround:**
1. Images are generated successfully and saved to your Vivago account
2. View and download images from: https://vivago.ai/history/image
3. The API returns image IDs that you can use to locate your images

### Asynchronous Processing
- API calls are asynchronous with automatic polling
- Images are automatically resized to max 1024px on longest side before upload
- Video generation supports 5 or 10 second durations
- Batch size for images: 1-4, for videos: 1
- All API calls include automatic retry logic

## Error Handling

The client handles common errors:
- Network timeouts (with retry)
- Rate limiting (with exponential backoff)
- Invalid parameters (validation before API call)
- Task failures (status code 3 or 4)

For detailed error codes, see Vivago AI API documentation.
