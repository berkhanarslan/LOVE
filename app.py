import streamlit as st
import datetime
from supabase import create_client, Client
import uuid

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="🌿",
    layout="wide"
)

# 2. SUPABASE BAĞLANTISI
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase: Client = init_connection()

# 3. GÖRSEL TASARIM (CSS) - YENİ NESİL ŞEFFAF TASARIM
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    /* Arka plan: Mavi ve Yeşil soft geçiş */
    .stApp { 
        background: linear-gradient(135deg, #e0f2f1 0%, #e1f5fe 100%);
        font-family: 'Inter', sans-serif; 
        color: #1c313a; /* Siyah yerine koyu lacivert/gri tonu */
    }
    
    /* Başlık Renkleri */
    h1, h2, h3, h4 { 
        font-family: 'Playfair Display', serif; 
        color: #004d40; /* Koyu orman yeşili */
    }
    
    /* Şeffaf Beyaz ve Yuvarlak Köşeli Kutular (Glassmorphism) */
    .quote-card, .timeline-card, .note-card {
        background: rgba(255, 255, 255, 0.6); /* Yarı şeffaf beyaz */
        backdrop-filter: blur(10px); /* Arka planı hafif flulaştırır */
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px; /* Yumuşak, yuvarlak köşeler */
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(0, 77, 64, 0.05); /* Çok hafif yeşilimsi gölge */
    }
    
    /* Streamlit'in kendi input (girdi) alanlarını da yuvarlak yapalım */
    div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {
        border-radius: 15px !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(0, 150, 136, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. ŞİFRE KORUMASI
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align:center; color:#00695c;'>🌿 Bizim Alanımız</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="Şifre")
        if st.button("Giriş"):
            if password == "1608":
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- YARDIMCI FONKSİYONLAR ---
def upload_image(file):
    file_extension = file.name.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    storage_path = f"photos/{file_name}"
    res = supabase.storage.from_("media").upload(storage_path, file.getvalue())
    return supabase.storage.from_("media").get_public_url(storage_path)

# --- ANA İÇERİK ---
st.title("🌿 İlayda & Berkhan")

# 5. GÜNÜN SÖZÜ
try:
    last_note = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).limit(1).execute()
    if last_note.data:
        note = last_note.data[0]
        st.markdown(f"""
            <div class='quote-card' style='text-align: center; padding: 30px;'>
                <h2 style='font-style: italic; color: #00695c;'>"{note['metin']}"</h2>
                <p style='text-align: right; color: #546e7a; margin-top: 10px;'>— {note['yazar']}</p>
            </div>
        """, unsafe_allow_html=True)
except:
    pass # Hata verirse veya boşsa ekranda kalabalık yapmasın, sessizce geçsin

tab1, tab2, tab3 = st.tabs(["⏳ Anılar", "🍯 Notlar", "📸 Yeni Ekle"])

# TAB 1: ZAMAN TÜNELİ
with tab1:
    try:
        memories = supabase.table("zaman_tuneli").select("*").order("tarih", descending=True).execute()
        for m in memories.data:
            col_text, col_img = st.columns([2, 1])
            with col_text:
                st.markdown(f"""
                    <div class='timeline-card'>
                        <p style='color:#00897b; font-weight:600; font-size:0.9em; margin-bottom:5px;'>{m['tarih']}</p>
                        <h4 style='margin-top:0;'>{m['baslik']}</h4>
                        <p style='color:#37474f;'>{m['detay']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_img:
                if m.get('resim_url'):
                    st.image(m['resim_url'], use_container_width=True)
    except Exception as e:
        st.error("Bir sorun oluştu.")

# TAB 2: ANI KAVANOZU
with tab2:
    with st.expander("✨ Yeni Not", expanded=True):
        yazar = st.radio("", ["İlayda", "Berkhan"], horizontal=True, label_visibility="collapsed")
        mesaj = st.text_area("", placeholder="İçinden gelenler...")
        if st.button("Gönder"):
            if mesaj:
                supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": mesaj}).execute()
                st.rerun()

    st.write("") # Boşluk
    all_notes = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).execute()
    for n in all_notes.data:
        st.markdown(f"""
            <div class='note-card'>
                <strong style='color:#00695c;'>{n['yazar']}:</strong> <span style='color:#263238;'>{n['metin']}</span>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: YENİ ANI EKLE
with tab3:
    with st.form("yeni_ani_formu", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        baslik = st.text_input("Başlık", placeholder="O günün adı...")
        detay = st.text_area("Detay", placeholder="Kısaca anlat...")
        yuklenen_resim = st.file_uploader("Fotoğraf (İsteğe bağlı)", type=["jpg", "png", "jpeg"])
        
        submit = st.form_submit_button("Kaydet")
        
        if submit:
            if baslik and detay:
                resim_url = ""
                if yuklenen_resim:
                    with st.spinner("Yükleniyor..."):
                        resim_url = upload_image(yuklenen_resim)
                
                supabase.table("zaman_tuneli").insert({
                    "tarih": str(tarih),
                    "baslik": baslik,
                    "detay": detay,
                    "resim_url": resim_url
                }).execute()
                st.success("Kaydedildi! ✨")
                st.rerun()
            else:
                st.warning("Başlık ve detay gerekli.")
