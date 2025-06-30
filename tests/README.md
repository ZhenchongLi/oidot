# 测试说明

本项目使用 pytest 进行测试。

## 安装测试依赖

```bash
uv sync --group dev
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_main.py
```

### 运行特定测试函数
```bash
pytest tests/test_main.py::TestMain::test_main_prints_hello_message
```

### 运行测试并显示覆盖率报告
```bash
pytest --cov=oidot --cov-report=html
```

### 跳过慢速测试
```bash
pytest -m "not slow"
```

### 只运行慢速测试
```bash
pytest -m "slow"
```

## 测试文件结构

- `conftest.py`: pytest 配置和共享 fixtures
- `test_main.py`: main 模块的测试
- `test_merge_docx.py`: merge_docx 模块的测试
- `data/`: 测试数据文件目录（如果需要）

## 测试标记

- `@pytest.mark.slow`: 标记为慢速测试
- `@pytest.mark.integration`: 标记为集成测试

## 覆盖率报告

运行测试后，覆盖率报告会生成在 `htmlcov/` 目录中。 