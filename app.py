import streamlit as st
from google import genai
import yt_dlp

st.set_page_config(page_title="یوتوب بە کوردی", page_icon="🎬", layout="wide")

st.title("🎬 یوتوب بە کوردی (وەرگێڕانی دەق)")
st.write("لینکی هەر ڤیدیۆیەکی یوتوب دابنێ، وەرگێڕان و دەقی کوردی بە کاتەوە بۆت دەردەهێنێت.")

url = st.text_input("لینکی یوتوب:")

if url:
    st.video(url)
    if st.button("🚀 وەرگێڕان بۆ کوردی"):
        with st.spinner("لە پرۆسەی خوێندنەوە و وەرگێڕانی ڤیدیۆکەدایە..."):
            try:
                # بەکارهێنانی کلیل بۆ جێمنای
                client = genai.Client(api_key="AQ.Ab8RN6LijmR7IPXXeIPePhaohAjpCdTMMTlwesMiJs2d1KYZEA")
                
                ydl_opts = {'quiet': True, 'skip_download': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Unknown Title')
                    video_desc = info.get('description', '')

                prompt = f"Analyze this YouTube video titled '{video_title}'. Provide the lyrics or spoken transcript formatted line by line with timestamps (e.g., [00:14]) translated into fluent Sorani Kurdish, exactly like subtitle style."
                
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.subheader("١. وەرگێڕانی کوردی (سۆرانی)")
                st.write(res.text)
                
            except Exception as e:
                st.error(f"هەڵە: {e}")
