import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from gtts import gTTS
from groq import Groq

# Güvenlik uyarısını aşmak için anahtarı buraya yerleştiriyoruz
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine ONLİNE", page_icon="🚀", layout="centered")

# Arayüz Tasarımı
st.title("🚀 ULTRA MOTOR ÇEVRİMİÇİ")
st.markdown("---")

url = st.text_input("Link Yapıştırın:", placeholder="https://www.youtube.com/watch?v=...")
format_secim = st.selectbox("Format Seçin:", ["Video (MP4)", "Müzik (MP3)"])

if st.button("İŞLEMİ BAŞLAT"):
    if not url:
        st.warning("Lütfen bir link girin!")
    else:
        with st.spinner("Sunucu videoyu işliyor, bu işlem videonun boyutuna göre vakit alabilir..."):
            try:
                # Geçici klasör oluşturma (Streamlit sunucusu için)
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'nocheckcertificate': True,
                        'ignoreerrors': False,
                        'logtostderr': False,
                        'quiet': True,
                        'no_warnings': True,
                        # 403 Hatasını engellemek için kritik Header ayarları
                        'addheader': [
                            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'),
                            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'),
                            ('Accept-Language', 'en-US,en;q=0.9'),
                        ],
                    }

                    if format_secim == "Müzik (MP3)":
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Video bilgilerini al ve indir
                        info = ydl.extract_info(url, download=True)
                        indirilen_dosya = ydl.prepare_filename(info)
                        
                        # Eğer MP3 ise uzantıyı düzelt
                        if format_secim == "Müzik (MP3)":
                            indirilen_dosya = os.path.splitext(indirilen_dosya)[0] + ".mp3"

                        # Kullanıcıya indirme butonunu göster
                        with open(indirilen_dosya, "rb") as f:
                            btn = st.download_button(
                                label="📥 DOSYAYI CİHAZINA KAYDET",
                                data=f,
                                file_name=os.path.basename(indirilen_dosya),
                                mime="video/mp4" if format_secim == "Video (MP4)" else "audio/mpeg"
                            )
                        
                        st.success(f"'{info['title']}' başarıyla hazırlandı!")
                        
                        # AI Analiz Bölümü
                        st.markdown("---")
                        st.subheader("🤖 AI Video Analizi")
                        prompt = f"Şu videoyu 3 kısa maddede özetle: {info.get('title')} {info.get('description')[:300]}"
                        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                        summary = res.choices[0].message.content
                        st.info(summary)

            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
                st.info("İpucu: Eğer 403 hatası alıyorsanız, YouTube bazen bulut sunucularını engelleyebilir. Birkaç dakika sonra tekrar deneyin.")
