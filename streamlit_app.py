import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Ultra Engine - Bypass Edition", page_icon="🔓")

# Çerez Dosyası (Mutlaka güncel olmalı)
COOKIE_FILE = "www.youtube.com_cookies.txt"

st.title("🔓 ULTRA ENGINE: BYPASS MODE")
st.markdown("YouTube kısıtlamalarını aşmak için **IPv4 + Android TV Client** aktif.")

with st.form("bypass_form"):
    url = st.text_input("Link:", placeholder="https://www.youtube.com/watch?v=...")
    submit_button = st.form_submit_button(label="🎬 GÜVENLİ İNDİR")

if submit_button and url:
    with st.spinner("IP Engelleri Aşılıyor ve FFmpeg ile Birleştiriliyor..."):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    # Yüksek çözünürlük için en iyi format seçimi
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    
                    # --- BAYPAS AYARLARI ---
                    'source_address': '0.0.0.0', # IPv6 bloklarını aşmak için IPv4 zorla
                    'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                    'nocheckcertificate': True,
                    'extractor_args': {
                        'youtube': {
                            # Bot kontrolünün en zayıf olduğu istemciler
                            'player_client': ['android_vr', 'tv', 'web_embedded'],
                            'po_token': 'web+1'
                        }
                    },
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    fpath = ydl.prepare_filename(info)
                    
                    # Dosya yolu kontrolü
                    if not os.path.exists(fpath):
                        fpath = fpath.rsplit('.', 1)[0] + ".mp4"

                    st.success(f"Bypass Başarılı: {info.get('title')}")
                    st.info(f"Kalite: {info.get('height')}p | Format: MP4")
                    
                    with open(fpath, "rb") as f:
                        st.download_button(
                            label="📥 VİDEOYU BİLGİSAYARINA KAYDET",
                            data=f,
                            file_name=os.path.basename(fpath),
                            mime="video/mp4"
                        )

        except Exception as e:
            st.error(f"Erişim Reddedildi: {str(e)}")
            st.warning("Eğer hala 403 alıyorsan, GitHub'daki çerez dosyanı yenilemen şarttır.")
