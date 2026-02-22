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
        "format": "İndirme Türünü Seçin:",
        "btn": "İŞLEMİ BAŞLAT",
        "save": "📥 CİHAZA KAYDET",
        "ai": "🤖 Yapay Zeka Video Analizi",
        "success": "✅ Dosya başarıyla hazırlandı!",
        "cookie_ok": "✅ YouTube Çerezleri Aktif",
        "cookie_err": "⚠️ cookies.txt bulunamadı!"
    },
    "English": {
        "title": "🚀 ULTRA ENGINE PRO",
        "link": "Video or Music Link:",
        "format": "Select Download Type:",
        "btn": "START PROCESS",
        "save": "📥 SAVE TO DEVICE",
        "ai": "🤖 AI Video Analysis",
        "success": "✅ File prepared successfully!",
        "cookie_ok": "✅ Cookies Active",
        "cookie_err": "⚠️ cookies.txt missing!"
    }
}
T = texts[lang]

# Çerez Dosyası Kontrolü (GitHub deponuzdaki dosya adlarına göre)
cookie_file = "cookies.text"
if not os.path.exists(cookie_file):
    cookie_file = "www.youtube.com_cookies.txt" # Alternatif dosya adı kontrolü

if os.path.exists(cookie_file):
    st.sidebar.success(T["cookie_ok"])
else:
    st.sidebar.warning(T["cookie_err"])

st.title(T["title"])
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(T["link"], placeholder="YouTube, Shorts, Instagram...")
    mode = st.selectbox(T["format"], ["Video (MP4)", "Müzik (MP3)"])
    
    if st.button(T["btn"]):
        if not url:
            st.error("Lütfen bir link girin!")
        else:
            with st.spinner("İşlem yapılıyor..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        # --- FORMAT HATASI ÇÖZÜMÜ ---
                        # Bu format ayarı, en yüksek kalite birleşmezse en iyi tek dosyayı çeker.
                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'nocheckcertificate': True,
                            'quiet': True,
                            'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
                            'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                            }
                        }

                        if mode == "Müzik (MP3)":
                            ydl_opts.update({
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            })

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            fpath = ydl.prepare_filename(info)
                            
                            # MP3 uzantı kontrolü
                            if mode == "Müzik (MP3)":
                                fpath = os.path.splitext(fpath)[0] + ".mp3"

                            with open(fpath, "rb") as f:
                                st.download_button(T["save"], f, file_name=os.path.basename(fpath))
                            st.success(T["success"])
                            
                            # AI Analiz
                            with col2:
                                st.subheader(T["ai"])
                                ai_msg = f"Summarize this briefly: {info.get('title')} {info.get('description', '')[:300]}"
                                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":ai_msg}])
                                target_l = 'tr' if lang == "Turkish" else 'en'
                                st.info(GoogleTranslator(target=target_l).translate(res.choices[0].message.content))
                                
                except Exception as e:
                    st.error(f"Hata: {str(e)}")
