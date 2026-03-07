# 更新日志

## [0.8.1] - 2026-03-07

### 系统测试完成 ✅

#### 完整测试覆盖
- ✅ Tier 1-5 全部测试通过 (42/42, 100%)
- ✅ 总积分消耗: 720+
- ✅ 14个视频模板验证通过
- ✅ 39项功能测试全部通过

#### Bug修复
- **Nano Banana 请求格式**: 移除 `version` 字段，修复 "Unknown Error"
- **模板回调路径**: `style_transformer` 类型使用正确回调路径，修复 404 错误

#### 安全改进
- **30分钟超时机制**: 所有 API 调用默认 30 分钟超时
- **防止重复计费**: 360次轮询 × 5秒间隔，确保任务完成前不超时

#### 新增测试
- `tests/tier1_report.py` - Tier 1 测试报告
- `tests/tier2_integration.py` - 组件集成测试
- `tests/tier3_image.py` - 核心图片功能测试
- `tests/tier4_image_ports.py` - 图片端口采样测试
- `tests/test_3_templates.py` - 3模板测试
- `tests/test_5_templates.py` - 5模板测试
- `tests/test_5_more_templates.py` - 再5模板测试
- `tests/test_renovation.py` - 老照片修复测试
- `docs/TEST_REPORT_2026_03_07.md` - 完整测试报告

### 系统状态
🟢 **健康运行** - 所有核心功能验证通过，可投入生产使用

---

## [0.8.0] - 2026-03-06

### P0 优化完成

#### 安全改进
- ✅ 添加 `.env` 环境变量支持
- ✅ 添加 `.gitignore` 保护敏感文件
- ✅ 创建 `scripts/config.py` 统一配置管理

#### 错误处理
- ✅ 创建 `scripts/exceptions.py` 自定义异常体系
- ✅ 12个异常类覆盖所有错误场景
- ✅ 清晰的错误分类和上下文

#### 测试框架
- ✅ 创建 `tests/framework.py` 统一测试框架
- ✅ `TemplateTestRunner` 类支持批量测试
- ✅ 消除测试代码重复

#### 自动化测试
- ✅ 创建 `tests/test_basic.py` pytest测试
- ✅ 使用Mock避免调用真实API
- ✅ 更新 `requirements.txt` 添加测试依赖

### P1 优化完成

#### 类型系统
- ✅ 创建 `scripts/types.py` 类型定义
- ✅ `TaskStatus`, `AspectRatio` 枚举
- ✅ `GenerationResult`, `PortInfo` 数据类

#### 配置管理
- ✅ 创建 `scripts/config_manager.py`
- ✅ `templates_data.json` 作为唯一数据源
- ✅ 消除 `api_ports.json` 重复

#### 架构重构
- ✅ 创建 `scripts/task_poller.py` 轮询组件
- ✅ 创建 `scripts/image_uploader.py` 上传组件
- ✅ 创建 `scripts/vivago_client_v2.py` 重构客户端

### P2 优化完成

#### 文档整合
- ✅ 创建 `docs/` 目录结构
- ✅ `docs/README.md` - 文档入口
- ✅ `docs/quickstart.md` - 快速开始
- ✅ `docs/architecture.md` - 架构设计
- ✅ `docs/api_reference.md` - API参考
- ✅ `docs/testing.md` - 测试指南
- ✅ `docs/troubleshooting.md` - 故障排查

#### 日志系统
- ✅ 创建 `scripts/logging_config.py`
- ✅ 统一的日志配置
- ✅ 支持文件和控制台输出

#### CI/CD
- ✅ 创建 `.github/workflows/ci.yml`
- ✅ Lint检查 (flake8, black)
- ✅ 类型检查 (mypy)
- ✅ 单元测试 (pytest)
- ✅ 代码覆盖率报告
- ✅ 创建 `.github/workflows/daily_test.yml`
- ✅ 每日定时模板测试

### 新增文件

```
scripts/
├── exceptions.py          # 异常体系 (P0)
├── config.py              # 配置管理 (P0)
├── types.py               # 类型定义 (P1)
├── config_manager.py      # 统一配置 (P1)
├── task_poller.py         # 任务轮询 (P1)
├── image_uploader.py      # 图片上传 (P1)
├── vivago_client_v2.py    # 重构客户端 (P1)
└── logging_config.py      # 日志配置 (P2)

tests/
├── framework.py           # 测试框架 (P0)
└── test_basic.py          # 基础测试 (P0)

docs/
├── README.md              # 文档入口 (P2)
├── quickstart.md          # 快速开始 (P2)
├── architecture.md        # 架构设计 (P2)
├── api_reference.md       # API参考 (P2)
├── testing.md             # 测试指南 (P2)
└── troubleshooting.md     # 故障排查 (P2)

.github/workflows/
├── ci.yml                 # CI工作流 (P2)
└── daily_test.yml         # 定时测试 (P2)

.env.example               # 环境变量模板 (P0)
.gitignore                 # Git忽略文件 (P0)
```

### 统计

- **P0**: 7个文件, 814行代码
- **P1**: 5个文件, 850+行代码
- **P2**: 10个文件, 2000+行文档和配置
- **总计**: 22个新文件, 3700+行

## [0.7.0] - 2026-03-06

### 新增
- 视频首尾帧 (Keyframe-to-Video) 功能
- v3L 端口支持
- 测试报告: 皮卡丘 → 柯基变身视频

## [0.6.0] - 2026-03-06

### 重构
- 图生图支持 Kling O1 和 Nano Banana 2
- 支持多图输入融合
- 图像编辑、AI肖像、虚拟试衣并入图生图

## [0.5.0] - 2026-03-06

### 新增
- Nano Banana 2 图生图（多图输入）
- `strength`, `relevance`, `image_guidance_scale` 参数

## [0.4.0] - 2026-03-05

### 新增
- 文生视频功能
- v3L / v3Pro / kling-video 端口

## [0.3.0] - 2026-03-05

### 新增
- Nano Banana 2 模型
- `display_name` 字段

## [0.2.0] - 2026-03-05

### 重构
- 层级架构（一级/二级端口）
- API端口配置系统

## [0.1.0] - 2026-03-05

### 初始版本
- 文生图功能（Kling O1）
