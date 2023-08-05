"""
文件操作模块
"""
import os


def get_ext(file_path):
    """
    获取文件的扩展名
    Args:
        file_path: str 文件名或文件路径

    Returns: str 返回扩展名

    """
    splits = os.path.splitext(file_path)
    return splits[1] if len(splits) == 2 else ''
