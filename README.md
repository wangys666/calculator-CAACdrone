# 科学计算器

面向CAAC无人机操控员考试，地面站部分的桌面计算工具，vibe coding的产物
基于 Python + Tkinter 实现。提供三角函数、三角形求解、风向航向修正三个常用计算模块。
暂未打包为exe，过两天会传上来，配置后也可自行打包。

## 功能模块

### 三角函数
计算 sin / cos / tan / cot / sec / csc 及其反函数，支持角度 / 弧度切换。

### 三角形求解
输入任意 3 个已知量（至少含 1 条边），自动求出剩余 3 个量及面积。支持以下配置：

| 配置 | 输入 | 求解依据 |
|------|------|----------|
| SSS | 三边 | 余弦定理 |
| SAS | 两边及夹角 | 余弦定理 |
| ASA | 两角及夹边 | 正弦定理 |
| AAS | 两角及非夹边 | 正弦定理 |
| SSA | 两边及一对角 | 正弦定理（含歧义解判别） |

### 风向航向
输入航线角 (TC) 与风向 (WD)，识别 8 种偏流情况（逆风、顺风、左右前/侧/后侧风），给出推荐的航向修正角 (WCA)。

## 目录结构

```
.
├── main.py              # 入口
├── app.py               # 主窗口
├── engine/              # 计算引擎
│   ├── triangle_engine.py
│   ├── wind_engine.py
│   └── utils.py
├── ui/                  # 界面层
│   ├── trig_tab.py
│   ├── triangle_tab.py
│   ├── wind_tab.py
│   └── widgets.py
├── tests/               # 单元测试
│   └── test_ssa.py
└── dist/                # 打包产物（可选）
    └── 科学计算器.exe（更新中暂未上传）
```

## 环境依赖

- **Python**: 3.8 及以上
- **标准库**: `math`、`tkinter`（GUI）
- **第三方库**: 运行时无第三方依赖；打包成 exe 时需要 `pyinstaller`

依赖清单见 [`requirements.txt`](./requirements.txt)。

## 环境安装

### 1. 安装 Python

- **Windows / macOS**: 从 [python.org](https://www.python.org/downloads/) 下载安装包，安装时勾选 "Add Python to PATH"。
- **macOS (Homebrew)**: `brew install python-tk`（自带 tkinter）
- **Ubuntu / Debian**: `sudo apt install python3 python3-tk`
- **Fedora**: `sudo dnf install python3 python3-tkinter`

验证 tkinter 可用：

```bash
python -m tkinter
```

弹出测试窗口即表示安装成功。

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> 仅运行程序的话可跳过此步，本项目运行时不依赖任何第三方包。

## 运行

```bash
python main.py
```

## 测试

```bash
python -m unittest discover tests
```

测试覆盖 SSA 的 6 种边角组合、歧义双解、无解、退化等边界情况。

## 打包

使用 PyInstaller 生成单文件可执行程序：

```bash
pyinstaller --onefile --windowed --name 科学计算器 main.py
```

产物位于 `dist/`。
