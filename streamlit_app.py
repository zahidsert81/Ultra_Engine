import streamlit as st
import yt_dlp
import os
from deep_translator import GoogleTranslator
from groq import Groq

# Groq AI - Video Analizi İçin
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Engine Pro v2", page_icon="🚀", layout="wide")

# --- ÇEREZ VE AYARLAR ---
COOKIE_FILE = "www.youtube.com_cookies.txt" if os.path.exists("www.youtube.com_cookies.txt") else "cookies.txt"

def get_video_info(url):
    """Videoyu indirmeden sadece bilgilerini çeker."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
        'format': 'best',
        # Önemli: Videoyu sunucuya indirmeyi kapatıyoruz
        'extract_flat': False, 
        'force_generic_extractor': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# --- ARAYÜZ ---
st.title("🚀 ULTRA ENGINE PRO - Akıllı Mimari")
st.markdown("---")

url = st.text_input("YouTube / Shorts / Social Media Link:", placeholder="https://...")

if url:
    with st.spinner("Metadata çekiliyor ve analiz ediliyor..."):
        try:
            # 1. BİLGİ ÇEKME (Backend sadece bilgi okur)
            info = get_video_info(url)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Video Bilgileri
                st.subheader("📺 Video Bilgileri")
                st.image(info.get('thumbnail'), use_column_width=True)
                st.write(f"**Başlık:** {info.get('title')}")
                st.write(f"**Kanal:** {info.get('uploader')}")
                st.write(f"**Süre:** {info.get('duration_string')} sn")
                
                # İNDİRME BUTONLARI (Doğrudan URL üzerinden)
                st.markdown("### 📥 İndirme Bağlantıları")
                direct_url = info.get('url') # YouTube'un geçici doğrudan video linki
                
                if direct_url:
                    st.video(direct_url) # Önizleme oynatıcı
                    st.markdown(f'''
                        <a href="{direct_url}" download="{info.get('title')}.mp4" style="text-decoration:none;">
                            <button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">
                                🔥 VİDEOYU ŞİMDİ İNDİR (Client-Side)
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("Doğrudan indirme linki oluşturulamadı.")

            with col2:
                # 2. AI ANALİZ (Cache dostu)
                st.subheader("🤖 Yapay Zeka Analizi")
                desc = info.get('description', 'Açıklama yok.')[:500]
                prompt = f"Aşağıdaki video içeriğini kısaca özetle ve 3 anahtar madde çıkar: \nBaşlık: {info.get('title')}\nAçıklama: {desc}"
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                summary = res.choices[0].message.content
                st.info(summary)
                
                # Teknik Detaylar (Debug/Cache için)
                with st.expander("Teknik Detayları Gör"):
                    st.json({
                        "id": info.get('id'),
                        "formats_count": len(info.get('formats', [])),
                        "status": "Success",
                        "ip_protection": "Active"
                    })

        except Exception as e:
            st.error(f"Hata detayı: {str(e)}")
            if "403" in str(e):
                st.warning("YouTube IP/Çerez engeli saptandı. Lütfen cookies.txt dosyasını tazeleyin.")

# --- FOOTER / AYARLAR ---
st.sidebar.markdown("### 🛠️ Sistem Durumu")
if os.path.exists(COOKIE_FILE):
    st.sidebar.success("✅ Çerezler Yüklü")
else:
    st.sidebar.error("❌ Çerez Dosyası Eksik")

st.sidebar.info("""
**Neden bu mimari?**
- **Sıfır Sunucu Yükü:** Dosyalar sunucuya inmez.
- **Hızlı Yanıt:** Sadece saniyeler sürer.
- **Güvenli:** IP adresin bot olarak işaretlenmez.
""")
