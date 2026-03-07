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
- **Video Templates** (`template_to_video`): 134 pre-defined video effects
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

# Video Templates - use pre-defined effects
results = client.template_to_video(
    image_uuid=client.upload_image("/path/to/image.jpg"),
    template="ghibli",  # See available templates below
    wh_ratio="9:16"
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

### Feishu Channel Messaging Guidelines

When sending generated content through Feishu (飞书) channel:

| Content Type | Send Method | Example |
|-------------|-------------|---------|
| **Images** | ✅ Direct file upload | Attach image file directly |
| **Videos** | ❌ **Must send as link** | `https://media.vivago.ai/{video_uuid}` |

**⚠️ Critical**: Videos **CANNOT** be sent as file attachments in Feishu. Always construct and send the direct media URL:

```
https://media.vivago.ai/b1268f08-ac32-4b83-863f-a419797d768e.mp4
```

**Why**: Feishu does not support playable video attachments. Sending video files directly will result in delivery failure or unplayable content.

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

## Video Templates Reference

The following **134 video templates** are available via `template_to_video()`:

### Quick Categories

| Category | Count | Example Templates |
|----------|-------|-------------------|
| **Style Transfer** | 20+ | ghibli, 1930s-2000s vintage styles |
| **Harry Potter** | 4 | magic_reveal_ravenclaw, gryffindor, hufflepuff, slytherin |
| **Wings/Fantasy** | 10+ | angel_wings, phoenix_wings, crystal_wings, fire_wings |
| **Superheroes** | 5+ | iron_man, cat_woman, ghost_rider |
| **Dance** | 10+ | apt, dadada, dance, limbo_dance |
| **Effects** | 15+ | ash_out, metallic_liquid, flash_flood |
| **Thanksgiving** | 10+ | turkey_chasing, autumn_feast, gratitude_photo |
| **Comics/Cartoon** | 8+ | gta_star, anime_figure, bring_comics_to_life |
| **Products** | 8+ | glasses_display, music_box, food_product_display |
| **Scenes** | 20+ | romantic_kiss, graduation, starship_chef |

### Popular Templates

| Template ID | Description |
|-------------|-------------|
| `ghibli` / `ghibli2` | Studio Ghibli animation style |
| `magic_reveal_ravenclaw` | Harry Potter Ravenclaw transformation |
| `magic_reveal_gryffindor` | Harry Potter Gryffindor transformation |
| `magic_reveal_hufflepuff` | Harry Potter Hufflepuff transformation |
| `magic_reveal_slytherin` | Harry Potter Slytherin transformation |
| `iron_man` | Iron Man armor assembly |
| `angel_wings` / `phoenix_wings` / `crystal_wings` / `fire_wings` | Wing transformations |
| `cat_woman` | Cat Woman style |
| `ghost_rider` | Ghost Rider flaming skull |
| `joker` | Joker villain style |
| `mermaid` | Mermaid underwater scene |
| `snow_white` | Snow White princess |
| `barbie` | Barbie princess transformation |
| `me_in_hand` | Miniature figure in hand |
| `music_box` | Rotating figure on music box |
| `anime_figure` | Transform into anime figure |
| `gta_star` | GTA game style transformation |
| `apt` / `dadada` / `dance` | Dance templates |
| `ash_out` | Disintegrate into ashes |
| `eye_of_the_storm` | Thunder god awakening |
| `metallic_liquid` | Metal mask transformation |
| `flash_flood` | Water/flood effect |
| `turkey_chasing` / `turkey_away` / `turkey_giant` | Thanksgiving turkey scenes |
| `autumn_feast` / `autumn_stroll` | Autumn scenes |
| `renovation_of_old_photos` | Colorize B&W photos |
| `graduation` | Graduation ceremony |
| `glasses` / `glasses_display` | Glasses/eyewear showcase |
| `bikini` / `sexy_man` / `sexy_pants` | Fashion/beach |
| `romantic_kiss` / `boyfriends_rose` / `girlfriends_rose` | Romantic scenes |
| `ai_archaeologist` / `starship_chef` / `cyber_cooker` | Sci-fi characters |
| `jungle_reign` / `panther_queen` / `roar_of_the_dustlands` / `tiger_snuggle` | Animal companions |
| `instant_sadness` / `headphone_vibe` / `relax` | Emotion/reaction |
| `frost_alert` | Cold/freeze effect |
| `bald_me` | Bald transformation |
| `boom_hair` / `curl_pop` / `long_hair` | Hair transformations |
| `muscles` | Muscle transformation |
| `face_punch` / `gun_point` | Action effects |
| `static_shot` / `tracking_shot` / `orbit_shot` / `push_in` / `zoom_out` / `handheld_shot` | Camera movements |
| `earth_zoom_in` / `earth_zoom_out` | Earth zoom effects |

### View All Templates

```python
from scripts.template_manager import get_template_manager

manager = get_template_manager()
templates = manager.list_templates()

print(f"Total templates: {len(templates)}")
for tid, name in sorted(templates.items()):
    print(f"  {tid}: {name}")
```

### Usage Example
```python
from scripts.vivago_client import create_client

client = create_client()

# Upload image
image_uuid = client.upload_image("/path/to/photo.jpg")

# Apply Ghibli style template
results = client.template_to_video(
    image_uuid=image_uuid,
    template="ghibli",
    wh_ratio="9:16"
)

# Harry Potter transformation
results = client.template_to_video(
    image_uuid=image_uuid,
    template="magic_reveal_ravenclaw",
    wh_ratio="9:16"
)
```
