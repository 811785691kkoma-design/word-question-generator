# 单词题目生成工具

一个基于Streamlit的单词题目生成应用，用于快速生成单词选择题。

## 功能特点

- 支持上传包含'单词'和'中文翻译'两列的Excel文件
- 可自定义题目数量和选项数量
- 自动生成随机打乱的选项
- 确保每个单词至少出现一次作为正确答案（当题目数量不小于单词数量时）
- 提供题目预览功能
- 支持导出为Excel文件

## 如何使用

1. 准备一个包含'单词'和'中文翻译'两列的Excel文件
2. 上传文件
3. 设置题目数量和选项数量
4. 点击'生成题目'按钮
5. 查看预览并下载生成的题目文件

## 技术栈

- Python 3.9+
- Streamlit
- Pandas
- OpenPyXL

## 本地运行

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run word_question_generator.py
```

## 部署到Streamlit Cloud

1. 将代码推送到GitHub仓库
2. 访问[Streamlit Cloud](https://share.streamlit.io/)
3. 登录并点击'New app'
4. 选择你的GitHub仓库
5. 选择主分支和主文件（word_question_generator.py）
6. 点击'Deploy'

## 文件结构

```
.
├── word_question_generator.py  # 主应用文件
├── requirements.txt            # 依赖列表
├── .gitignore                  # Git忽略文件
└── README.md                   # 项目说明
```

## 注意事项

- 确保Excel文件的表头包含'单词'和'中文翻译'两列
- 选项数量不能大于单词数量
- 当题目数量少于单词数量时，可能无法保证每个单词至少出现一次作为正确答案
