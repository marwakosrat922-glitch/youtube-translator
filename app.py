import os
import time
import streamlit as st
from google import genai
import yt_dlp

GEMINI_API_KEY ="AQ.Ab8RN6LijmR7IPXXeIPePhaohAjpCdTMMTlWesMiJs2d1KYZEA"
MODEL = "gemini-3.8-flash"

client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="یوتوب بە کوردی", page_icon="🎥")
st.title("🎥 یوتوب بە کوردی")
st.write("لینکی هەر ڤیدیۆیەکی یوتوب دابنێ، بە کوردی سۆرانی دەیگێڕێت.")

PROMPT = """Listen carefully to the audio of this video.
Provide the output in two clear sections:
1. Kurdish Translation only (fluent Sorani Kurdish, line by line with timestamps like [00:12]).
2. Bilingual Transcript (both English original lyrics/words and Kurdish translation side by side or line by line with timestamps).
Ensure the Kurdish is natural and accurate."""

url = st.text_input("🔗 لینکی یوتوب:")

if url:
    st.video(url)

    if st.button("🚀 وەرگێڕان بۆ کوردی"):
        with st.spinner("کەمێک چاوەڕێ بکە... ⏳"):
            audio_file = "downloaded_audio.m4a"
            if os.path.exists(audio_file):
                os.remove(audio_file)

            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": audio_file,
                "quiet": True,
                "no_warnings": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                uploaded = client.files.upload(file=audio_file)
                while uploaded.state.name == "PROCESSING":
                    time.sleep(2)
                    uploaded = client.files.get(name=uploaded.name)

                response = None
                for attempt in range(5):
                    try:
                        response = client.models.generate_content(
                            model=MODEL,
                            contents=[uploaded, PROMPT],
                        )
                        break
                    except Exception as e:
                        if "503" in str(e) and attempt < 4:
                            time.sleep(10)
                        else:
                            raise

                st.success("وەرگێڕان تەواو بوو!")
                st.markdown("---")
                st.subheader("📝 کوردی:")
                st.write(response.text)

            except Exception as e:
                st.error(f"⚠️ هەڵە: {e}")
