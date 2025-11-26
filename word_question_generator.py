import streamlit as st
import pandas as pd
import random
from io import BytesIO

def main():
    # 设置页面标题和图标
    st.markdown("<h2 style='font-size: 24px;'>KkoMa的题目生成工具v1.0</h2>", unsafe_allow_html=True)
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传单词Excel文件", 
        type=["xlsx", "xls"],
        help="支持.xlsx和.xls格式，表头需包含'单词'和'中文翻译'两列"
    )
    
    # 题目参数设置 - 一行两列布局
    col1, col2 = st.columns(2)
    with col1:
        st.write("题目数量")
        question_count = st.number_input(
            "题目数量", 
            min_value=1, 
            max_value=1000, 
            value=100,
            label_visibility="collapsed"
        )
    with col2:
        st.write("选项数量")
        option_count = st.number_input(
            "选项数量", 
            min_value=2, 
            max_value=10, 
            value=3,
            label_visibility="collapsed"
        )
    
    # 按钮样式 - 居中并拉宽
    st.markdown("""
    <style>
    /* 确保容器占满整个宽度并居中 */
    .generate-button-container {
        display: flex;
        justify-content: center;
        margin: 10px 0;
        width: 100% !important;
    }
    
    /* 重置Streamlit默认按钮样式 */
    div[data-testid="stButton"] button {
        background-color: white !important;
        color: #333333 !important;
        font-size: 14px !important;
        font-weight: normal !important;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        border: 1px solid #cccccc !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] button:hover {
        background-color: #f0f0f0 !important;
        color: #333333 !important;
    }
    
    /* 生成题目按钮 - 醒目样式（最高优先级） */
    div.generate-button-container > div[data-testid="stButton"] > button {
        width: 550px !important;
        background-color: #8B0000 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 18px 35px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(139, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
        z-index: 999 !important;
        outline: none !important;
        font-family: 'Arial', sans-serif !important;
        cursor: pointer !important;
        display: inline-block !important;
        margin: 0 auto !important;
    }
    
    div.generate-button-container > div[data-testid="stButton"] > button:hover {
        background-color: #6B0000 !important;
        box-shadow: 0 8px 20px rgba(139, 0, 0, 0.6) !important;
        transform: translateY(-3px) !important;
    }
    
    /* 针对特定按钮的更具体选择器，确保覆盖所有情况 */
    div.generate-button-container > div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #8B0000 !important;
        color: white !important;
    }
    
    /* 确保按钮文字居中 */
    div[data-testid="stButton"] > button div {
        text-align: center !important;
        margin: 0 auto !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用容器包裹按钮实现居中
    st.markdown('<div class="generate-button-container">', unsafe_allow_html=True)
    generate_button = st.button("生成题目", key="generate_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 初始化变量
    df = None
    word_count = 0
    
    if uploaded_file is not None:
        # 读取Excel文件
        df = pd.read_excel(uploaded_file)
        
        # 检查表头是否正确
        if '单词' not in df.columns or '中文翻译' not in df.columns:
            st.error("Excel文件格式错误！请确保表头包含'单词'和'中文翻译'两列。")
            df = None
        else:
            st.success(f"成功读取文件，共包含 {len(df)} 个单词")
            word_count = len(df)
            
            # 查看单词列表按钮
            if st.button("查看单词列表"):
                st.dataframe(df)
            
            # 检查题目数量是否足够
            if question_count < word_count:
                st.warning(f"注意：题目数量({question_count})少于单词数量({word_count})，可能无法保证每个单词至少出现一次作为正确答案。")
            elif option_count > word_count:
                st.error(f"选项数量({option_count})不能大于单词数量({word_count})！")
    
    # 使用说明 - 上下布局，放在配置选项下方
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 16px; margin-bottom: 8px;'>使用说明</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 13px; color: #666666; line-height: 1.6;'>
    <div>1. 准备包含'单词'和'中文翻译'两列的Excel文件</div>
    <div>2. 上传文件并设置题目数量和选项数量</div>
    <div>3. 点击'生成题目'按钮</div>
    <div>4. 查看预览并下载生成的题目文件</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 生成题目逻辑
    if generate_button:
        if df is None:
            st.error("请先上传有效的Excel文件！")
        else:
            # 再次确认选项数量不大于单词数量
            if option_count > word_count:
                st.error(f"选项数量({option_count})不能大于单词数量({word_count})！")
            else:
                with st.spinner("正在生成题目..."):
                    # 生成题目
                    result_df = generate_questions(df, question_count, option_count)
                
                st.success("题目生成完成！")
                
                # 显示前几行结果
                st.write("生成的题目预览：")
                st.dataframe(result_df.head())
                
                # 导出为Excel文件
                towrite = BytesIO()
                result_df.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)
                
                st.download_button(
                    label="下载题目Excel文件",
                    data=towrite,
                    file_name="generated_questions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def generate_questions(df, question_count, option_count):
    words = df['单词'].tolist()
    word_count = len(words)
    
    # 创建结果数据框
    columns = ['题干'] + [f'选项{j+1}' for j in range(option_count)] + ['正确选项']
    result_df = pd.DataFrame(columns=columns)
    
    # 确保每个单词至少作为一次正确答案
    # 先为每个单词生成一道题目
    required_questions = []
    words_copy = words.copy()
    random.shuffle(words_copy)
    
    for word in words_copy:
        # 随机选择其他单词作为干扰项
        other_words = [w for w in words if w != word]
        random.shuffle(other_words)
        distractors = other_words[:option_count-1]
        
        # 合并题干单词和干扰项，并随机排序
        options = [word] + distractors
        random.shuffle(options)
        
        # 确定正确选项的位置
        correct_option_index = options.index(word) + 1
        correct_option_text = f'选项{correct_option_index}'
        
        # 记录题目
        row = {'题干': word}
        for j in range(option_count):
            row[f'选项{j+1}'] = options[j]
        row['正确选项'] = correct_option_text
        
        required_questions.append(row)
    
    # 如果需要更多题目，随机生成剩余题目
    remaining_questions = max(question_count - word_count, 0)
    additional_questions = []
    
    for i in range(remaining_questions):
        # 随机选择题干单词
        question_word = random.choice(words)
        
        # 随机选择其他单词作为干扰项
        other_words = [w for w in words if w != question_word]
        random.shuffle(other_words)
        distractors = other_words[:option_count-1]
        
        # 合并题干单词和干扰项，并随机排序
        options = [question_word] + distractors
        random.shuffle(options)
        
        # 确定正确选项的位置
        correct_option_index = options.index(question_word) + 1
        correct_option_text = f'选项{correct_option_index}'
        
        # 记录题目
        row = {'题干': question_word}
        for j in range(option_count):
            row[f'选项{j+1}'] = options[j]
        row['正确选项'] = correct_option_text
        
        additional_questions.append(row)
    
    # 合并所有题目
    all_questions = required_questions + additional_questions
    
    # 打乱题目的顺序
    random.shuffle(all_questions)
    
    # 将题目转换为DataFrame
    result_df = pd.DataFrame(all_questions, columns=columns)
    
    return result_df

if __name__ == '__main__':
    main()