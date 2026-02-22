import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from groq import Groq

# Groq AI Bağlantısı
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine Online", page_icon="🚀", layout="wide")

# --- DİL SEÇENEKLERİ ---
lang = st.sidebar.selectbox("Language / Dil Seçin", ["Turkish", "English"])
texts = {
    "Turkish": {
        "title": "🚀 ULTRA ENGINE PRO",
        "link": "Video veya Müzik Linki:",
        "format": "Format Seçin:",
        "btn": "İŞLEMİ BAŞLAT",
        "save": "📥 CİHAZA KAYDET",
        "ai": "🤖 Yapay Zeka Analizi",
        "cookie_ok": "✅ Çerezler Aktif",
        "cookie_err": "⚠️ cookies.txt Eksik!"
    },
    "English": {
        "title": "🚀 ULTRA ENGINE PRO",
        "link": "Video or Music Link:",
        "format": "Select Format:",
        "btn": "START PROCESS",
        "save": "📥 SAVE TO DEVICE",
        "ai": "🤖 AI Analysis",
        "cookie_ok": "✅ Cookies Active",
        "cookie_err": "⚠️ Cookies Missing!"
    }
}
T = texts[lang]

# Çerez Dosyası Kontrolü (GitHub deponda ismi 'cookies.txt' olduğu için buna sabitledik)
cookie_file = "cookies.text"
if os.path.exists(cookie_file):
    st.sidebar.success(T["cookie_ok"])
else:
    st.sidebar.warning(T["cookie_err"])

st.title(T["title"])
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(T["link"], placeholder="YouTube, Instagram, TikTok...")
    mode = st.selectbox(T["format"], ["Video (MP4)", "Müzik (MP3)"])
    
    if st.button(T["btn"]):
        if not url:
            st.error("Lütfen bir link girin!")
        else:
            with st.spinner("İşlem yapılıyor..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            # FORMAT HATASI ÇÖZÜMÜ: En iyi birleşik mp4'ü zorla, olmazsa en iyisini al
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'nocheckcertificate': True,
                            'quiet': True,
                            # Yüklediğin cookies.txt dosyasını kullan
                            'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
                            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                            }
                        }

                        if mode == "Müzik (MP3)":
                            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            fpath = ydl.prepare_filename(info)
                            if mode == "Müzik (MP3)": fpath = os.path.splitext(fpath)[0] + ".mp3"

                            with open(fpath, "rb") as f:
                                st.download_button(T["save"], f, file_name=os.path.basename(fpath))
                            st.success("Hazır!")
                            
                            # AI Analizi
                            with col2:
                                st.subheader(T["ai"])
                                prompt = f"Summarize this briefly: {info.get('title')} {info.get('description', '')[:200]}"
                                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                                target_lang = 'tr' if lang == "Turkish" else 'en'
                                st.info(GoogleTranslator(target=target_lang).translate(res.choices[0].message.content))
                                
                except Exception as e:
                    st.error(f"Hata detayı: {str(e)}")
