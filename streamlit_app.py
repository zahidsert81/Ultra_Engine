import streamlit as st
import yt_dlp
import os
import tempfile
from deep_translator import GoogleTranslator
from groq import Groq

# Groq AI
client = Groq(api_key="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")

st.set_page_config(page_title="Ultra Motor AI Pro", page_icon="🚀", layout="wide")

# --- CSS: Arayüzü Güzelleştirelim ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #38bdf8; color: black; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #22c55e; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DİL SEÇİMİ ---
lang = st.sidebar.selectbox("Language / Dil", ["Turkish", "English"])
texts = {
    "Turkish": {
        "t": "🚀 ULTRA ENGİNE PRO AI", 
        "l": "Video/Ses Linki:", 
        "f": "Format Seçin:", 
        "b": "OPERASYONU BAŞLAT", 
        "s": "📥 DOSYAYI İNDİR", 
        "ai": "🤖 Yapay Zeka Analiz Raporu",
        "cookie_err": "⚠️ Çerez dosyası (cookies.txt) bulunamadı! YouTube engeliyle karşılaşabilirsiniz."
    },
    "English": {
        "t": "🚀 ULTRA ENGINE PRO AI", 
        "l": "Video/Audio Link:", 
        "f": "Select Format:", 
        "b": "START OPERATION", 
        "s": "📥 DOWNLOAD FILE", 
        "ai": "🤖 AI Analysis Report",
        "cookie_err": "⚠️ Cookie file (cookies.txt) not found! You may face YouTube blocks."
    }
}
T = texts[lang]

st.title(T["t"])
st.write("Instagram, YouTube (Cookies Destekli), TikTok ve 1000+ site desteklenir.")
st.markdown("---")

# Yan Panel: Sistem Durumu
if not os.path.exists("www.youtube.com_cookies.txt"):
    st.sidebar.error(T["cookie_err"])
else:
    st.sidebar.success("✅ YouTube Cookies Active")

# Ana Arayüz
col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(T["l"], placeholder="https://...")
    fmt = st.selectbox(T["f"], ["Video (MP4)", "Müzik (MP3)"])
    start_btn = st.button(T["b"])

if start_btn:
    if not url:
        st.warning("Link boş olamaz!")
    else:
        with st.spinner("Sunucu işlem yapıyor..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'nocheckcertificate': True,
                        'quiet': True,
                        'no_warnings': True,
                        'cookiefile': 'www.youtube.com_cookies.txt', # Senin yüklediğin dosya 
                        'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        }
                    }

                    if fmt == "Müzik (MP3)":
                        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        fpath = ydl.prepare_filename(info)
                        if fmt == "Müzik (MP3)": fpath = os.path.splitext(fpath)[0] + ".mp3"

                        with col1:
                            st.success(f"✅ {info['title']}")
                            with open(fpath, "rb") as f:
                                st.download_button(T["s"], f, file_name=os.path.basename(fpath))
                        
                        # AI Analiz Bölümü
                        with col2:
                            st.subheader(T["ai"])
                            # Daha gelişmiş AI promptu
                            ai_prompt = f"""
                            Analyze this content:
                            Title: {info.get('title')}
                            Description: {info.get('description', '')[:500]}
                            Tasks:
                            1. Summarize in 3 bullet points.
                            2. Suggest 5 trending hashtags.
                            3. Identify the main category.
                            """
                            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":ai_prompt}])
                            raw_ai = res.choices[0].message.content
                            
                            target_l = 'tr' if lang == "Turkish" else 'en'
                            translated_ai = GoogleTranslator(source='auto', target=target_l).translate(raw_ai)
                            st.info(translated_ai)

            except Exception as e:
                st.error(f"Kritik Hata: {str(e)}")
                if "403" in str(e):
                    st.info("YouTube çerezleri yenilenmeli veya video bölge kısıtlamalı olabilir.")
