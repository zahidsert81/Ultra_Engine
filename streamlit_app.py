import streamlit as st
import yt_dlp
import os
from deep_translator import GoogleTranslator
from gtts import gTTS
from groq import Groq
import tempfile

# AI Bağlantısı
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine Web", page_icon="🚀")

st.title("🚀 ULTRA ENGINE ONLINE")
st.markdown("Yapay Zeka Destekli Video & Ses İstasyonu")

url = st.text_input("Link Yapıştırın:", placeholder="https://youtube.com/...")
format_tipi = st.selectbox("Format Seçin:", ["Video (MP4)", "Müzik (MP3)"])

if st.button("İŞLEMİ BAŞLAT"):
    if url:
        with st.spinner("Bulut sunucusu işliyor, lütfen bekleyin..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    }
                    if format_tipi == "Müzik (MP3)":
                        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        indirilen_yol = ydl.prepare_filename(info)
                        
                        # İndirme Butonu Oluştur
                        with open(indirilen_yol, "rb") as f:
                            st.download_button("Dosyayı Cihazına Kaydet", f, file_name=os.path.basename(indirilen_yol))
                        st.success("İşlem Başarılı!")
            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
