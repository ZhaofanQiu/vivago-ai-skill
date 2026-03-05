# Testing Guide

## Quick Start

```bash
# Run all enabled tests
python tests/test_suite.py

# Run specific test
python tests/test_suite.py --test txt2img_basic

# Run with custom config
python tests/test_suite.py --config tests/my_config.json
```

## Test Configuration

Edit `tests/test_config.json` to:
- Enable/disable specific tests
- Change API endpoints
- Adjust timeout settings

## Test Cases

| Test Name | Description | Priority |
|-----------|-------------|----------|
| txt2img_basic | Basic text-to-image | P0 |
| txt2img_batch | Batch generation | P1 |
| txt2img_ratios | Different aspect ratios | P1 |
| api_error_handling | Error handling | P0 |

## Adding New Tests

1. Add test method to `TestSuite` class:
```python
def test_my_feature(self, result: TestResult):
    result.response_data = {...}
```

2. Add to test_config.json:
```json
"my_feature": {
  "enabled": true,
  "priority": "P1",
  "description": "My feature test"
}
```

## Continuous Integration

Run tests before each commit:
```bash
#!/bin/bash
# pre-commit hook
python tests/test_suite.py
if [ $? -ne 0 ]; then
  echo "Tests failed, commit aborted"
  exit 1
fi
```
