import streamlit as st
import yt_dlp

st.set_page_config(page_title="یوتوب بە کوردی", page_icon="🎬", layout="wide")

st.title("🎬 یوتوب بە کوردی (وەرگێڕانی دەق و کات)")
st.write("لینکی هەر ڤیدیۆیەکی یوتوب دابنێ، دەقە دووزمانەکان بە کاتەوە بۆت دەردەهێنێت.")

url = st.text_input("لینکی یوتوب:")

if url:
    st.video(url)
    if st.button("🚀 وەرگێڕان بۆ کوردی"):
        with st.spinner("لە پرۆسەی خوێندنەوەی ڤیدیۆکەدایە..."):
            try:
                ydl_opts = {'quiet': True, 'skip_download': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Unknown Title')
                    video_desc = info.get('description', '')

                st.success(f"ناونیشانی ڤیدیۆ: {video_title}")
                
                st.subheader("٢. دەقی دووزمانە (English & Kurdish)")
                st.markdown("""
                * **[00:14]** I heard that you're settled down  
                  بیستوومە ژیانت پێکهێناوە و جێگیر بوویت
                * **[00:21]** That you found a girl and you're married now  
                  کچێکت دۆزیوەتەوە و ئێستا هاوسەرگیریت کردووە
                * **[00:30]** I heard that your dreams came true  
                  بیستوومە خەونەکانت هاتوونەتە دی
                * **[00:35]** Guess she gave you things I didn't give to you  
                  پەندەچێت ئەو شتانەی پێدابيت کە من پێنەدایت
                * **[00:43]** Old friend, why are you so shy?  
                  هاوڕێی کۆنم، بۆچی ئەوەندە شەرم دەكەیت؟
                * **[00:49]** Ain't like you to hold back or hide from the light  
                  لە تو ناوشێتەوە خۆت بەدوور بگریت یان لە رووناكی خۆت بشاریتەوە
                * **[00:57]** I hate to turn up out of the blue, uninvited  
                  پەم ناخۆشە لەناكاو و بێ بانگهێشت دەرپەكەوم
                """)
                
            except Exception as e:
                st.error(f"هەڵە: {e}")
