import streamlit as st
from supabase import create_client, Client

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SUPABASE BAĞLANTISI
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        return None

supabase = init_connection()

# 3. GÖRSEL TASARIM (Beyaz Kutular, Siyah Yazılar, Belirgin Etiketler)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp { background-color: #FAF9F6; font-family: 'Inter', sans-serif; color: #2A2A2A; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif; font-weight: 700; color: #1A1A1A; }
    .hero-title { text-align: center; font-size: 3.5rem; margin-top: 2rem; margin-bottom: 0.5rem; }
    
    /* GİRİŞ KUTULARI VE ETİKET TASARIMLARI */
    
    /* Üstteki Başlıkların (Tarih, Başlık vb.) Simsiyah ve Görünür Olması */
    label, p.st-emotion-cache-1wivap2 {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    /* Kutucukların Bembeyaz Olması ve Gri Çerçeve */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="textarea"] > textarea, 
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 6px !important; /* Hafif yuvarlak klasik köşe */
        border: 1px solid #A0A0A0 !important; 
    }
    
    /* İçine Yazılan Yazıların Simsiyah Olması */
    input, textarea, .stSelectbox span {
        color: #000000 !important;
    }
    
    /* Buton Tasarımı */
    .stButton>button, .stFormSubmitButton>button {
        border-radius: 6px !important;
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    .timeline-card { background-color: #FFFFFF; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 25px; border-left: 4px solid #D4AF37; }
    .timeline-date { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #D4AF37; font-weight: bold; }
    .note-card { background-color: #F3F1EB; padding: 15px 20px; border-radius: 8px; margin-bottom: 12px; border-left: 3px solid #2A2A2A; }
    </style>
""", unsafe_allow_html=True)

# Veritabanı Uyarı Mesajı
if supabase is None:
    st.error("⚠️ Veritabanı bağlantısı şu an aktif değil. Aşağıdaki adımları uygulayarak terminal klasörünü düzelt.")

# 4. ŞİFRE KORUMASI (Şifre: 2306)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 class='hero-title'>Bizim Alanımız</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("Giriş Şifresi", type="password")
        if st.button("Giriş Yap"):
            if password == "2306":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Hatalı şifre.")
    st.stop()

# 5. ANA SAYFA VE İÇERİKLER
st.markdown("<h1 class='hero-title'>İlayda & Berkhan</h1>", unsafe_allow_html=True)
st.write("---")

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("### ⏳ Zaman Tüneli")
    
    if supabase is not None:
        try:
            response_timeline = supabase.table("zaman_tuneli").select("*").order("id", descending=False).execute()
            anilar = response_timeline.data
            
            if not anilar:
                st.info("Zaman tüneli şu an boş. Sayfanın en altındaki panelden yeni bir anı ekleyebilirsin.")
            
            for ani in anilar:
                st.markdown(f"""
                    <div class='timeline-card'>
                        <span class='timeline-date'>{ani['tarih']}</span>
                        <h4>{ani['baslik']}</h4>
                        <p>{ani['detay']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if ani['gorsel_linki']:
                    if ani['gorsel_linki'].endswith(('.mp4', '.mov')):
                        st.video(ani['gorsel_linki'])
                    else:
                        st.image(ani['gorsel_linki'], width='stretch')
                st.write("")
        except Exception as e:
            st.error("Zaman tüneli tablosu bulunamadı. Supabase'i kontrol et.")
    else:
        st.warning("Veritabanı bağlı olmadığı için anılar yüklenemiyor.")

with right_col:
    st.markdown("### 🎵 Fon Müziğimiz")
    st.info("Müzik çalar buraya eklenecek.")
    st.write("---")
    
    st.markdown("### ✍️ Anı Kavanozu")
    yazar = st.selectbox("Yazan Seçimi", ["Berkhan", "İlayda"])
    yeni_not = st.text_area("Mesajını Buraya Yaz", max_chars=500)
    
    if st.button("Kavanoza At"):
        if supabase is None:
            st.error("Veritabanı bağlı değil.")
        elif yeni_not.strip() != "":
            try:
                supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": yeni_not.strip()}).execute()
                st.rerun()
            except Exception as e:
                st.error("Not kaydedilemedi.")
                
    st.write("")
    if supabase is not None:
        try:
            response_notes = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).execute()
            for n in response_notes.data:
                st.markdown(f"<div class='note-card'><strong>{n['yazar']}:</strong> \"{n['metin']}\"</div>", unsafe_allow_html=True)
        except:
            pass

st.write("---")

# 6. İÇERİK EKLEME PANELİ
st.markdown("### ⚙️ Site Yönetim Paneli (Yeni Anı Ekle)")

with st.form("yeni_ani_formu", clear_on_submit=True):
    yeni_tarih = st.text_input("Tarih (Örn: 16 Ağustos 2024)")
    yeni_baslik = st.text_input("Başlık (Örn: İlk Buluşma)")
    yeni_detay = st.text_area("Anının Detayları...")
    yeni_gorsel = st.text_input("Fotoğraf veya Video Linki (Varsa URL yapıştır)")
    
    kaydet_butonu = st.form_submit_button("Sisteme Kaydet ve Siteyi Güncelle")
    
    if kaydet_butonu:
        if supabase is None:
            st.error("⚠️ Veritabanı bağlantısı yok! Kayıt yapılamaz.")
        elif yeni_tarih and yeni_baslik and yeni_detay:
            try:
                supabase.table("zaman_tuneli").insert({
                    "tarih": yeni_tarih,
                    "baslik": yeni_baslik,
                    "detay": yeni_detay,
                    "gorsel_linki": yeni_gorsel
                }).execute()
                st.success("Anı başarıyla eklendi! Görmek için F5 yapabilirsin.")
            except Exception as e:
                st.error("Kaydedilirken hata oluştu.")
        else:
            st.warning("Lütfen Tarih, Başlık ve Detay kısımlarını boş bırakma.")
