## 项目简介

本项目旨在提供一个访问本地某个路径下文件的 MCP 服务。

## 工具列表

| 工具名 | 功能描述 |
|--------|----------|
| `list_directory` | 列出指定目录下的文件和子目录 |
| `list_directory_recursive` | 递归列出目录下所有文件（忽略以 `.` 开头的文件夹） |
| `read_file` | 读取文件完整内容 |
| `get_file_info` | 获取文件元信息（大小、创建/修改/访问时间、权限等） |
| `read_file_head` | 读取文件前 N 行（默认 20 行） |
| `read_file_tail` | 读取文件后 N 行（默认 20 行） |
| `read_file_range` | 读取文件的指定行范围（1-indexed） |
| `search_in_file` | 在文件中搜索正则表达式匹配的行，返回行号和内容 |
| `count_lines` | 统计文件的行数、单词数、字符数 |
| `glob_files` | 使用 glob 模式查找文件（如 `*.py`、`**/*.md`） |

## 配置项

通过 `.env` 文件配置：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `KB_ROOT` | 允许访问的根目录路径 | 必填 |
| `MCP_PORT` | MCP 服务端口 | 必填 |
| `MCP_TRANSPORT` | 传输协议 (`stdio`/`sse`/`streamable-http`) | `stdio` |


## 项目管理

本项目使用 uv 管理 python

```bash
# 运行：
uv run main.py

# 安装包
uv add <package>
```