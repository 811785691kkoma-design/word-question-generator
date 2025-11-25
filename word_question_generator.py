import streamlit as st
import pandas as pd
import random
from io import BytesIO

def main():
    # 设置页面标题和图标
    st.markdown("<h2 style='font-size: 24px;'>kkoma的题目生成工具v1.0</h2>", unsafe_allow_html=True)
    
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
    
    /* 生成题目按钮 - 醒目样式 */
    .generate-button-container div[data-testid="stButton"] > button {
        width: 450px !important;
        background-color: #cc0000 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(204, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .generate-button-container div[data-testid="stButton"] > button:hover {
        background-color: #990000 !important;
        box-shadow: 0 6px 16px rgba(204, 0, 0, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 查看单词列表按钮 - 白色背景样式 */
    div[data-testid="stButton"] > button:not(.generate-button-container button) {
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
    
    div[data-testid="stButton"] > button:not(.generate-button-container button):hover {
        background-color: #f5f5f5 !important;
        border-color: #999999 !important;
        box-shadow: none !important;
        transform: none !important;
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
    generate_button = st.button("生成题目")
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
    columns = ['正确选项'] + [f'单词{i+1}' for i in range(option_count)]
    result_df = pd.DataFrame(columns=columns)
    
    # 确保每个单词至少一次作为正确答案
    # 先处理必须的次数
    required_correct = words.copy()
    random.shuffle(required_correct)
    
    # 然后处理剩余的题目
    remaining_questions = max(question_count - len(required_correct), 0)
    extra_correct = [random.choice(words) for _ in range(remaining_questions)]
    
    # 合并所有正确答案
    all_correct = required_correct + extra_correct
    
    # 生成每组题目
    for i in range(question_count):
        correct_word = all_correct[i]
        
        # 随机选择其他单词作为干扰项
        other_words = [word for word in words if word != correct_word]
        random.shuffle(other_words)
        distractors = other_words[:option_count-1]
        
        # 合并正确答案和干扰项，并随机排序
        options = [correct_word] + distractors
        random.shuffle(options)
        
        # 记录选项顺序
        option_dict = {f'单词{j+1}': options[j] for j in range(option_count)}
        
        # 添加到结果数据框
        row = {'正确选项': correct_word, **option_dict}
        result_df = result_df._append(row, ignore_index=True)
    
    return result_df

if __name__ == '__main__':
    main()