"""MCP tools for file system operations."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量获取根目录
KB_ROOT = os.getenv("KB_ROOT")


def list_directory(relative_path: str = "") -> list[dict]:
    """
    列出指定目录下的文件和子目录。

    Args:
        relative_path: 相对于根目录的路径，为空则列出根目录

    Returns:
        包含文件和目录信息的字典列表
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    # 构建完整路径
    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path if relative_path else base_path

    # 验证路径安全性（确保在根目录内）
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"Path does not exist: {relative_path}")

    if not resolved_target.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {relative_path}")

    result = []
    for item in sorted(resolved_target.iterdir()):
        result.append({
            "name": item.name,
            "path": str(item.relative_to(base_path)),
            "type": "directory" if item.is_dir() else "file",
        })

    return result


def get_root_path() -> str:
    """获取当前配置的根目录路径。"""
    return KB_ROOT


def list_directory_recursive(relative_path: str = "") -> list[dict]:
    """
    递归列出目录下所有文件（忽略以 . 开头的文件夹）。

    Args:
        relative_path: 相对于根目录的路径，为空则从根目录开始

    Returns:
        包含所有文件信息的字典列表
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path if relative_path else base_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"Path does not exist: {relative_path}")

    if not resolved_target.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {relative_path}")

    result = []

    def scan_directory(path: Path):
        for item in sorted(path.iterdir()):
            # 跳过以 . 开头的文件夹和文件
            if item.name.startswith("."):
                continue
            if item.is_dir():
                result.append({
                    "name": item.name,
                    "path": str(item.relative_to(base_path)),
                    "type": "directory",
                })
                scan_directory(item)
            else:
                result.append({
                    "name": item.name,
                    "path": str(item.relative_to(base_path)),
                    "type": "file",
                })

    scan_directory(resolved_target)
    return result

def read_file(relative_path: str) -> str:
    """
    读取文件内容。

    Args:
        relative_path: 相对于根目录的文件路径

    Returns:
        文件内容
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    return resolved_target.read_text(encoding="utf-8")


def get_file_info(relative_path: str) -> dict:
    """
    获取文件的元信息（大小、创建时间、修改时间、权限等）。

    Args:
        relative_path: 相对于根目录的文件路径

    Returns:
        包含文件元信息的字典
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    stat = resolved_target.stat()
    return {
        "name": resolved_target.name,
        "path": str(resolved_target.relative_to(base_path)),
        "size_bytes": stat.st_size,
        "size_human": _format_size(stat.st_size),
        "is_directory": False,
        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "accessed_time": datetime.fromtimestamp(stat.st_atime).isoformat(),
        "permissions": _format_permissions(resolved_target),
    }


def read_file_head(relative_path: str, lines: int = 20) -> str:
    """
    读取文件的前几行。

    Args:
        relative_path: 相对于根目录的文件路径
        lines: 要读取的行数，默认 20 行

    Returns:
        文件前 N 行的内容
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    with open(resolved_target, 'r', encoding='utf-8') as f:
        head_lines = []
        for i, line in enumerate(f):
            if i >= lines:
                break
            head_lines.append(line.rstrip('\n\r'))

    return '\n'.join(head_lines)


def read_file_tail(relative_path: str, lines: int = 20) -> str:
    """
    读取文件的后几行。

    Args:
        relative_path: 相对于根目录的文件路径
        lines: 要读取的行数，默认 20 行

    Returns:
        文件后 N 行的内容
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    # 读取文件最后 N 行
    with open(resolved_target, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    tail_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
    return ''.join([line.rstrip('\n\r') for line in tail_lines])


def search_in_file(relative_path: str, pattern: str, case_sensitive: bool = False) -> list[dict]:
    """
    在文件中搜索匹配特定模式的行。

    Args:
        relative_path: 相对于根目录的文件路径
        pattern: 要搜索的模式（支持正则表达式）
        case_sensitive: 是否区分大小写，默认 False

    Returns:
        匹配行的列表，每项包含行号和内容
    """
    import re

    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    flags = 0 if case_sensitive else re.IGNORECASE
    regex = re.compile(pattern, flags)

    matches = []
    with open(resolved_target, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if regex.search(line):
                matches.append({
                    "line_number": i,
                    "content": line.rstrip('\n\r'),
                })

    return matches


def count_lines(relative_path: str) -> dict:
    """
    统计文件的行数、单词数和字符数。

    Args:
        relative_path: 相对于根目录的文件路径

    Returns:
        包含统计信息的字典
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    with open(resolved_target, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    words = content.split()

    return {
        "path": str(resolved_target.relative_to(base_path)),
        "lines": len(lines),
        "words": len(words),
        "characters": len(content),
    }


def read_file_range(relative_path: str, start_line: int = 1, end_line: Optional[int] = None) -> dict:
    """
    读取文件的指定行范围。

    Args:
        relative_path: 相对于根目录的文件路径
        start_line: 起始行号（从 1 开始）
        end_line: 结束行号（包含），如果为 None 则读取到文件末尾

    Returns:
        包含行范围内容的字典
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    target_path = base_path / relative_path

    # 验证路径安全性
    resolved_target = target_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_target.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_target.exists():
        raise FileNotFoundError(f"File does not exist: {relative_path}")

    if resolved_target.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {relative_path}")

    with open(resolved_target, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()

    # 确保索引正确（转换为 0-based）
    start_idx = max(0, start_line - 1)
    if end_line is None:
        end_idx = len(all_lines)
    else:
        end_idx = min(len(all_lines), end_line)

    if start_idx >= end_idx:
        return {
            "path": str(resolved_target.relative_to(base_path)),
            "start_line": start_line,
            "end_line": end_line if end_line else len(all_lines),
            "content": "",
            "total_lines": len(all_lines),
        }

    selected_lines = all_lines[start_idx:end_idx]
    content = ''.join([line.rstrip('\n\r') for line in selected_lines])

    return {
        "path": str(resolved_target.relative_to(base_path)),
        "start_line": start_line,
        "end_line": end_line if end_line else len(all_lines),
        "content": content,
        "total_lines": len(all_lines),
    }


def _format_size(size_bytes: int) -> str:
    """格式化文件大小为人类可读格式。"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def _format_permissions(path: Path) -> str:
    """格式化文件权限。"""
    import stat
    st = path.stat()
    mode = st.st_mode

    perms = []
    perms.append('d' if path.is_dir() else '-')
    perms.append('r' if mode & stat.S_IRUSR else '-')
    perms.append('w' if mode & stat.S_IWUSR else '-')
    perms.append('x' if mode & stat.S_IXUSR else '-')
    perms.append('r' if mode & stat.S_IRGRP else '-')
    perms.append('w' if mode & stat.S_IWGRP else '-')
    perms.append('x' if mode & stat.S_IXGRP else '-')
    perms.append('r' if mode & stat.S_IROTH else '-')
    perms.append('w' if mode & stat.S_IWOTH else '-')
    perms.append('x' if mode & stat.S_IXOTH else '-')

    return ''.join(perms)


def glob_files(pattern: str = "**/*", relative_path: str = "") -> list[dict]:
    """
    使用 glob 模式查找文件。

    Args:
        pattern: glob 模式，例如 "*.py", "**/*.md", "src/**/*.py"
        relative_path: 相对于根目录的搜索起始路径，为空则从根目录开始

    Returns:
        匹配的文件列表
    """
    if not KB_ROOT:
        raise ValueError("KB_ROOT environment variable not set")

    base_path = Path(KB_ROOT)
    search_path = base_path / relative_path if relative_path else base_path

    # 验证路径安全性
    resolved_search = search_path.resolve()
    resolved_base = base_path.resolve()

    if not resolved_search.is_relative_to(resolved_base):
        raise PermissionError("Access outside root directory is not allowed")

    if not resolved_search.exists():
        raise FileNotFoundError(f"Path does not exist: {relative_path}")

    if not resolved_search.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {relative_path}")

    # 处理 pattern，确保在相对路径下正确匹配
    if relative_path:
        # 如果有相对路径，需要调整 pattern
        glob_pattern = f"{relative_path}/{pattern}" if not pattern.startswith("/") else pattern
    else:
        glob_pattern = pattern

    result = []
    for item in sorted(base_path.glob(glob_pattern)):
        # 跳过目录
        if item.is_file():
            result.append({
                "name": item.name,
                "path": str(item.relative_to(base_path)),
                "type": "file",
            })

    return result


if __name__ == "__main__":
    # 测试列出根目录
    try:
        files = list_directory()
        for f in files:
            print(f)
    except Exception as e:
        print(f"Error: {e}")