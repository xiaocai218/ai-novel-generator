"""
生成参数配置模块 - 支持场景化参数配置

版权所有 © 2026 新疆幻城网安科技有限责任公司 (幻城科技)
作者：幻城
"""

import json
from typing import Dict, Any

from .runtime_paths import get_config_file

# 配置文件路径
CONFIG_FILE = get_config_file("generation_config.json")


def load_generation_config() -> Dict[str, Any]:
    """
    加载生成配置文件
    
    Returns:
        配置字典
    """
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_generation_params(scene_type: str = "default") -> Dict[str, Any]:
    """
    获取指定场景的生成参数
    
    Args:
        scene_type: 场景类型 (default, dialogue, narrative, description)
        
    Returns:
        该场景的生成参数字典
    """
    config = load_generation_config()
    scene_params = config.get("scene_params", {})
    
    # 如果场景存在则返回场景配置，否则返回default配置
    if scene_type in scene_params:
        return scene_params[scene_type]
    
    # 兜底返回default配置
    return scene_params.get("default", {
        "temperature": config.get("temperature", 0.75),
        "top_p": config.get("top_p", 0.9),
        "frequency_penalty": config.get("frequency_penalty", 0.3),
        "presence_penalty": config.get("presence_penalty", 0.2)
    })


def get_base_generation_params() -> Dict[str, Any]:
    """
    获取基础生成参数（不含场景化配置）
    
    Returns:
        基础生成参数字典
    """
    config = load_generation_config()
    
    return {
        "temperature": config.get("temperature", 0.75),
        "top_p": config.get("top_p", 0.9),
        "top_k": config.get("top_k", 50),
        "max_tokens": config.get("max_tokens", 20000),
        "frequency_penalty": config.get("frequency_penalty", 0.3),
        "presence_penalty": config.get("presence_penalty", 0.2)
    }


def get_all_scene_types() -> list:
    """
    获取所有可用的场景类型
    
    Returns:
        场景类型列表
    """
    config = load_generation_config()
    scene_params = config.get("scene_params", {})
    return list(scene_params.keys())
