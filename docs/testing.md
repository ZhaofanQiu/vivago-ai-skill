# 测试指南

## 运行测试

### 安装测试依赖

```bash
pip install -r requirements.txt
```

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试

```bash
# 只运行基础测试
pytest tests/test_basic.py -v

# 运行特定测试函数
pytest tests/test_basic.py::TestVivagoClient::test_client_initialization -v
```

### 生成覆盖率报告

```bash
pytest tests/ --cov=scripts --cov-report=html
# 报告生成在 htmlcov/ 目录
```

## 测试结构

```
tests/
├── test_basic.py       # 基础单元测试（使用Mock）
├── framework.py        # 测试框架
└── fixtures/           # 测试数据（待创建）
```

## 测试类型

### 1. 单元测试 (test_basic.py)

使用Mock，不调用真实API：

```python
def test_client_initialization():
    """测试客户端初始化"""
    client = VivagoClient(token='test_token')
    assert client.token == 'test_token'
```

**特点**:
- ✅ 快速（秒级）
- ✅ 不消耗Credits
- ✅ 不依赖网络
- ✅ 可离线运行

### 2. 集成测试 (framework.py)

调用真实API：

```python
from tests.framework import quick_test

# 测试单个模板
result = quick_test('ghibli', image_uuid='j_xxx')
```

**特点**:
- ⚠️ 慢（分钟级）
- ⚠️ 消耗Credits
- ⚠️ 需要网络
- ⚠️ 可能不稳定

**运行前确保**:
```bash
export HIDREAM_TOKEN="your_token"
export STORAGE_AK="your_ak"
export STORAGE_SK="your_sk"
export TEST_IMAGE_UUID="j_xxx"  # 测试用的图片UUID
```

## 编写测试

### 基础测试模板

```python
import pytest
from scripts.vivago_client import create_client

class TestMyFeature:
    def test_success_case(self):
        """测试正常情况"""
        client = create_client()
        result = client.some_method()
        assert result is not None
    
    def test_error_case(self):
        """测试错误情况"""
        with pytest.raises(ValueError):
            client.some_method(invalid_param=True)
```

### 使用Mock

```python
from unittest.mock import patch, MagicMock

@patch('scripts.vivago_client.requests.post')
def test_api_call(mock_post):
    """Mock API调用"""
    mock_post.return_value = MagicMock(
        json=lambda: {'code': 0, 'result': {'task_id': 'test'}},
        raise_for_status=lambda: None
    )
    
    result = client.text_to_image(prompt="test")
    assert result['code'] == 0
```

### 使用测试框架

```python
from tests.framework import TemplateTestRunner

# 批量测试
runner = TemplateTestRunner(image_uuid='j_xxx')

results = runner.test_batch([
    'ghibli',
    'iron_man',
    'angel_wings'
])

# 生成报告
report_path = runner.save_report()
print(f"报告已保存: {report_path}")
```

## 持续集成

GitHub Actions 配置（见 `.github/workflows/ci.yml`）:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=scripts
```

## 测试数据

### 测试图片

放在 `tests/fixtures/`:

```
tests/fixtures/
├── test_photo.jpg      # 人像照片
├── test_landscape.jpg  # 风景
└── test_product.jpg    # 产品
```

### Mock响应

```python
# tests/fixtures/mock_responses.py
TEXT_TO_IMAGE_RESPONSE = {
    "code": 0,
    "result": {
        "task_id": "mock_task_123"
    }
}
```

## 调试测试

```bash
# 详细输出
pytest tests/ -v -s

# 遇到第一个失败就停止
pytest tests/ -x

# 只运行上次失败的测试
pytest tests/ --lf

# 使用pdb调试
pytest tests/ --pdb
```

## 性能测试

```python
import time

def test_performance():
    """测试性能"""
    start = time.time()
    client.text_to_image(prompt="test")
    elapsed = time.time() - start
    
    assert elapsed < 5.0  # 应该在5秒内完成
```
