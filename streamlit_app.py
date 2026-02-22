import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Ultra Engine - IP Fix", page_icon="🛡️")

COOKIE_FILE = "www.youtube.com_cookies.txt"

st.title("🛡️ Ultra Engine - IP Blok Bypass Modu")
st.warning("Eğer indirme butonu çalışmıyorsa, 'Doğrudan Link'e sağ tıklayıp farklı kaydedin.")

url = st.text_input("YouTube Linki:")

if url:
    with st.spinner("IP bloğu aşılıyor, direkt link oluşturuluyor..."):
        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
                'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
                'source_address': '0.0.0.0', # IPv4 Zorlaması
                'extractor_args': {'youtube': {'player_client': ['android_vr', 'web_embedded']}}
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False) # SUNUCUYA İNDİRME YAPMAZ!
                
                video_url = info.get('url')
                title = info.get('title')

                st.success(f"Video Bulundu: {title}")
                st.image(info.get('thumbnail'), width=300)

                # YÖNTEM A: Streamlit Player (Kullanıcı burada izleyip sağ tıklayıp indirebilir)
                st.video(video_url)

                # YÖNTEM B: Doğrudan İndirme Butonu (Tarayıcıya yönlendirir)
                st.markdown(f"""
                    <a href="{video_url}" target="_blank" download="{title}.mp4">
                        <button style="background-color: #4CAF50; color: white; padding: 15px 32px; border: none; border-radius: 8px; cursor: pointer; width: 100%;">
                            📥 VİDEOYU BURADAN İNDİR (IP BLOKSUZ)
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                st.caption("Not: Buton çalışmazsa videonun üzerindeki üç noktaya tıklayıp 'İndir' deyin.")

        except Exception as e:
            st.error(f"IP Blok Hatası: {str(e)}")
            st.info("Çözüm: GitHub deponuzun adını değiştirip Streamlit'te yeniden deploy edin.")
