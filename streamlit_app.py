import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from groq import Groq

# Groq AI Bağlantısı
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine Online", page_icon="🚀", layout="wide")

# --- ÇEREZ DOSYASI YÖNETİMİ ---
# GitHub deponda hangi isimle varsa onu bulur
cookie_file = "cookies.text" if os.path.exists("cookies.txt") else "www.youtube.com_cookies.txt"

# --- DİL SEÇENEKLERİ ---
lang = st.sidebar.selectbox("Language / Dil", ["Turkish", "English"])
texts = {
    "Turkish": {
        "title": "🚀 ULTRA ENGINE PRO",
        "link": "Video veya Müzik Linki:",
        "format": "Tür Seçin:",
        "btn": "İŞLEMİ BAŞLAT",
        "save": "📥 CİHAZA KAYDET",
        "cookie_ok": "✅ Çerezler Aktif",
        "cookie_err": "⚠️ Çerezler Geçersiz veya Eksik!"
    },
    "English": {
        "title": "🚀 ULTRA ENGINE PRO",
        "link": "Video or Music Link:",
        "format": "Select Type:",
        "btn": "START PROCESS",
        "save": "📥 SAVE TO DEVICE",
        "cookie_ok": "✅ Cookies Active",
        "cookie_err": "⚠️ Cookies Invalid/Missing!"
    }
}
T = texts[lang]

# Sidebar Bilgi
if os.path.exists(cookie_file):
    st.sidebar.success(T["cookie_ok"])
else:
    st.sidebar.error(T["cookie_err"])

st.title(T["title"])
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(T["link"], placeholder="https://youtube.com/...")
    mode = st.selectbox(T["format"], ["Video (MP4)", "Müzik (MP3)"])
    
    if st.button(T["btn"]):
        if not url:
            st.error("Lütfen bir link girin!")
        else:
            with st.spinner("YouTube Korumaları Aşılıyor..."):
                try:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        # 403 ve PO-TOKEN HATALARINI AŞAN ÖZEL AYARLAR
                        ydl_opts = {
                            # En uyumlu formatı seç (Sunucuda birleştirme yapmadan direkt indirir)
                            'format': 'best', 
                            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                            'nocheckcertificate': True,
                            'quiet': True,
                            'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
                            # YouTube'un yeni bot korumasını aşmak için istemci taklidi
                            'extractor_args': {
                                'youtube': {
                                    'player_client': ['android_vr', 'web_embedded', 'tv'],
                                    'player_skip': ['js'],
                                }
                            },
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Accept': '*/*',
                                'Connection': 'keep-alive',
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
                            # Video bilgisini al ve indir
                            info = ydl.extract_info(url, download=True)
                            fpath = ydl.prepare_filename(info)
                            
                            # MP3 ise uzantıyı düzelt
                            if mode == "Müzik (MP3)":
                                fpath = os.path.splitext(fpath)[0] + ".mp3"

                            with open(fpath, "rb") as f:
                                st.download_button(T["save"], f, file_name=os.path.basename(fpath))
                            st.success("İşlem Başarılı!")
                            
                            # AI Analizi
                            with col2:
                                st.subheader("🤖 AI Analizi")
                                summary_prompt = f"Summarize this video content briefly: {info.get('title')} {info.get('description', '')[:300]}"
                                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":summary_prompt}])
                                translated = GoogleTranslator(target='tr' if lang=="Turkish" else 'en').translate(res.choices[0].message.content)
                                st.info(translated)
                                
                except Exception as e:
                    if "403" in str(e):
                        st.error("HATA 403: YouTube çerezlerinizi reddetti. Lütfen cookies.txt dosyasını yenileyin.")
                    else:
                        st.error(f"Hata: {str(e)}")
