import streamlit as st
import datetime
from supabase import create_client, Client

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SUPABASE BAĞLANTISI (Aynı kalıyor, dokunmana gerek yok)
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error("Veritabanı bağlantısı kurulamadı. Lütfen ayarları kontrol edin.")

# 3. GÖRSEL TASARIM (CSS - Sadece stiller, yazı yok)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp {
        background-color: #FAF9F6;
        font-family: 'Inter', sans-serif;
        color: #2A2A2A;
    }
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #1A1A1A;
    }
    .hero-title {
        text-align: center;
        font-size: 3.5rem;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        font-style: italic;
        color: #707070;
        margin-bottom: 3rem;
    }
    .timeline-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        margin-bottom: 25px;
        border-left: 4px solid #D4AF37;
    }
    .timeline-date {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #D4AF37;
        font-weight: bold;
    }
    .note-card {
        background-color: #F3F1EB;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# 4. ŞİFRE KORUMASI (Şifre 2306 olarak güncellendi)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 class='hero-title'>Bizim Alanımız</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Giriş yapmak için şifremizi gir.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("Giriş Şifresi", type="password")
        if st.button("Giriş Yap"):
            if password == "2306":  # YENİ ŞİFREN BURADA
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı şifre, lütfen tekrar dene.")
    st.stop()

# 5. ANA SAYFA İÇERİĞİ BAŞLIKLARI
st.markdown("<h1 class='hero-title'>İlayda & Berkhan</h1>", unsafe_allow_html=True)

# ALT BAŞLIK EKLEME YERİ
st.markdown("<p class='hero-subtitle'>Buraya kendi alt başlık yazını ekleyebilirsin.</p>", unsafe_allow_html=True)

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    # BUGÜNÜN HATIRASI BÖLÜMÜ
    st.markdown("### 🌟 Bugünün Hatırası")
    
    # METİN EKLEME YERİ: Aşağıdaki tırnak içine yazını yaz
    st.write("Buraya bugüne özel notunu veya genel bir metin yazabilirsin.")
    
    # VİDEO EKLEME YERİ: Kendi videonun adını tırnak içine yaz (örn: "bizim_video.mp4")
    # st.video("video_dosyasinin_adi.mp4") 

    st.write("---")

    # ZAMAN TÜNELİ BÖLÜMÜ
    st.markdown("### ⏳ Zaman Tüneli")
    
    # FOTOĞRAF VE ANI EKLEME YERİ
    timeline_events = [
        {
            "tarih": "Tarihi Buraya Yaz",
            "baslik": "Başlığı Buraya Yaz",
            "detay": "Açıklamayı ve anınızı buraya yaz.",
            "gorsel": "" # Fotoğraf adını buraya yaz (örn: "ilk_bulusma.jpg")
        },
        # Yeni bir anı eklemek istersen yukarıdaki süslü parantezli bloğu kopyalayıp buraya yapıştırabilirsin.
    ]
    
    for event in timeline_events:
        st.markdown(f"""
            <div class='timeline-card'>
                <span class='timeline-date'>{event['tarih']}</span>
                <h4>{event['baslik']}</h4>
                <p>{event['detay']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Eğer gorsel kısmına bir şey yazarsan fotoğrafı ekranda gösterir
        if event['gorsel'] != "":
            st.image(event['gorsel'], width='stretch')
        st.write("")

with right_col:
    # MÜZİK KUTUSU BÖLÜMÜ
    st.markdown("### 🎵 Fon Müziğimiz")
    
    # SPOTIFY LINK EKLEME YERİ
    spotify_embed = """
    """
    st.markdown(spotify_embed, unsafe_allow_html=True)
    
    st.write("---")
    
    # ANI KAVANOZU (Burası Supabase'e bağlı, dokunmana gerek yok)
    st.markdown("### ✍️ Anı Kavanozu")
    
    yazar = st.selectbox("Yazan", ["Berkhan", "İlayda"])
    yeni_not = st.text_area("Mesajın...", placeholder="Kısa bir cümle ya da upuzun bir paragraf...", max_chars=500)
    
    if st.button("Kavanoza At"):
        if yeni_not.strip() != "":
            try:
                supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": yeni_not.strip()}).execute()
                st.success("Notumuz kavanoza eklendi! ✨")
                st.rerun()
            except Exception as e:
                st.error("Not kaydedilirken bir hata oluştu.")
                
    st.write("")
    st.markdown("<h4>📜 Son Bırakılan Notlar</h4>", unsafe_allow_html=True)
    try:
        response = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).execute()
        notlar = response.data
        
        for n in notlar:
            st.markdown(f"""
                <div class='note-card'>
                    <strong>{n['yazar']}:</strong> "{n['metin']}"
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.write("Henüz bir not eklenmedi.")
