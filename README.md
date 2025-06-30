# DOCX解析工具

一个用于提取DOCX文件中文本内容并合成文本文件的Python工具。

## 功能特性

- 🔍 **文本提取**: 从DOCX文件中提取纯文本内容
- 📝 **格式保留**: 可选择保留基本格式（如标题）
- 💾 **文件输出**: 将提取的文本保存为TXT文件
- 🖥️ **控制台输出**: 支持在控制台显示提取的文本
- 🛡️ **错误处理**: 完善的错误处理和验证机制

## 安装依赖

```bash
# 使用uv安装依赖
uv sync

# 或者使用pip安装
pip install python-docx lxml
```

## 使用方法

### 命令行使用

```bash
# 基本使用 - 提取文本并保存为同名.txt文件
python docx_parser.py document.docx

# 指定输出文件
python docx_parser.py document.docx -o output.txt

# 保留格式（标题等）
python docx_parser.py document.docx -f

# 在控制台显示提取的文本
python docx_parser.py document.docx -p

# 组合使用
python docx_parser.py document.docx -f -p -o formatted_output.txt
```

### 命令行参数

- `docx_file`: 要解析的DOCX文件路径（必需）
- `-o, --output`: 输出文本文件路径（可选）
- `-f, --format`: 保留基本格式（标题等）
- `-p, --print`: 在控制台打印提取的文本

### 编程使用

```python
from docx_parser import DocxParser

# 创建解析器
parser = DocxParser("document.docx")

# 提取纯文本
text = parser.extract_text()
print(text)

# 提取带格式的文本
formatted_text = parser.extract_text_with_formatting()
print(formatted_text)

# 保存到文件
output_file = parser.save_to_text_file()
print(f"文本已保存到: {output_file}")

# 保存带格式的文本到指定文件
output_file = parser.save_to_text_file(
    output_path="output.txt",
    preserve_formatting=True
)
```

## 示例

运行示例代码：

```bash
python example.py
```

## 工作原理

1. **文件验证**: 检查文件是否存在且为DOCX格式
2. **ZIP解压**: DOCX文件本质上是ZIP压缩包
3. **XML解析**: 提取`word/document.xml`中的文本内容
4. **文本处理**: 根据需求提取纯文本或保留格式
5. **文件输出**: 将处理后的文本保存为TXT文件

## 支持的格式

- ✅ 纯文本提取
- ✅ 段落分隔
- ✅ 标题识别（Heading样式）
- ✅ UTF-8编码支持

## 错误处理

工具会处理以下常见错误：

- 文件不存在
- 非DOCX格式文件
- 损坏的DOCX文件
- XML解析错误
- 编码问题

## 项目结构

```
oidot/
├── docx_parser.py      # 主要解析工具
├── example.py          # 使用示例
├── main.py            # 项目入口
├── pyproject.toml     # 项目配置
└── README.md          # 说明文档
```

## 依赖包

- `python-docx`: DOCX文件处理
- `lxml`: XML解析
- `pathlib`: 路径处理
- `argparse`: 命令行参数解析

## 许可证

MIT License
