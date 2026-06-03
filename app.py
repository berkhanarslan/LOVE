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
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error("Veritabanı bağlantısı kurulamadı.")

# 3. GÖRSEL TASARIM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    .stApp { background-color: #FAF9F6; font-family: 'Inter', sans-serif; color: #2A2A2A; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif; font-weight: 700; color: #1A1A1A; }
    .hero-title { text-align: center; font-size: 3.5rem; margin-top: 2rem; margin-bottom: 0.5rem; }
    .timeline-card { background-color: #FFFFFF; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02); margin-bottom: 25px; border-left: 4px solid #D4AF37; }
    .timeline-date { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #D4AF37; font-weight: bold; }
    .note-card { background-color: #F3F1EB; padding: 15px 20px; border-radius: 8px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

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
    
    # Veritabanından zaman tüneli verilerini çek
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
            
            # Eğer fotoğraf veya video linki eklenmişse göster
            if ani['gorsel_linki']:
                if ani['gorsel_linki'].endswith(('.mp4', '.mov')):
                    st.video(ani['gorsel_linki'])
                else:
                    st.image(ani['gorsel_linki'], width='stretch')
            st.write("")
    except Exception as e:
        st.error("Zaman tüneli yüklenemedi.")

with right_col:
    st.markdown("### 🎵 Fon Müziğimiz")
    # Spotify Linkini yine siteden güncelleyebilmen için bir alan yapılabilir ama şimdilik kodda durması en sağlıklısı
    st.info("Müzik çalar buraya eklenecek.")
    st.write("---")
    
    # ANI KAVANOZU (Notlar)
    st.markdown("### ✍️ Anı Kavanozu")
    yazar = st.selectbox("Yazan", ["Berkhan", "İlayda"])
    yeni_not = st.text_area("Mesajın...", max_chars=500)
    
    if st.button("Kavanoza At"):
        if yeni_not.strip() != "":
            supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": yeni_not.strip()}).execute()
            st.rerun()
                
    st.write("")
    try:
        response_notes = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).execute()
        for n in response_notes.data:
            st.markdown(f"<div class='note-card'><strong>{n['yazar']}:</strong> \"{n['metin']}\"</div>", unsafe_allow_html=True)
    except:
        pass

st.write("---")

# 6. İÇERİK EKLEME PANELİ (SİTE ÜZERİNDEN YÖNETİM)
st.markdown("### ⚙️ Site Yönetim Paneli (Yeni Anı Ekle)")
st.caption("Buradan eklediğin her şey otomatik olarak yukarıdaki Zaman Tüneline yerleşir. Koda girmene gerek kalmaz.")

with st.form("yeni_ani_formu", clear_on_submit=True):
    yeni_tarih = st.text_input("Tarih (Örn: 16 Ağustos 2024)")
    yeni_baslik = st.text_input("Başlık (Örn: İlk Buluşma)")
    yeni_detay = st.text_area("Anının Detayları, Uzun Yazı...")
    yeni_gorsel = st.text_input("Fotoğraf veya Video Linki (Varsa URL'sini yapıştır. Yoksa boş bırakabilirsin.)")
    
    kaydet_butonu = st.form_submit_button("Sisteme Kaydet ve Siteyi Güncelle")
    
    if kaydet_butonu:
        if yeni_tarih and yeni_baslik and yeni_detay:
            try:
                supabase.table("zaman_tuneli").insert({
                    "tarih": yeni_tarih,
                    "baslik": yeni_baslik,
                    "detay": yeni_detay,
                    "gorsel_linki": yeni_gorsel
                }).execute()
                st.success("Anı başarıyla eklendi! Görmek için sayfayı yenile.")
            except Exception as e:
                st.error("Kaydedilirken hata oluştu.")
        else:
            st.warning("Lütfen Tarih, Başlık ve Detay kısımlarını boş bırakma.")
