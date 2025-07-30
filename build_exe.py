import os
import subprocess
import sys

def build_exe():
    """打包GUI程序为exe文件"""
    print("开始打包程序...")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 创建spec文件
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'flask',
        'sqlite3',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'webbrowser',
        'threading',
        'socket',
        're',
        'time',
        'os',
        'sys'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='游戏数据查询系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    # 写入spec文件
    with open('game_query.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("spec文件已创建")
    
    # 执行打包命令
    print("开始执行PyInstaller...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "--clean", 
            "--onefile", 
            "--windowed",
            "--name=游戏数据查询系统",
            "gui_main.py"
        ])
        print("打包完成！")
        print("exe文件位置: dist/游戏数据查询系统.exe")
        
        # 创建使用说明
        create_readme()
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False
    
    return True

def create_readme():
    """创建使用说明"""
    readme_content = '''# 游戏数据查询系统 - 使用说明

## 程序功能
这是一个游戏数据查询系统，可以查询怪物爆率、地图信息等游戏数据。

## 使用方法

### 1. 启动程序
双击运行 "游戏数据查询系统.exe"

### 2. 配置设置
- **服务端根目录**: 点击"浏览"按钮选择游戏服务端的根目录
- **端口号**: 设置Web服务器端口（默认8080）

### 3. 初始化数据
点击"初始化数据"按钮，程序会：
- 检查必需文件是否存在
- 读取Config.ini中的服务端名称
- 解析MapInfo.txt中的地图映射
- 解析MonItems目录中的怪物爆出物品
- 解析MonGen.txt中的怪物刷新信息
- 创建数据库并存储所有数据

### 4. 启动服务器
数据初始化成功后，点击"启动服务器"按钮启动Web服务器

### 5. 访问查询界面
- 点击"打开浏览器"按钮自动打开查询界面
- 或手动在浏览器中访问: http://localhost:端口号

## 查询功能

### 地图查询
- 查看所有地图列表
- 点击地图查看该地图的怪物刷新信息
- 点击怪物查看其爆出物品

### 怪物查询
- 查看所有怪物列表
- 点击怪物查看其爆出物品和出现地图
- 点击物品查看爆出该物品的其他怪物

### 物品查询
- 查看所有物品列表
- 点击物品查看爆出该物品的怪物列表
- 点击怪物查看其出现地图

## 文件要求

程序需要以下文件存在于服务端根目录：
```
服务端根目录/
├── Config.ini                    # 配置文件（包含GameName）
└── Mir200/
    ├── M2Data/                   # 数据库目录（自动创建）
    ├── Envir/
    │   ├── MonItems/            # 怪物爆出物品目录
    │   ├── MonGen.txt           # 怪物刷新配置
    │   └── MapInfo.txt          # 地图信息配置
    └── sqlite3.dll              # SQLite动态库
```

## 注意事项
1. 确保服务端根目录下有完整的游戏文件
2. 端口号不要与其他程序冲突
3. 程序会自动创建数据库文件
4. 支持多个服务端同时运行（使用不同端口）

## 技术支持
如有问题，请检查：
1. 文件路径是否正确
2. 端口是否被占用
3. 防火墙设置
4. 程序日志输出
'''
    
    with open('使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("使用说明已创建: 使用说明.txt")

if __name__ == "__main__":
    build_exe() 