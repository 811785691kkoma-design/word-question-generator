import streamlit as st
import pandas as pd
import os
import sys
import tempfile

# 导入现有的题目生成模块
sys.path.append('/Users/chandlerq/Desktop')
from question_generator import generate_questions, export_questions

# 修改版的读取函数，支持Streamlit上传的文件对象
def read_word_list_streamlit(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # 调试信息：打印实际读取到的列名
        print(f"实际读取到的列名：{list(df.columns)}")
        
        # 移除列名中的空格和可能的隐藏字符
        df.columns = [col.strip() for col in df.columns]
        
        # 再次打印处理后的列名
        print(f"处理后的列名：{list(df.columns)}")
        
        # 确保文件有正确的表头（不区分大小写）
        columns_lower = [col.lower() for col in df.columns]
        has_word = '单词' in df.columns or 'word' in columns_lower
        has_translation = '中文翻译' in df.columns or 'translation' in columns_lower or '中文' in columns_lower
        
        if not has_word or not has_translation:
            raise ValueError(f"Excel文件缺少必要的表头：'单词'或'中文翻译'。实际读取到的列：{list(df.columns)}")
        
        return df
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return str(e)

# 设置页面配置
st.set_page_config(
    page_title="单词题目生成工具",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题
st.title("📝 单词题目生成工具")

# 添加CSS样式
st.markdown("""
    <style>
    /* 生成题目按钮 - 醒目样式 */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        background-color: #8B0000 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 18px 35px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(139, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
        z-index: 10 !important;
        outline: none !important;
        font-family: 'Arial', sans-serif !important;
        cursor: pointer !important;
        margin-top: 10px !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #6B0000 !important;
        box-shadow: 0 8px 20px rgba(139, 0, 0, 0.6) !important;
        transform: translateY(-3px) !important;
    }
    
    /* 针对primary类型按钮的更具体选择器 */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #8B0000 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("配置选项")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传单词Excel文件",
        type=["xlsx"],
        help="Excel文件需包含'单词'和'中文翻译'两列"
    )
    
    # 参数设置
    num_questions = st.number_input(
        "题目数量",
        min_value=1,
        value=10,
        step=1,
        help="需要生成的题目数量"
    )
    
    num_options = st.number_input(
        "选项数量",
        min_value=2,
        value=4,
        step=1,
        help="每个题目的选项数量"
    )
    
    # 生成按钮
    generate_button = st.button("生成题目", type="primary")

# 主内容区
if uploaded_file is not None:
    # 读取上传的文件
    try:
        word_list = read_word_list_streamlit(uploaded_file)
        if isinstance(word_list, pd.DataFrame):
            st.success(f"✅ 成功读取文件，共包含 {len(word_list)} 个单词")
            
            # 显示单词列表预览
            with st.expander("查看单词列表"):
                st.dataframe(word_list, use_container_width=True)
    except Exception as e:
        st.error(f"❌ 读取文件时出错：{e}")
        word_list = None
    else:
        if isinstance(word_list, str):
            st.error(f"❌ {word_list}")
            word_list = None
else:
    st.info("📁 请先上传单词Excel文件")
    word_list = None

# 生成题目逻辑
if generate_button and word_list is not None:
    with st.spinner("正在生成题目..."):
        # 生成题目
        questions = generate_questions(word_list, num_questions, num_options)
        
        if questions is not None:
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                export_questions(questions, tmp.name)
                
                # 显示生成结果
                st.success(f"🎉 题目生成完成！")
                st.info(f"📊 共生成 {len(questions)} 道题目，每道题目有 {num_options} 个选项")
                
                # 显示题目预览
                with st.expander("查看生成的题目"):
                    st.dataframe(questions, use_container_width=True)
                
                # 提供下载链接
                with open(tmp.name, 'rb') as f:
                    st.download_button(
                        label="📥 下载生成的题目",
                        data=f,
                        file_name="generated_questions.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # 清理临时文件
                os.unlink(tmp.name)
        else:
            st.error("❌ 生成题目失败，请检查参数设置")

# 底部说明
st.markdown("---")
st.markdown("**使用说明：**")
st.markdown("1. 准备包含'单词'和'中文翻译'两列的Excel文件")
st.markdown("2. 上传文件并设置题目数量和选项数量")
st.markdown("3. 点击'生成题目'按钮")
st.markdown("4. 查看预览并下载生成的题目文件")
