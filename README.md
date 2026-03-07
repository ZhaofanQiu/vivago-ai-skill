# Vivago AI Skill

<p align="center">
  <img src="assets/logo.jpg" alt="Vivago AI Skill Logo" width="80%">
</p>

AI image and video generation using Vivago AI (智小象) platform.

[![CI](https://github.com/ZhaofanQiu/vivago-ai-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhaofanQiu/vivago-ai-skill/actions)

## 📚 文档

- [快速开始](docs/quickstart.md) - 5分钟上手
- [API参考](docs/api_reference.md) - 完整API文档
- [架构设计](docs/architecture.md) - 系统设计
- [测试指南](docs/testing.md) - 如何测试
- [测试报告](TEST_REPORT.md) - Tier 1-4 完整测试报告
- [测试报告 2026-03-07](docs/TEST_REPORT_2026_03_07.md) - 最新系统测试报告
- [测试策略](docs/TEST_STRATEGY_OPTIMIZED.md) - 智能测试优化策略
- [故障排查](docs/troubleshooting.md) - 常见问题
- [更新日志](docs/CHANGELOG.md) - 版本历史

## 📊 功能状态

### 一级功能（大功能划分）

| 一级功能 | 状态 | 说明 |
|---------|------|------|
| 🎨 **文生图 (Text-to-Image)** | ✅ 已测试 | 支持 Kling O1 / Vivago 2.0 / Nano Banana 2 |
| 📝 **文生视频 (Text-to-Video)** | ✅ 已测试 | 支持 v3L(快) / v3Pro(质) / Kling video O1 |
| 🎬 **图生视频 (Image-to-Video)** | ✅ 已测试 | 支持 v3L / v3Pro / Kling video O1 |
| 🔄 **图生图 (Image-to-Image)** | ✅ 已测试 | 支持 Kling O1(快) / Nano Banana 2(质)，多图融合 |
| 🎞️ **视频首尾帧 (Keyframe-to-Video)** | ✅ 已测试 | 支持 v3L / v3Pro |
| 🎭 **视频模板 (Template-to-Video)** | ✅ 已测试 | 支持 134+ 模板效果 |
| ⬆️ **图像上传 (Image Upload)** | ✅ 已实现 | 支持自动压缩 |

### 测试覆盖率

| 层级 | 测试项 | 通过 | 积分消耗 | 状态 |
|------|--------|------|----------|------|
| Tier 1 | 单元测试 | 10 | 0 | ✅ 完成 |
| Tier 2 | 组件集成 | 4 | 16 | ✅ 完成 |
| Tier 3 | 核心功能 | 6 | 106 | ✅ 完成 |
| Tier 4 | 端口采样 | 8 | 168 | ✅ 完成 |
| Tier 5 | 模板采样 | 14 | 420 | ✅ 完成 |
| **总计** | | **42** | **710+** | **100%** |

> ✅ **系统状态**: 健康运行 - 详见 [TEST_REPORT_2026_03_07.md](docs/TEST_REPORT_2026_03_07.md)

### 二级端口（具体API端点）

#### 文生图 (Text-to-Image)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 | 积分 |
|---------|-------------|------|------|------|------|------|------|
| `kling-image` | **Kling O1** | `/v3/image/image_gen_kling/async` | ✅ 已测试 | ✅ | 快 | 优秀 | 8 |
| `hidream-txt2img` | **Vivago.ai 2.0** | `/v3/image/txt2img/async` | ✅ 已测试 | - | 中等 | 良好 | **2** |
| `nano-banana` | **Nano Banana 2** | `/v3/image/image_gen_std/async` | ✅ 已测试 | - | 慢 | 极优 | 10 |

#### 图生图 (Image-to-Image)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `kling-image` | **Kling O1** | `/v3/image/image_gen_kling/async` | ✅ 已测试 | ✅ | 快 | 优秀 |
| `nano-banana` | **Nano Banana 2** | `/v3/image/image_gen_std/async` | ✅ 已测试 | - | 慢 | 极优 |

> **功能覆盖**：图生图支持多图输入融合，可实现风格迁移、图像编辑、AI换脸、虚拟试衣等场景

> **关键参数**：`strength`(变化强度), `relevance`[权重数组], `image_guidance_scale`

#### 图生视频 (Image-to-Video)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `v3Pro` | **Vivago.ai 2.0** | `/v3/video/video_diffusion_img2vid/async` | ✅ 已测试 | ✅ | 慢 | 极优 |
| `v3L` | **Vivago.ai 2.0 360p** | `/v3/video/video_diffusion_img2vid/async` | ✅ 已测试 | - | 快 | 良好 |
| `kling-video` | **Kling video O1** | `/v3/video/video_diffusion_img2vid/async` | ✅ 已测试 | - | 中等 | 极优 |

#### 文生视频 (Text-to-Video)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `v3L` | **Vivago.ai 2.0 360p** | `/v3/video/video_diffusion/async` | ✅ 已测试 | ✅ | 快 | 良好 |
| `v3Pro` | **Vivago.ai 2.0** | `/v3/video/video_diffusion/async` | ✅ 已测试 | - | 慢 | 极优 |
| `kling-video` | **Kling video O1** | `/v3/video/video_diffusion_gen2vid/async` | ✅ 已测试 | - | 中等 | 极优 |

#### 视频首尾帧 (Keyframe-to-Video)

| 代码端口 | 网站显示名称 | 端点 | 状态 | 默认 | 速度 | 质量 |
|---------|-------------|------|------|------|------|------|
| `v3L` | **Vivago.ai 2.0 360p** | `/v3/video/video_diffusion_keyframes/async` | ✅ 已测试 | ✅ | 快 | 良好 |
| `v3Pro` | **Vivago.ai 2.0** | `/v3/video/video_diffusion_keyframes/async` | ✅ 已测试 | - | 慢 | 极优 |

#### 视频模板 (Template-to-Video)

**134+ 可用模板**，按类别分类：

| 类别 | 数量 | 示例模板 |
|------|------|----------|
| **风格转换** | 20+ | ghibli, 1930s-2000s vintage styles |
| **哈利波特** | 4 | magic_reveal_ravenclaw, gryffindor, hufflepuff, slytherin |
| **翅膀/奇幻** | 10+ | angel_wings, phoenix_wings, crystal_wings |
| **超级英雄** | 5+ | iron_man, cat_woman, ghost_rider |
| **舞蹈** | 10+ | apt, dadada, dance, limbo_dance |
| **特效** | 15+ | ash_out, metallic_liquid, flash_flood |
| **感恩节** | 10+ | turkey_chasing, autumn_feast, gratitude_photo |
| **漫画/卡通** | 8+ | gta_star, anime_figure, bring_comics_to_live |
| **产品展示** | 8+ | glasses_display, music_box, food_product_display |
| **场景** | 20+ | romantic_kiss, graduation, starship_chef |

> 查看完整模板列表：`scripts/api_ports.json` 或运行 `python -c "from scripts.template_manager import get_template_manager; tm = get_template_manager(); print(f'Total: {len(tm.templates)}')
`

---

## 🏗️ 架构设计

### 层级机制

```
Vivago AI Skill
├── 一级功能 (Category)          # 大功能划分
│   ├── text_to_image            # 文生图
│   ├── image_to_video           # 图生视频
│   ├── image_to_image           # 图生图
│   ├── keyframe_to_video        # 视频首尾帧
│   └── template_to_video        # 视频模板
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

**图生图（多图融合）：**
```python
# 单图风格迁移
results = client.image_to_image(
    prompt="将图片转换为水彩画风格",
    image_uuids=["p_xxxxx"],
    port="kling-image",
    strength=0.8
)

# 多图融合（皮卡丘 + 绿头鸭）
results = client.image_to_image(
    prompt="一只皮卡丘骑在绿头鸭背上",
    image_uuids=["p_pikachu", "p_duck"],
    port="kling-image",
    strength=0.8,
    relevance=[0.9, 0.9]  # 两张图的参考权重
)
```

**视频模板（Ghibli 风格）：**
```python
results = client.template_to_video(
    image_uuid="p_photo",           # 输入图片
    template="ghibli",              # 模板名称
    wh_ratio="9:16"
)
```

---

## 🧪 智能测试系统

项目包含完整的智能测试优化系统：

```bash
# 查看推荐测试列表
python tests/smart_test_optimizer.py

# 执行单元测试 (0积分)
python tests/test_tier1_unit.py

# 执行图片测试
python tests/test_tier3_image.py

# 执行视频测试
python tests/tier4_video_v3l.py
```

### 测试策略特点

- **风险优先**: 优先测试从未测试或长期未测试的功能
- **成本优化**: 智能选择低成本高回报的测试项
- **历史追踪**: 完整记录每次测试的历史记录
- **动态调整**: 根据测试结果动态调整推荐策略

详见 [docs/TEST_STRATEGY_OPTIMIZED.md](docs/TEST_STRATEGY_OPTIMIZED.md)

---

## ⚠️ 重要提示

### 飞书消息发送限制

**图片**: ✅ 可直接发送，显示为图片格式  
**视频**: ❌ 无法直接发送可播放格式，只能发送链接

### 模型选择建议

| 场景 | 推荐模型 | 说明 |
|------|---------|------|
| 快速生成图片 | Kling O1 | 速度快，质量优秀 |
| 低成本测试 | Vivago 2.0 | 仅需2积分 |
| 高质量图片 | Nano Banana 2 | 慢但效果最佳 |
| 图生图/风格迁移 | Kling O1 | 速度快，支持多图融合 |
| 高清视频 | Vivago.ai 2.0 (v3Pro) | 高质量 |
| 快速视频 | Vivago.ai 2.0 360p (v3L) | 360p，速度快 |
| 最佳视频 | Kling video O1 | 质量最优 |

### 视频生成注意事项

- ⏱️ **生成时间较长**: 通常需要 2-5 分钟
- 🔄 **避免频繁调用**: 请合理安排测试频率
- 💰 **Credits消耗**: 视频生成消耗更多 credits
- 📊 **积分参考**: 图片 2-10 积分，视频 20-80 积分

---

## 📁 项目结构

```
vivago-ai-skill/
├── scripts/
│   ├── vivago_client.py      # 核心客户端（支持层级调用）
│   ├── api_ports.json        # 187个端口配置
│   ├── template_manager.py   # 模板管理器（134+模板）
│   └── ...
├── tests/
│   ├── test_tier1_unit.py    # 单元测试
│   ├── test_tier3_*.py       # 核心功能测试
│   ├── tier4_*.py            # 端口采样测试
│   ├── tier5_templates/      # 模板测试套件
│   └── smart_test_optimizer.py  # 智能优化器
├── docs/                      # 文档目录
│   ├── api_reference.md
│   ├── architecture.md
│   ├── TEST_STRATEGY_OPTIMIZED.md
│   └── ...
├── TEST_REPORT.md            # 测试报告
├── requirements.txt
└── README.md                 # 本文件
```

---

## 📝 更新日志

### v0.8.0 (2026-03-07)
- ✅ 完成 Tier 1-4 完整测试（27项测试100%通过）
- ✅ 建立智能测试优化系统
- ✅ 修复 Nano Banana 版本参数 Bug
- ✅ 测试覆盖率达到 80%（端口）/ 61%（功能）
- ✅ 总积分消耗 290（约¥12.2）
- ✅ 新增测试历史追踪系统

### v0.7.0 (2026-03-06)
- ✅ 新增 **视频首尾帧 (Keyframe-to-Video)** 功能
- ✅ 支持根据首尾帧生成过渡视频
- ✅ 添加 v3L 端口支持
- ✅ 测试成功：皮卡丘 → 柯基变身视频

### v0.6.0 (2026-03-06)
- ✅ 重构功能架构，简化一级功能
- ✅ 图生图支持 Kling O1 (快) 和 Nano Banana 2 (质)
- ✅ 支持多图输入融合 (`image_uuids` + `relevance`)

### v0.5.0 (2026-03-06)
- ✅ 添加 Nano Banana 2 图生图（多图输入）
- ✅ 支持图像风格迁移、编辑、融合功能

### v0.4.0 (2026-03-05)
- ✅ 新增 **文生视频** 一级功能
- ✅ 支持 v3L / v3Pro / Kling video O1

### v0.1.0 (2026-03-05)
- ✅ 初始版本
- ✅ 文生图功能（Kling O1）

---

## 📞 问题反馈

如有问题，请查看：
- [TEST_REPORT.md](TEST_REPORT.md) - 完整测试报告
- [docs/troubleshooting.md](docs/troubleshooting.md) - 故障排查
- [docs/testing.md](docs/testing.md) - 测试指南

---

*最后更新: 2026-03-07*  
*版本: v0.8.0*
