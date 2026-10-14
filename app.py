import streamlit as st
from google import genai
import yt_dlp

# دروستکردنی کلاینت بە کلیلەکە
GEMINI_API_KEY = "AQ.Ab8RN6LijmR7IPXXeIPePhaohAjpCdTMMTlwesMiJs2d1KYZEA"
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="یوتوب بە کوردی", page_icon="🎬")
st.title("🎬 یوتوب بە کوردی")
st.write("لینکی هەر ڤیدیۆیەکی یوتوب دابنێ، ناونیشان و ناوەرۆکەکەی بە کوردی سۆرانی بۆت وەردەگێڕێت.")

url = st.text_input("لینکی یوتوب:")

if url:
    st.video(url)
    if st.button("🚀 وەرگێڕان و شیکردنەوە"):
        with st.spinner("لە پرۆسەی وەرگرتنی زانیاری ڤیدیۆکەدایە..."):
            try:
                ydl_opts = {'quiet': True, 'skip_download': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Unknown Title')
                    video_desc = info.get('description', '')

                st.success(f"ناونیشانی ڤیدیۆ: {video_title}")
                
                prompt = f"Translate and summarize this YouTube video title and description into natural Sorani Kurdish: Title: {video_title}, Description: {video_desc[:400]}"
                
                # بەکارهێنانی شێوازی دروستی ڤێرژنی نوێی گلاینت
                response = client.chats.create(model="gemini-2.5-flash") # یان بەکارهێنانی generate_content راستەوخۆ
                
                # ڕێگەی ڕاستەوخۆی generate_content بۆ وەشانی نوێ
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.subheader("📝 پوختە و وەرگێڕان بە کوردی:")
                st.write(res.text)
                
            except Exception as e:
                st.error(f"هەڵە: {e}")
