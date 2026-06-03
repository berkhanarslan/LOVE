import streamlit as st
import datetime
import pandas as pd

# 1. SAYFA YAPILANDIRMASI (Modern ve Geniş Düzen)
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ÖZEL CSS TASARIMI (Profesyonel Tipografi ve Renk Paleti)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');
    
    /* Genel Arka Plan ve Yazı Tipi */
    .stApp {
        background-color: #FAF9F6; /* Minimalist Kırık Beyaz */
        font-family: 'Inter', sans-serif;
        color: #2A2A2A;
    }
    
    /* Başlık Stilleri */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .hero-title {
        font-size: 3rem;
        text-align: center;
        margin-top: 2rem;
        color: #1A1A1A;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        font-style: italic;
        text-align: center;
        color: #707070;
        margin-bottom: 3rem;
    }
    
    /* Zaman Tüneli Kart Tasarımı */
    .timeline-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
        border-left: 4px solid #D4AF37; /* Zarif Altın Detay */
    }
    
    .timeline-date {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        color: #D4AF37;
        font-weight: bold;
    }
    
    /* Anı Kutusu Notları */
    .note-card {
        background-color: #F3F1EB;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-style: italic;
    }
    
    /* Buton Tasarımları */
    .stButton>button {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 10px 24px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GİRİŞ KONTROLÜ (Sadece İkinize Özel)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 class='hero-title'>Bizim Alanımız</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Sadece ikimize özel küçük bir dijital ev.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("Giriş Şifresi", type="password", placeholder="Özel tarihimiz...")
        if st.button("Giriş Yap"):
            # Buraya ikinizin bildiği ortak bir şifre veya tanışma yılınızı koyabilirsin
            if password == "1608": 
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı şifre, lütfen tekrar dene.")
    st.stop()

# 4. ANA SAYFA HERO BÖLÜMÜ
st.markdown("<h1 class='hero-title'>İlayda & Berkhan</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Birlikte biriktirdiğimiz tüm güzel anlar, kelimeler ve melodiler.</p>", unsafe_allow_html=True)

# Yan yana iki ana sütun oluşturuyoruz: Sol taraf içerik, Sağ taraf müzik ve anı ekleme
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    # 5. DİNAMİK GÜNÜN ANISI (Belirli Günlerde Öne Çıkan Edit)
    st.markdown("### 🌟 Bugünün Hatırası")
    bugun = datetime.date.today().strftime("%d-%m")
    
    # Özel gün senaryoları (Örn: Yıldönümü veya Doğum Günleri)
    if bugun == "03-06": # Bugünün tarihi simülasyonu
        st.info("🎉 Bugün bizim yıldönümümüz! Birlikte geçen her ana minnettarım.")
        # Buraya OneDrive veya Google Fotoğraflar'dan alacağın özel bir editi/videoyu koyabilirsin
        st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Örnek video linki
    else:
        st.markdown(
            "<div class='timeline-card'>"
            "<p class='timeline-date'>Sıradan Bir Günün Güzelliği</p>"
            "<p>Bugün takvimde özel bir dönüm noktası olmayabilir ama seninle geçen her gün zaten başlı başına bir kutlama nedeni.</p>"
            "</div>", 
            unsafe_allow_html=True
        )

    # 6. İNTERAKTİF ZAMAN TÜNELİ (Timeline)
    st.markdown("### ⏳ Zaman Tüneli")
    
    # Zaman tüneli verilerini istersen harici bir dosyadan da okutabilirsin
    timeline_events = [
        {
            "tarih": "12 Nisan 2026",
            "baslik": "Eskişehir Seyahati",
            "detay": "Kütahya üzerinden Eskişehir'e geçtiğimiz o güzel gün. Trendeki sohbetimiz ve kaçırdığımız o otobüs bile günün neşesini bozmaya yetmemişti.",
            "gorsel": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846" # Google Fotoğraflar linki ile değiştirilecek
        },
        {
            "tarih": "26 Aralık 2025",
            "baslik": "Manisa Keşfi",
            "detay": "Tarihi sokaklarda kaybolduğumuz, müze ziyaretleriyle geçen ve kış soğuğuna rağmen içimizi ısıtan o harika hafta sonu kaçamağı.",
            "gorsel": "https://images.unsplash.com/photo-1490730141103-6cac27aaab94"
        }
    ]
    
    for event in timeline_events:
        st.markdown(f"""
            <div class='timeline-card'>
                <span class='timeline-date'>{event['tarih']}</span>
                <h4>{event['baslik']}</h4>
                <p>{event['detay']}</p>
            </div>
        """, unsafe_allow_html=True)
        # İsteğe bağlı görsel ekleme
        st.image(event['gorsel'], use_container_width=True)
        st.write("")

with right_col:
    # 7. MÜZİK KUTUSU (Spotify Entegrasyonu)
    st.markdown("### 🎵 Fon Müziğimiz")
    # Kendi Spotify çalma listenizin veya şarkınızın URI/Embed kodunu buraya ekleyebilirsin
    spotify_embed_code = """
    <iframe src="https://open.spotify.com/embed/track/5QREn7A66CO4VkaN9vYw0b?utm_source=generator" 
    width="100%" height="152" frameBorder="0" allowfullscreen="" 
    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    """
    st.markdown(spotify_embed_code, unsafe_allow_html=True)
    
    st.write("---")
    
    # 8. DİJİTAL ANI KAVANOZU (Veri Gönderimi ve Depolama)
    st.markdown("### ✍️ Anı Kavanozuna Not Bırak")
    st.write("Birbirimize söylemek istediğimiz küçük cümleleri veya paragrafları buradan fırlatabiliriz.")
    
    # Streamlit üzerinde geçici depolama (Supabase entegrasyonu yapılana kadar)
    if 'notlar' not in st.session_state:
        st.session_state['notlar'] = [
            {"yazar": "Berkhan", "metin": "Bu siteyi tasarlarken sadece sana olan sevgimi değil, geleceğe bırakacağımız izleri düşündüm."},
            {"yazar": "İlayda", "metin": "Her sabah buraya yeni bir not bırakmak için uyanabilirim!"}
        ]
    
    yazar = st.selectbox("Yazan", ["Berkhan", "İlayda"])
    yeni_not = st.text_area("Mesajın...", placeholder="Kısa bir cümle ya da upuzun bir paragraf...", max_chars=500)
    
    if st.button("Kavanoza At"):
        if yeni_not.strip() != "":
            st.session_state['notlar'].insert(0, {"yazar": yazar, "metin": yeni_not})
            st.success("Notumuz kavanoza eklendi! ✨")
            st.rerun()
            
    # Notların Listelenmesi
    st.write("")
    st.markdown("#### 📜 Son Bırakılan Notlar")
    for n in st.session_state['notlar']:
        st.markdown(f"""
            <div class='note-card'>
                <strong>{n['yazar']}:</strong> "{n['metin']}"
            </div>
        """, unsafe_allow_html=True)