# Vivago AI Skill

AI image and video generation using Vivago AI (智小象) platform.

## Features

- 🎨 **Text to Image**: Generate images from text descriptions
- 🎬 **Image to Video**: Animate static images into videos
- 🖼️ **Image to Image**: Transform and restyle existing images
- ✏️ **Image Edit**: Easy image editing with prompts
- 📤 **Image Upload**: Automatic upload and resizing

## Quick Start

### 1. Setup Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Images

```bash
python scripts/txt2img.py \
  --prompt "a cat astronaut in space" \
  --wh-ratio 16:9 \
  --batch-size 2
```

### 4. Generate Videos

```bash
python scripts/img2video.py \
  --prompt "slow zoom out" \
  --image photo.jpg \
  --duration 5
```

## Python API

```python
from scripts.vivago_client import create_client

client = create_client()

# Generate images
results = client.text_to_image(
    prompt="beautiful landscape",
    wh_ratio="16:9",
    batch_size=2
)

# Generate video from local image
image_uuid = client.upload_image("photo.jpg")
video_results = client.image_to_video(
    prompt="gentle camera movement",
    image_uuid=image_uuid,
    duration=5
)
```

## Configuration

Required environment variables:
- `HIDREAM_TOKEN`: Vivago API token
- `STORAGE_AK`: Storage access key
- `STORAGE_SK`: Storage secret key

## License

MIT
