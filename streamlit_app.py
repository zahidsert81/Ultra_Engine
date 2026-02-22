import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from gtts import gTTS
from groq import Groq

# AI Bağlantısı
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Motor AI", page_icon="🚀")

# --- DİL SEÇENEĞİ ---
lang = st.sidebar.selectbox("Language / Dil", ["Turkish", "English"])

texts = {
    "Turkish": {
        "title": "🚀 ULTRA MOTOR ÇEVRİMİÇİ",
        "link_lab": "Link Yapıştırın:",
        "format_lab": "Format Seçin:",
        "btn": "İŞLEMİ BAŞLAT",
        "warn": "Lütfen bir link girin!",
        "process": "İşleniyor, lütfen bekleyin...",
        "success": "Başarıyla hazırlandı!",
        "save": "📥 DOSYAYI CİHAZINA KAYDET",
        "ai_title": "🤖 AI Video Analizi",
        "error": "Hata oluştu: "
    },
    "English": {
        "title": "🚀 ULTRA MOTOR ONLINE",
        "link_lab": "Paste Link:",
        "format_lab": "Select Format:",
        "btn": "START OPERATION",
        "warn": "Please enter a link!",
        "process": "Processing, please wait...",
        "success": "Ready successfully!",
        "save": "📥 SAVE TO DEVICE",
        "ai_title": "🤖 AI Video Analysis",
        "error": "Error occurred: "
    }
}

T = texts[lang]

st.title(T["title"])
st.markdown("---")

url = st.text_input(T["link_lab"], placeholder="YouTube, Instagram, TikTok...")
format_secim = st.selectbox(T["format_lab"], ["Video (MP4)", "Müzik (MP3)"])

if st.button(T["btn"]):
    if not url:
        st.warning(T["warn"])
    else:
        with st.spinner(T["process"]):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'nocheckcertificate': True,
                        'quiet': True,
                        # YouTube 403 Hatası İçin Kritik Fix
                        'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        }
                    }

                    if format_secim == "Müzik (MP3)":
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        fpath = ydl.prepare_filename(info)
                        if format_secim == "Müzik (MP3)": fpath = os.path.splitext(fpath)[0] + ".mp3"

                        with open(fpath, "rb") as f:
                            st.download_button(T["save"], f, file_name=os.path.basename(fpath))
                        
                        st.success(T["success"])
                        
                        # AI Analiz
                        st.subheader(T["ai_title"])
                        prompt = f"Summarize this in 3 bullets: {info.get('title')} {info.get('description')[:300]}"
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                        summary = res.choices[0].message.content
                        
                        # Dile göre çevir
                        target_lang = 'tr' if lang == "Turkish" else 'en'
                        final_summary = GoogleTranslator(source='auto', target=target_lang).translate(summary)
                        st.info(final_summary)

            except Exception as e:
                st.error(f"{T['error']} {str(e)}")
