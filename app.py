# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:34:21 2026

@author: httk
"""

import streamlit as st
import pandas as pd
import random

# Set up page styling
st.set_page_config(page_title="Chinese Flashcard Hub", page_icon="🏮", layout="centered")

st.markdown("""
    <style>
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

st.title("🏮 Chinese Vocabulary Flashcards")
st.write("Upload your vocabulary list to start studying. Share this page's link with anyone to let them practice too!")

# 1. File Uploading (Expects columns: Chinese, Pinyin, English)
uploaded_file = st.file_uploader("Upload your vocabulary file (CSV or Excel)", type=["csv", "xlsx"])

# Default fallback vocabulary data if no file is uploaded yet
default_data = {
    "Chinese": ["你好", "谢谢", "学习", "苹果"],
    "Pinyin": ["nǐ hǎo", "xièxie", "xuéxí", "píngguǒ"],
    "English": ["Hello", "Thank you", "To study / learn", "Apple"]
}

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Simple validation
        required_cols = ["Chinese", "Pinyin", "English"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"Your file must contain these exact column headers: {', '.join(required_cols)}")
            df = pd.DataFrame(default_data)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        df = pd.DataFrame(default_data)
else:
    df = pd.DataFrame(default_data)
    st.info("💡 Showing sample vocabulary. Upload your own file above to update the deck.")

# 2. Setup Session State variables to keep track of current card index
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "flipped" not in st.session_state:
    st.session_state.flipped = False

# Ensure the card index doesn't overshoot if a shorter file is uploaded
if st.session_state.card_index >= len(df):
    st.session_state.card_index = 0

# Get current word data
current_row = df.iloc[st.session_state.card_index]

# Progress layout
st.write(f"**Card {st.session_state.card_index + 1} of {len(df)}**")

# 3. Render Flashcard
with st.container():
    if not st.session_state.flipped:
        # Front of card (Hanzi Only)
        st.markdown(f"""
            <div class="flashcard-box">
                <p class="chinese-text">{current_row['Chinese']}</p>
                <p style="color:#aaa; margin-top:20px;">[ Click Flip to see meaning ]</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Back of card (Hanzi + Pinyin + English)
        st.markdown(f"""
            <div class="flashcard-box">
                <p class="chinese-text">{current_row['Chinese']}</p>
                <p class="pinyin-text">{current_row['Pinyin']}</p>
                <hr style="border: 0; border-top: 1px dashed #ddd; margin: 15px 0;">
                <p class="english-text">{current_row['English']}</p>
            </div>
        """, unsafe_allow_html=True)

# 4. Interaction Controls
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

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
