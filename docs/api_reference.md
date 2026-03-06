# API参考

## VivagoClient

### 初始化

```python
from scripts.vivago_client import create_client

# 从环境变量读取凭证
client = create_client()

# 或者显式传入
client = create_client(
    token="your_token",
    storage_ak="your_ak",
    storage_sk="your_sk"
)
```

### 文生图 (text_to_image)

```python
results = client.text_to_image(
    prompt="描述文本",           # 必需
    port="kling-image",          # 可选，默认kling-image
    wh_ratio="1:1",              # 可选，默认1:1
    batch_size=1,                # 可选，默认1，范围1-4
    style="default",             # 可选
    seed=-1                      # 可选，随机种子
)
```

**参数说明**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| prompt | str | ✅ | 图像描述 |
| port | str | ❌ | 模型端口 |
| wh_ratio | str | ❌ | 宽高比 |
| batch_size | int | ❌ | 生成数量 |
| style | str | ❌ | 风格 |
| seed | int | ❌ | 随机种子 |

**wh_ratio选项**: "1:1", "16:9", "9:16", "4:3", "3:4"

**port选项**: "kling-image", "hidream-txt2img", "nano-banana"

**返回**:
```python
[
    {
        "task_id": "uuid",
        "task_status": 1,
        "result": ["url1", "url2"]
    }
]
```

### 图生视频 (image_to_video)

```python
results = client.image_to_video(
    prompt="视频描述",           # 必需
    image_uuid="j_xxxx",         # 必需，图片UUID
    port="v3Pro",                # 可选，默认v3Pro
    wh_ratio="1:1",              # 可选
    duration=5,                  # 可选，默认5，可选5或10
    mode="Slow"                  # 可选，默认Slow，可选Fast/Slow
)
```

**参数说明**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| prompt | str | ✅ | 视频描述 |
| image_uuid | str | ✅ | 图片UUID |
| port | str | ❌ | 模型端口 |
| wh_ratio | str | ❌ | 宽高比 |
| duration | int | ❌ | 时长(秒) |
| mode | str | ❌ | 模式 |

**port选项**: "v3Pro", "v3L", "kling-video"

### 视频模板 (template_to_video)

```python
results = client.template_to_video(
    image_uuid="j_xxxx",         # 必需
    template="ghibli",           # 必需，模板ID
    wh_ratio="1:1"               # 可选
)
```

**热门模板**:

| 模板ID | 说明 |
|--------|------|
| ghibli | 吉卜力风格 |
| iron_man | 钢铁侠装甲 |
| angel_wings | 天使翅膀 |
| magic_reveal_ravenclaw | 拉文克劳魔法 |
| renovation_of_old_photos | 老照片修复 |

查看所有模板：
```python
from scripts.template_manager import get_template_manager

manager = get_template_manager()
templates = manager.list_templates()
for tid, name in templates.items():
    print(f"{tid}: {name}")
```

### 图片上传 (upload_image)

```python
image_uuid = client.upload_image(
    "/path/to/image.jpg"    # 本地图片路径
)
# 返回: "j_xxxxx"
```

**自动处理**:
- 压缩到1024px
- JPEG格式
- 最大5MB

## 任务状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 0 | 等待中 | 任务已提交 |
| 1 | 已完成 | 可以获取结果 |
| 2 | 处理中 | 正在生成 |
| 3 | 失败 | 生成失败 |
| 4 | 被拒绝 | 内容审核未通过 |

## 异常处理

```python
from scripts.exceptions import (
    TaskFailedError,
    TaskRejectedError,
    NetworkError
)

try:
    results = client.text_to_image(prompt="test")
except TaskRejectedError as e:
    print(f"内容被拒绝: {e.reason}")
except TaskFailedError as e:
    print(f"任务失败: {e.reason}")
except NetworkError as e:
    print(f"网络错误: {e}")
```

## 高级用法

### 批量生成

```python
# 一次生成4张图
results = client.text_to_image(
    prompt="风景",
    batch_size=4
)
```

### 自定义轮询

```python
from scripts.task_poller import TaskPoller

poller = TaskPoller(client, max_attempts=30, retry_delay=5)

result = poller.poll(
    task_id="xxx",
    result_endpoint="/v3/video/...",
    on_progress=lambda attempt, max: print(f"{attempt}/{max}"),
    on_complete=lambda data: print("完成！"),
    on_fail=lambda err: print(f"失败: {err}")
)
```

### 使用V2客户端

```python
from scripts.vivago_client_v2 import create_client_v2

client = create_client_v2()
# API与V1相同，但内部架构更优
results = client.text_to_image(prompt="test")
```
