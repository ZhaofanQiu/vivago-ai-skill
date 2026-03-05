# Vivago AI Skill

AI image and video generation using Vivago AI (智小象) platform.

## 📊 功能状态

### 一级功能（大功能划分）

| 一级功能 | 状态 | 说明 |
|---------|------|------|
| 🎨 **文生图 (Text-to-Image)** | ✅ 已实现 | 支持 Kling O1 / Vivago 2.0 / Nano Banana 2 |
| 📝 **文生视频 (Text-to-Video)** | ✅ 已实现 | 支持 v3L(快) / v3Pro(质) / Kling video O1 |
| 🎬 **图生视频 (Image-to-Video)** | ✅ 已实现 | 支持 v3L / v3Pro / Kling video O1 |
| 🔄 **图生图 (Image-to-Image)** | ✅ 已实现 | 支持 Kling O1(快) / Nano Banana 2(质)，多图融合 |
| ⬆️ **图像上传 (Image Upload)** | ✅ 已实现 | 支持自动压缩 |

> **注**：图像编辑、AI肖像、虚拟试衣等功能均可通过图生图实现，无需单独一级功能

### 未来计划

| 一级功能 | 状态 | 说明 |
|---------|------|------|
| 🎞️ **视频首尾帧 (Keyframe-to-Video)** | ⏳ 规划中 | 根据首尾帧生成过渡视频 |
| 🎭 **视频模板 (Template-to-Video)** | ⏳ 规划中 | 特定类型视频特效（固定模板） |

### 二级端口（具体API端点）

#### 文生图 (Text-to-Image)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `kling-image` | **Kling O1** | `/v3/image/image_gen_kling/async` | ✅ 已测试 | ✅ | 快 | 优秀 |
| `hidream-txt2img` | **Vivago.ai 2.0** | `/v3/image/txt2img/async` | ✅ 已测试 | - | 中等 | 良好 |
| `nano-banana` | **Nano Banana 2** | `/v3/image/image_gen_std/async` | ✅ 已测试 | - | 慢 | 极优 |

#### 图生图 (Image-to-Image)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `kling-image` | **Kling O1** | `/v3/image/image_gen_kling/async` | ✅ 已测试 | ✅ | 快 | 优秀 |
| `nano-banana` | **Nano Banana 2** | `/v3/image/image_gen_std/async` | ✅ 已测试 | - | 慢 | 极优 |

> **功能覆盖**：图生图支持多图输入融合，可实现风格迁移、图像编辑、AI换脸、虚拟试衣等场景

> **关键参数**：`strength`(变化强度), `relevance`[权重数组], `image_guidance_scale`

---

## 🏗️ 架构设计

### 层级机制

```
Vivago AI Skill
├── 一级功能 (Category)          # 大功能划分
│   ├── text_to_image            # 文生图
│   ├── image_to_video           # 图生视频
│   ├── image_to_image           # 图生图
│   └── ...
│
└── 二级端口 (Port)              # 具体API配置
    ├── 端点路径 (endpoint)       # API提交地址
    ├── 回调路径 (result_endpoint) # 结果查询地址
    ├── 版本参数 (version)        # 模型版本标识
    └── 显示名称 (display_name)   # Vivago网站显示名称
```

### 核心设计原则

1. **一级功能** = 业务功能划分（文生图、图生视频等）
2. **二级端口** = 具体API配置（端点、版本、回调路径）
3. **display_name** = 与 Vivago 网站模型名称对齐
4. **相同端点 + 不同 version = 不同模型**（关键架构点）

### 示例：图生视频端口配置

```json
{
  "v3Pro": {
    "display_name": "Vivago.ai 2.0",
    "endpoint": "/v3/video/video_diffusion_img2vid/async",
    "result_endpoint": "/v3/video/video_diffusion/async/results",
    "version": "v3Pro"
  },
  "v3L": {
    "display_name": "Vivago.ai 2.0 360p",
    "endpoint": "/v3/video/video_diffusion_img2vid/async",  // 相同端点
    "result_endpoint": "/v3/video/video_diffusion/async/results",
    "version": "v3L"  // 不同版本 = 不同模型
  }
}
```

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

**查看可用模型：**
```python
from scripts.vivago_client import create_client

client = create_client()

# 查看所有一级功能
for cat_id, info in client.list_categories().items():
    print(f"{info['name']} ({info['name_en']})")

# 查看文生图可用模型
for port_id, info in client.list_ports("text_to_image").items():
    print(f"  {info['display_name']}: {info['speed']}, {info['quality']}")
```

**文生图（Kling O1）：**
```python
results = client.text_to_image(
    prompt="一只可爱的小熊猫",
    port="kling-image",  # 或 "hidream-txt2img", "nano-banana"
    wh_ratio="1:1",
    batch_size=1
)
```

**图生视频（Kling video O1）：**
```python
results = client.image_to_video(
    prompt="熊猫慢慢转头",
    image_uuid="j_xxxxx",
    port="kling-video",  # 或 "v3Pro", "v3L"
    duration=5,
    mode="Slow"
)
```

---

## ⚠️ 重要提示

### 模型选择建议

| 场景 | 推荐模型 | 说明 |
|------|---------|------|
| 快速生成 | Kling O1 | 速度快，质量优秀 |
| 高质量图片 | Nano Banana 2 | 慢但效果最佳 |
| 高清视频 | Vivago.ai 2.0 | 高质量，4分钟 |
| 快速视频 | Vivago.ai 2.0 360p | 360p，速度快 |
| 最佳视频 | Kling video O1 | 质量最优 |

### 视频生成注意事项

- ⏱️ **生成时间较长**: 通常需要 2-3 分钟
- 🔄 **避免频繁调用**: 请合理安排测试频率
- 📶 **网络稳定性**: 长时间等待可能导致回调失败
- 💰 **Credits消耗**: 视频生成消耗更多 credits

### 回调路径差异

不同端口可能使用不同的回调路径：
- 普通图片：`/v3/image/txt2img/async/results`
- Nano Banana：`/v3/image/image/async/results/batch`
- 视频：`/v3/video/video_diffusion/async/results`

---

## 📁 项目结构

```
vivago-ai-skill/
├── scripts/
│   ├── vivago_client.py      # 核心客户端（支持层级调用）
│   ├── api_ports.json        # 端口配置（含 display_name）
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

### v0.4.1 (2026-03-05)
- ✅ 测试 v3Pro 文生视频 - 成功
- ✅ 测试 Kling video O1 文生视频 - 成功
  - 关键发现：使用 `/v3/video/video_diffusion_gen2vid/async` 端点
  - module: `video_diffusion_gen2vid`
- ✅ 修复 `text_to_video()` 方法，根据 endpoint 动态设置 module
- ✅ 所有文生视频端口测试完成

### v0.4.0 (2026-03-05)
- ✅ 新增 **文生视频** 一级功能
- ✅ 测试 Vivago.ai 2.0 360p 文生视频 (v3L)
- ✅ 关键发现：文生视频和图生视频共用 `/v3/video/video_diffusion/async` 端点
- ✅ 修复 `text_to_video()` 方法，支持 `magic_prompt` 参数

### v0.3.1 (2026-03-05)
- ✅ 修复 Nano Banana 2 支持
- ✅ 修正 `result_endpoint` 路径
- ✅ 添加 `mode=2K` 参数

### v0.3.0 (2026-03-05)
- ✅ 添加 Nano Banana 2 模型支持
- ✅ 添加 `display_name` 字段，与 Vivago 网站对齐
- ✅ 整理模型名称对应表
- ✅ 更新架构说明文档

### v0.2.2 (2026-03-05)
- ✅ 测试 kling-video 端口
- ✅ 所有图生视频端口测试完成

### v0.2.0 (2026-03-05)
- ✅ 重构层级架构，支持一级/二级端口
- ✅ 添加 API 端口配置系统

### v0.1.0 (2026-03-05)
- ✅ 初始版本
- ✅ 文生图功能（Kling O1）

---

## 📞 问题反馈

如有问题，请查看 `test_reports/` 目录下的测试报告。

### 模型名称确认

如果不确定某个二级端口的 Vivago 网站显示名称，可以询问我确认后再添加。
