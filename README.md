# 游戏数据查询系统

这是一个用于查询游戏怪物、物品和地图数据的Web系统。

## 系统要求

1. Python 3.7+
2. Flask 框架
3. 必需的文件和目录结构

## 必需的文件结构

```
程序目录/
├── main.py                    # 主程序文件
├── requirements.txt           # Python依赖
├── sqlite3.dll              # SQLite3动态库文件
├── MonGen.txt               # 怪物刷新配置文件（ANSI编码）
└── Envir/
    └── MonItems/            # 怪物爆出物品目录
        ├── 怪物1.txt        # 怪物1的爆出物品文件
        ├── 怪物2.txt        # 怪物2的爆出物品文件
        └── ...              # 更多怪物文件
```

## 文件格式说明

### MonGen.txt 格式
每行格式：`地图名 X坐标 Y坐标 怪物名 范围 数量 刷新时间(分钟) [国家] [颜色]`
示例：`FOX02 277 205 红狐狸 400 300 15`

### 怪物爆出物品文件格式
文件名：`怪物名.txt`（ANSI编码）
内容格式：`概率 物品名`
示例：
```
1/10 祈祷之刃
1/100 龙纹剑
; 这是注释行
```

## 安装和运行

1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 准备数据文件：
   - 确保服务端目录结构正确：
     - `服务端根目录/Mir200/Envir/MonGen.txt`
     - `服务端根目录/Mir200/Envir/MonItems/`
     - `服务端根目录/Mir200/sqlite3.dll`

3. 运行程序：
```bash
python main.py
```

4. 按提示输入服务端根目录路径

5. 在浏览器中访问：`http://localhost:8858`

## 功能特性

### 地图查询
- 显示所有地图列表
- 点击地图查看该地图的怪物刷新信息
- 支持搜索功能

### 怪物查询
- 显示所有怪物列表
- 点击怪物查看爆出物品和出现地图
- 显示爆出概率
- 支持搜索功能

### 物品查询
- 显示所有物品列表
- 点击物品查看爆出该物品的怪物
- 显示爆出概率
- 支持搜索功能

## 系统流程

1. **端口检测**：检查8858端口是否被占用，如果被占用会提示用户输入新端口
2. **文件检查**：验证必需的文件和目录是否存在
3. **数据库创建**：在M2Data目录下创建dyzSearch.DB数据库
4. **数据解析**：读取并解析MonGen.txt和MonItems目录下的所有文件
5. **Web服务**：启动Flask Web服务器，提供查询界面

## 数据库结构

### Map表
- id: 主键
- map_name: 地图名
- x, y: 坐标
- monster_name: 怪物名
- range_val: 范围
- count: 数量
- refresh_time: 刷新时间
- country: 国家
- color: 颜色

### MonItems表
- id: 主键
- monster_name: 怪物名
- item_name: 物品名
- probability: 概率字符串
- rate_numerator: 分子
- rate_denominator: 分母

### Item表
- id: 主键
- item_name: 物品名（唯一）

## 注意事项

1. 所有文本文件必须使用ANSI编码（GBK）
2. 确保sqlite3.dll文件在程序目录下
3. 程序会自动创建M2Data目录和数据库文件
4. 如果端口被占用，程序会提示输入新端口号
5. 支持注释行（以";"开头）和空行 