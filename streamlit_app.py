import streamlit as st
import yt_dlp
import os

# Sayfa Ayarları
st.set_page_config(page_title="Ultra Engine Web", page_icon="🚀", layout="centered")

# Çerez Dosyası Kontrolü
COOKIE_FILE = "www.youtube.com_cookies.txt"

st.title("🚀 ULTRA ENGINE WEB v1.6")
st.info("Linkinizi yapıştırın ve 'SORGULA' butonuna basın.")

# FORM BAŞLANGICI: Enter tuşunun sayfayı rastgele yenilemesini engeller
with st.form("download_form"):
    url = st.text_input("YouTube veya Shorts Linki:", placeholder="https://www.youtube.com/watch?v=...")
    submit_button = st.form_submit_button(label="🔍 VİDEOYU SORGULA")

# İşlem sadece butona basıldığında başlar
if submit_button:
    if not url:
        st.warning("Lütfen önce bir link girin!")
    else:
        with st.spinner("YouTube Güvenlik Protokolleri Aşılıyor..."):
            try:
                # 403 Hatalarını ve IP Bloklarını Aşmak İçin Parametreler
                ydl_opts = {
                    'format': 'best', 
                    'quiet': True,
                    'no_warnings': True,
                    'source_address': '0.0.0.0', # IPv4 Zorlaması (IP bloklarını aşmak için)
                    'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android_vr', 'web_embedded'], # En az korunan istemciler
                            'player_skip': ['js'],
                        }
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # extract_info: Videoyu sunucuya indirmez, sadece metadata ve direct-url çeker.
                    info = ydl.extract_info(url, download=False)
                    direct_url = info.get('url')
                    title = info.get('title')
                    thumbnail = info.get('thumbnail')

                    # Sonuçları Göster
                    st.divider()
                    st.success(f"Bağlantı Kuruldu: {title}")
                    st.image(thumbnail, use_container_width=True)

                    # Video Oynatıcı (Kullanıcı burada izleyip sağ tıkla indirebilir)
                    st.video(direct_url)

                    # Profesyonel İndirme Butonu (Direct-Link üzerinden Client-side)
                    st.markdown(f"""
                        <a href="{direct_url}" target="_blank" download="{title}.mp4" style="text-decoration: none;">
                            <div style="
                                width: 100%;
                                background-color: #FF4B4B;
                                color: white;
                                text-align: center;
                                padding: 15px 0;
                                border-radius: 10px;
                                cursor: pointer;
                                font-weight: bold;
                                font-size: 18px;
                                margin-top: 10px;
                                border: 2px solid #ffffff22;
                            ">
                                📥 CİHAZINA KAYDET (1080p/720p)
                            </div>
                        </a>
                    """, unsafe_allow_html=True)
                    st.caption("Not: Eğer buton yeni sekmede videoyu açarsa, sağ tıklayıp 'Farklı Kaydet' deyin.")

            except Exception as e:
                # Loglardaki 403 ve PO Token hatalarını yakalar
                st.error("YouTube Erişimi Reddetti (403 Forbidden).")
                st.warning("Lütfen GitHub'daki 'www.youtube.com_cookies.txt' dosyasını güncelleyin.")
                if "PO Token" in str(e):
                    st.info("YouTube ek bir güvenlik doğrulaması (PO Token) bekliyor.")
