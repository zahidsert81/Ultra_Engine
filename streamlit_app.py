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
        "title": "🚀 ULTRA ENGINE ÇEVRİMİÇİ",
        "link": "Video veya Müzik Linki:",
        "format": "Format Seçin:",
        "btn": "İŞLEMİ BAŞLAT",
        "save": "📥 CİHAZA KAYDET",
        "ai": "🤖 Yapay Zeka Analizi",
        "success": "İşlem başarıyla tamamlandı!",
        "cookie_ok": "✅ Çerezler Aktif (YouTube Engeli Kaldırıldı)",
        "cookie_err": "⚠️ cookies.txt bulunamadı! YouTube hata verebilir."
    },
    "English": {
        "title": "🚀 ULTRA ENGINE ONLINE",
        "link": "Video or Music Link:",
        "format": "Select Format:",
        "btn": "START PROCESS",
        "save": "📥 SAVE TO DEVICE",
        "ai": "🤖 AI Video Analysis",
        "success": "Process completed successfully!",
        "cookie_ok": "✅ Cookies Active (YouTube Bypass Enabled)",
        "cookie_err": "⚠️ cookies.txt not found! YouTube may block."
    }
}
T = texts[lang]

# Çerez Dosyası Kontrolü
cookie_path = "cookies.txt" 
if os.path.exists(cookie_path):
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
            with st.spinner("Bulut sunucusu işliyor..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        ydl_opts = {
                            'format': 'best',
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'nocheckcertificate': True,
                            'quiet': True,
                            # Çerez dosyasını depondaki isme göre ayarladık
                            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
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
                            st.success(T["success"])
                            
                            # Gelişmiş AI Analizi
                            with col2:
                                st.subheader(T["ai"])
                                ai_msg = f"Bu içeriği özetle, kategorisini belirt ve 5 popüler hashtag ekle: {info.get('title')} {info.get('description', '')[:300]}"
                                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":ai_msg}])
                                target_l = 'tr' if lang == "Turkish" else 'en'
                                translated_res = GoogleTranslator(source='auto', target=target_l).translate(res.choices[0].message.content)
                                st.info(translated_res)
                                
                except Exception as e:
                    st.error(f"Hata: {str(e)}")
                    if "403" in str(e):
                        st.info("YouTube engeli algılandı. Lütfen cookies.txt dosyasını yenileyin.")
