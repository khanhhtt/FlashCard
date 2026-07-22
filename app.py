# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:34:21 2026

@author: httk
"""

import streamlit as st
import pandas as pd
import random
import os

# Set up page styling
st.set_page_config(page_title="Chinese Lesson Flashcards", page_icon="🏮", layout="centered")

st.markdown("""
    <style>
    /* 1. Hides standard menus, headers, and footers */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 2. Target and completely remove the external Streamlit Cloud branding badges */
    div[class^="viewerBadge_container"], 
    div[class*="viewerBadge_container"],
    .viewerBadge_container__1QSob, 
    .styles_viewerBadge__1yB5_,
    [data-testid="stViewerBadge"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
    }
    
    /* Your existing flashcard styles */
    .flashcard-box {
        padding: 40px;
        border-radius: 15px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .chinese-text { font-size: 70px; font-weight: bold; color: #333333; margin: 0; }
    .pinyin-text { font-size: 28px; color: #888888; font-style: italic; margin-top: 10px; }
    .english-text { font-size: 32px; color: #ff4b4b; font-weight: 500; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)


st.title("🏮 Video Lesson Flashcards")

# 1. Read the lesson parameter from the URL query
# Example: https://streamlit.app
query_params = st.query_params
requested_lesson = query_params.get("lesson", "default")

# 2. Determine which file path to load
lessons_dir = "lessons"
file_loaded = False

# Fallback sample vocabulary if the requested file isn't found
fallback_data = {
    "Chinese": ["你好", "谢谢", "学习"],
    "Pinyin": ["nǐ hǎo", "xièxie", "xuéxí"],
    "English": ["Hello", "Thank you", "To study"]
}

if requested_lesson != "default":
    # Match URL parameter directly to a file name in the folder
    csv_path = os.path.join(lessons_dir, f"{requested_lesson}.csv")
    xlsx_path = os.path.join(lessons_dir, f"{requested_lesson}.xlsx")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        file_loaded = True
    elif os.path.exists(xlsx_path):
        df = pd.read_excel(xlsx_path)
        file_loaded = True
    else:
        st.warning(f"Lesson '{requested_lesson}' not found. Loading default set.")
        df = pd.DataFrame(fallback_data)
else:
    df = pd.DataFrame(fallback_data)

# Display context to the user based on the active lesson
lesson_title = requested_lesson.replace("_", " ").title()
st.subheader(f"📖 Current Unit: {lesson_title}")

# 3. Setup Session State variables to keep track of current card index
# We include the lesson name in the session key to reset index if they switch lessons
if "current_lesson" not in st.session_state or st.session_state.current_lesson != requested_lesson:
    st.session_state.current_lesson = requested_lesson
    st.session_state.card_index = 0
    st.session_state.flipped = False

# Ensure index safety limits
if st.session_state.card_index >= len(df):
    st.session_state.card_index = 0

# Get current row vocabulary data
current_row = df.iloc[st.session_state.card_index]

# Progress layout
st.write(f"**Card {st.session_state.card_index + 1} of {len(df)}**")

# 4. Render Flashcard
with st.container():
    if not st.session_state.flipped:
        st.markdown(f"""
            <div class="flashcard-box">
                <p class="chinese-text">{current_row['Chinese']}</p>
                <p style="color:#aaa; margin-top:20px;">[ Click Flip to see meaning ]</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="flashcard-box">
                <p class="chinese-text">{current_row['Chinese']}</p>
                <p class="pinyin-text">{current_row['Pinyin']}</p>
                <hr style="border: 0; border-top: 1px dashed #ddd; margin: 15px 0;">
                <p class="english-text">{current_row['English']}</p>
            </div>
        """, unsafe_allow_html=True)

# 5. Interactive Navigation Controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⬅️ Previous"):
        st.session_state.card_index = (st.session_state.card_index - 1) % len(df)
        st.session_state.flipped = False
        st.rerun()

with col2:
    if st.button("🔄 Flip Card"):
        st.session_state.flipped = not st.session_state.flipped
        st.rerun()

with col3:
    if st.button("Next ➡️"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(df)
        st.session_state.flipped = False
        st.rerun()

with col4:
    if st.button("🔀 Shuffle"):
        st.session_state.card_index = random.randint(0, len(df) - 1)
        st.session_state.flipped = False
        st.rerun()

