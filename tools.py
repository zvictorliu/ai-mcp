"""MCP tools for file system operations."""

import os
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


if __name__ == "__main__":
    # 测试列出根目录
    try:
        files = list_directory()
        for f in files:
            print(f)
    except Exception as e:
        print(f"Error: {e}")