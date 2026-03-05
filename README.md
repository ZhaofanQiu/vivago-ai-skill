# Vivago AI Skill

AI image and video generation using Vivago AI (智小象) platform.

## 📊 功能状态

### 一级功能（大功能划分）

| 一级功能 | 状态 | 说明 |
|---------|------|------|
| 🎨 **文生图 (Text-to-Image)** | ✅ 已实现 | 支持多种模型 |
| 🎬 **图生视频 (Image-to-Video)** | 🧪 调试中 | 支持 v3Pro/v3L |
| 🔄 **图生图 (Image-to-Image)** | ✅ 代码就绪 | 待测试 |
| ✏️ **图像编辑 (Image Edit)** | ✅ 代码就绪 | 待测试 |
| 👤 **AI肖像 (AI Portrait)** | ⏳ 待实现 | 需要 face/body UUID |
| 👗 **虚拟试衣 (Try On)** | ⏳ 待实现 | 需要 model/cloth UUID |
| ⬆️ **图像上传 (Image Upload)** | ✅ 已实现 | 支持自动压缩 |

### 二级端口（具体API端点）

#### 文生图 (Text-to-Image)

| 二级端口 | 端点 | 状态 | 默认 | 说明 |
|---------|------|------|------|------|
| `kling-image` | `/v3/image/image_gen_kling/async` | ✅ 已测试 | ✅ | Kling 图像模型 |
| `hidream-txt2img` | `/v3/image/txt2img/async` | ⏳ 待测试 | - | 旧版文生图 |

#### 图生视频 (Image-to-Video)

| 二级端口 | 端点 | 状态 | 默认 | 说明 |
|---------|------|------|------|------|
| `v3Pro` | `/v3/video/video_diffusion_img2vid/async` | 🧪 调试中 | ✅ | 高质量，较慢 |
| `v3L` | `/v3/video/video_diffusion_img2vid/async` | ⏳ 待测试 | - | 快速版本 |
| `kling-video` | `/v3/video/video_diffusion_img2vid/async` | ⏳ 待测试 | - | Kling 视频模型 |

#### 图生图 (Image-to-Image)

| 二级端口 | 端点 | 状态 | 说明 |
|---------|------|------|------|
| `img2img` | `/v3/image/img2img/async` | ⏳ 待测试 | 图像风格转换 |
| `image_edit` | `/v2/image/image_easy_edit/async` | ⏳ 待测试 | 简易图像编辑 |

#### 视频结果查询

| 二级端口 | 端点 | 状态 | 说明 |
|---------|------|------|------|
| `video_diffusion` | `/v3/video/video_diffusion/async/results` | 🧪 调试中 | 图生视频结果 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
export HIDREAM_TOKEN="your_vivago_api_token"
export STORAGE_AK="your_storage_access_key"
export STORAGE_SK="your_storage_secret_key"
```

### 3. 使用示例

**文生图（Kling模型）:**
```python
from scripts.vivago_client import create_client

client = create_client()

# 使用默认端口 (kling-image)
results = client.text_to_image(
    prompt="一只可爱的小熊猫",
    wh_ratio="1:1",
    batch_size=1
)

# 或使用指定端口
results = client.text_to_image(
    prompt="一只可爱的小熊猫",
    port="kling-image",  # 指定二级端口
    wh_ratio="1:1",
    batch_size=1
)
```

**图生视频（v3Pro模型）:**
```python
# 注意：视频生成需要2-3分钟，请谨慎调用
results = client.image_to_video(
    prompt="熊猫慢慢转头",
    image_uuid="j_xxxxx",
    port="v3Pro",  # 或 "v3L" 快速版本
    duration=5,
    mode="Slow"
)
```

---

## 🏗️ 架构设计

### 层级机制

```
一级功能 (大功能)
├── 文生图 (text_to_image)
│   ├── kling-image (默认)
│   ├── hidream-txt2img
│   └── ... (未来扩展)
│
├── 图生视频 (image_to_video)
│   ├── v3Pro (默认)
│   ├── v3L
│   └── kling-video
│
└── 图生图 (image_to_image)
    ├── img2img
    └── image_edit
```

### 端口配置

端口配置存储在 `scripts/api_ports.json`，便于动态扩展：

```json
{
  "text_to_image": {
    "default": "kling-image",
    "ports": {
      "kling-image": {
        "endpoint": "/v3/image/image_gen_kling/async",
        "result_endpoint": "/v3/image/txt2img/async/results",
        "version": "kling-image-o1"
      }
    }
  }
}
```

---

## ⚠️ 重要提示

### 视频生成注意事项

- ⏱️ **生成时间较长**: 通常需要 2-3 分钟
- 🔄 **避免频繁调用**: 请合理安排测试频率
- 📶 **网络稳定性**: 长时间等待可能导致回调失败
- 💰 **Credits消耗**: 视频生成消耗更多 credits

### 测试建议

```bash
# 先运行简单测试
python tests/test_suite.py --test txt2img_basic

# 视频测试请单独运行，并耐心等待
python tests/test_suite.py --test img2video_basic
```

---

## 📁 项目结构

```
vivago-ai-skill/
├── scripts/
│   ├── vivago_client.py      # 核心客户端（支持层级调用）
│   ├── api_ports.json        # 端口配置
│   ├── txt2img.py            # 文生图 CLI
│   ├── img2video.py          # 图生视频 CLI
│   └── ...
├── tests/                     # 测试套件
├── test_reports/              # 测试报告
├── README.md                  # 本文件
└── requirements.txt
```

---

## 📝 更新日志

### v0.2.0 (2026-03-05)
- ✅ 重构层级架构，支持一级/二级端口
- ✅ 添加 API 端口配置系统
- 🧪 图生视频功能调试中
- ✅ 更新 README 功能状态表格

### v0.1.0 (2026-03-05)
- ✅ 初始版本
- ✅ 文生图功能（Kling模型）
- ✅ 基础测试套件

---

## 🔧 开发计划

- [ ] 完成图生视频调试
- [ ] 添加图生图功能测试
- [ ] 添加图像编辑功能测试
- [ ] 添加 AI 肖像功能
- [ ] 添加虚拟试衣功能
- [ ] 工作流引擎（功能组合）

---

## 📞 问题反馈

如有问题，请查看 `test_reports/` 目录下的测试报告。
