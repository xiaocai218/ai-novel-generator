"""
运行时配置路径管理

支持将用户配置写入持久化目录，避免 Docker 重建后丢失。
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)


def get_project_config_dir() -> Path:
    """获取项目内置配置目录。"""
    return Path(__file__).resolve().parents[2] / "config"


def get_runtime_config_dir() -> Path:
    """
    获取运行时配置目录。

    优先使用环境变量 `AINOVEL_CONFIG_DIR`，未设置时退回项目根目录下的 `config/`。
    """
    config_dir = Path(os.getenv("AINOVEL_CONFIG_DIR", "config"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file(filename: str, seed_from_project: bool = True) -> Path:
    """
    获取运行时配置文件路径，并在需要时从项目默认配置复制。

    Args:
        filename: 文件名
        seed_from_project: 文件不存在时，是否从项目默认配置复制
    """
    runtime_file = get_runtime_config_dir() / filename

    if runtime_file.exists() or not seed_from_project:
        return runtime_file

    project_file = get_project_config_dir() / filename
    if not project_file.exists():
        return runtime_file

    try:
        if project_file.resolve() != runtime_file.resolve():
            shutil.copy2(project_file, runtime_file)
            logger.info(f"[配置] 已初始化运行时配置: {runtime_file}")
    except FileNotFoundError:
        shutil.copy2(project_file, runtime_file)
        logger.info(f"[配置] 已初始化运行时配置: {runtime_file}")
    except Exception as e:
        logger.warning(f"[配置] 初始化运行时配置失败 {runtime_file}: {e}")

    return runtime_file


def ensure_runtime_config_files(filenames: Iterable[str]) -> None:
    """批量确保运行时配置文件存在。"""
    for filename in filenames:
        get_config_file(filename, seed_from_project=True)
