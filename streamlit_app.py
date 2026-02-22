import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from groq import Groq

# Groq AI
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine 4K", page_icon="🎬", layout="wide")

# Çerez Dosyası
COOKIE_FILE = "www.youtube.com_cookies.txt" if os.path.exists("www.youtube.com_cookies.txt") else "cookies.txt"

st.title("🎬 ULTRA ENGINE - Yüksek Çözünürlük Modu")
st.markdown("---")

url = st.text_input("YouTube Linki:", placeholder="Yüksek kalite indirmek istediğiniz linki girin...")

if url:
    with st.spinner("En yüksek kalite (1080p/4K) hazırlanıyor... Bu işlem birleştirme nedeniyle biraz sürebilir."):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # --- YÜKSEK KALİTE AYARLARI ---
                ydl_opts = {
                    # En iyi video (mp4) ve en iyi sesi (m4a) bul ve birleştir
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4', # FFmpeg kullanarak birleştirme yapar
                    'nocheckcertificate': True,
                    'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                    'quiet': False, # Hataları loglarda görmek için
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'web'],
                        }
                    },
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    fpath = ydl.prepare_filename(info)
                    
                    # Dosya ismi kontrolü (uzantı değişmiş olabilir)
                    if not os.path.exists(fpath):
                        fpath = fpath.rsplit('.', 1)[0] + ".mp4"

                    st.subheader(f"✅ Hazır: {info.get('title')}")
                    
                    with open(fpath, "rb") as f:
                        st.download_button(
                            label="📥 YÜKSEK KALİTE VİDEOYU İNDİR",
                            data=f,
                            file_name=os.path.basename(fpath),
                            mime="video/mp4"
                        )
                    
                    st.success(f"Çözünürlük: {info.get('width')}x{info.get('height')}")

                # AI Analizi (Opsiyonel)
                st.info("🤖 AI Analizi: " + GoogleTranslator(target='tr').translate(
                    client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Summarize: {info.get('title')}"}]
                    ).choices[0].message.content
                ))

        except Exception as e:
            st.error(f"Hata: {str(e)}")
            st.warning("Eğer 1080p+ inmiyorsa, sunucuda FFmpeg yüklü olmayabilir veya YouTube bu kaliteyi çerezsiz vermiyor olabilir.")
