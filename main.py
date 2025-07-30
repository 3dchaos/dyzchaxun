#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
典狱长数据查询系统
主程序入口
"""

import os
import sys
import time
import tkinter as tk
from tkinter import messagebox
from gui_app import GameDataGUI

def check_single_instance():
    """检查程序是否已经在运行"""
    # 创建锁文件路径
    lock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.lock")
    
    try:
        # 尝试创建锁文件
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        return True, lock_file
    except:
        # 如果无法创建锁文件，说明程序已在运行
        return False, lock_file

def cleanup_lock_file(lock_file):
    """清理锁文件"""
    try:
        if os.path.exists(lock_file):
            os.remove(lock_file)
    except:
        pass

def main():
    """主函数"""
    # 检查程序唯一性
    can_run, lock_file = check_single_instance()
    
    if not can_run:
        # 创建临时窗口显示提示
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 显示错误消息
        messagebox.showerror(
            "程序已在运行", 
            "典狱长数据查询系统已经在运行中！\n\n请关闭已运行的程序后再试。"
        )
        
        root.destroy()
        sys.exit(1)
    
    try:
        # 创建GUI应用
        gui = GameDataGUI()
        
        # 运行GUI
        gui.run()
    finally:
        # 程序结束时清理锁文件
        cleanup_lock_file(lock_file)

if __name__ == "__main__":
    main()
