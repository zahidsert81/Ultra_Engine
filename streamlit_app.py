import streamlit as st
import yt_dlp
import os
import tempfile

# Sayfa Ayarları
st.set_page_config(page_title="Ultra Engine 4K", page_icon="🎬", layout="centered")

# Çerez Dosyası
COOKIE_FILE = "www.youtube.com_cookies.txt"

st.title("🎬 ULTRA ENGINE - High Quality Mode")
st.info("Bu modda FFmpeg kullanılarak video ve ses en yüksek kalitede birleştirilir.")

# Form Yapısı (Enter ile değil, sadece butonla çalışır)
with st.form("hq_download_form"):
    url = st.text_input("YouTube Linki:", placeholder="https://www.youtube.com/watch?v=...")
    submit_button = st.form_submit_button(label="🚀 YÜKSEK KALİTE HAZIRLA")

if submit_button:
    if not url:
        st.warning("Lütfen bir link girin!")
    else:
        with st.spinner("En yüksek kalite (1080p+) taranıyor ve birleştiriliyor... Bu işlem biraz zaman alabilir."):
            try:
                # Geçici bir dizin oluşturarak işlemi orada yapıyoruz
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        # En iyi video (mp4) ve en iyi sesi (m4a) seç ve birleştir
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'merge_output_format': 'mp4', # FFmpeg'i tetikleyen satır
                        'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                        'source_address': '0.0.0.0', # IPv4 zorlaması
                        'nocheckcertificate': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'web'],
                            }
                        },
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        fpath = ydl.prepare_filename(info)
                        
                        # Eğer dosya ismi değiştiyse (örn. mkv olduysa mp4'e zorla)
                        if not os.path.exists(fpath):
                            fpath = fpath.rsplit('.', 1)[0] + ".mp4"

                        st.success(f"İşlem Tamamlandı: {info.get('title')}")
                        st.write(f"**Çözünürlük:** {info.get('width')}x{info.get('height')}")
                        
                        # Dosyayı sunucudan kullanıcıya transfer et
                        with open(fpath, "rb") as f:
                            st.download_button(
                                label="📥 YÜKSEK KALİTEYİ İNDİR",
                                data=f,
                                file_name=os.path.basename(fpath),
                                mime="video/mp4"
                            )

            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
                if "403" in str(e):
                    st.warning("YouTube erişimi reddetti. Lütfen cookies.txt dosyasını yenileyin.")
