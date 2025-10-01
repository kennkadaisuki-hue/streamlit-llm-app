import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

import streamlit as st

st.title("地域の歴史・グルメ情報紹介アプリ")
st.write("##### 動作モード1: 歴史スポット")
st.write("歴史スポットの動作モードをクリックし、地域名を入力後「実行」ボタンを押すことでその地域の歴史スポットを案内します。")
st.write("##### 動作モード2: グルメ情報")
st.write("グルメ情報の動作モードをクリックし、地域名を入力後「実行」ボタンを押すことでその地域のグルメ情報を紹介します。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["歴史スポット", "グルメ情報"]
)

st.divider()

input_message = st.text_input(label="観光地の地名を入力してください")

if st.button("実行"):
    st.divider()
    if not input_message:
        st.error("観光地名を入力してください。")
    else:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        if selected_item == "歴史スポット":
            sys_prompt = "あなたはとても親切な日本語のアシスタントです。入力された観光地について、3つの歴史的な観光スポットを日本語で簡潔に紹介してください。"
        else:
            sys_prompt = "あなたはとても親切な日本語のアシスタントです。入力された観光地について、3つのグルメスポットを日本語で簡潔に紹介してください。"
        messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=input_message),
        ]
        result = llm(messages)
        st.write(result.content if hasattr(result, 'content') else result)

