#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
典狱长数据查询系统
主程序入口
"""

from gui_app import GameDataGUI

def main():
    """主函数"""
    # 创建GUI应用
    gui = GameDataGUI()
    
    # 运行GUI
    gui.run()

if __name__ == "__main__":
    main()
