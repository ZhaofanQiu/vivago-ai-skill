#!/usr/bin/env python3
"""
日志配置
提供统一的日志设置
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    设置日志配置
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        log_file: 日志文件路径（可选）
        format_string: 自定义格式（可选）
        
    Returns:
        配置好的logger
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 创建formatter
    formatter = logging.Formatter(format_string)
    
    # 获取根logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # 清除现有handlers
    logger.handlers.clear()
    
    # 添加控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 添加文件handler（如果指定）
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的logger
    
    Args:
        name: logger名称，通常用 __name__
        
    Returns:
        logger实例
    """
    return logging.getLogger(name)


# 默认日志配置
default_setup = lambda: setup_logging(
    level=logging.INFO,
    format_string='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
