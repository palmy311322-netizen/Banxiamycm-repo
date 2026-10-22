#!/usr/bin/env python3
"""每日学习督促助手 — 命令行入口"""
import sys
from pathlib import Path

# 确保项目根目录在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent))

from helper.cli import main

if __name__ == "__main__":
    main()
