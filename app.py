import streamlit as st
import datetime
from supabase import create_client, Client
import uuid

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="🤍",
    layout="wide"
)

# 2. SUPABASE BAĞLANTISI
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase: Client = init_connection()

# 3. GÖRSEL TASARIM (CSS) - BEYAZ ARKA PLAN & SİYAH YAZILAR & TURKUAZ BUTONLAR
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    /* Arka plan bembeyaz, ana yazılar siyah */
    .stApp { 
        background-color: #ffffff !important;
        font-family: 'Inter', sans-serif; 
        color: #000000 !important; 
    }
    
    /* Tüm başlıklar siyah ve şık font */
    h1, h2, h3, h4, h5, h6, p, span, div { 
        font-family: 'Inter', sans-serif;
        color: #000000 !important; 
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }
    
    /* Kart tasarımları (Hafif gri tonlu/gölgeli beyaz kutular) */
    .quote-card, .timeline-card, .note-card {
        background-color: #fcfcfc !important;
        border-radius: 20px; 
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #eeeeee !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04); 
    }
    
    /* İNPUT (METİN GİRİŞ) KUTULARI - Beyaz arka plan, siyah yazı */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"],
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important; 
        border-radius: 12px !important;
        border: 1px solid #cccccc !important; 
    }
    
    input, textarea {
        background-color: transparent !important;
        color: #000000 !important; 
    }

    /* BUTONLAR - Yeşil/Mavi/Turkuaz Karışımı */
    div[data-testid="stButton"] > button, 
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #06beb6 0%, #48b1bf 100%) !important; /* Turkuaz/Mavi geçiş */
        color: #ffffff !important; /* Buton içi yazı beyaz kalsın ki okunsun */
        border: none !important;
        border-radius: 15px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(6, 190, 182, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Butonun üzerine gelince büyüme efekti */
    div[data-testid="stButton"] > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(6, 190, 182, 0.5) !important;
    }
    
    /* Sekme (Tab) yazılarının siyah olması */
    button[data-baseweb="tab"] {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. ŞİFRE KORUMASI
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align:center;'>🤍 Bizim Alanımız</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="Şifre")
        if st.button("Giriş Yap"):
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
st.title("🤍 İlayda & Berkhan")

# 5. GÜNÜN SÖZÜ
try:
    # HATA BURADA ÇÖZÜLDÜ: descending=True yerine desc=True kullanıldı.
    last_note = supabase.table("ani_kavanozu").select("*").order("created_at", desc=True).limit(1).execute()
    if last_note.data:
        note = last_note.data[0]
        st.markdown(f"""
            <div class='quote-card' style='text-align: center; padding: 30px;'>
                <h2 style='font-style: italic;'>"{note['metin']}"</h2>
                <p style='text-align: right; margin-top: 10px; font-weight: bold;'>— {note['yazar']}</p>
            </div>
        """, unsafe_allow_html=True)
except:
    pass 

tab1, tab2, tab3 = st.tabs(["⏳ Anılar", "🍯 Notlar", "📸 Yeni Ekle"])

# TAB 1: ZAMAN TÜNELİ
with tab1:
    try:
        # HATA BURADA ÇÖZÜLDÜ: desc=True
        memories = supabase.table("zaman_tuneli").select("*").order("tarih", desc=True).execute()
        for m in memories.data:
            col_text, col_img = st.columns([2, 1])
            with col_text:
                st.markdown(f"""
                    <div class='timeline-card'>
                        <p style='font-weight:600; font-size:0.9em; margin-bottom:5px; color:#48b1bf !important;'>{m['tarih']}</p>
                        <h4 style='margin-top:0;'>{m['baslik']}</h4>
                        <p>{m['detay']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_img:
                if m.get('resim_url'):
                    st.image(m['resim_url'], use_container_width=True)
    except Exception as e:
        st.error("Anılar yüklenirken bir sorun oluştu.")

# TAB 2: ANI KAVANOZU
with tab2:
    with st.expander("✨ Yeni Not Ekle", expanded=True):
        yazar = st.radio("", ["İlayda", "Berkhan"], horizontal=True, label_visibility="collapsed")
        mesaj = st.text_area("", placeholder="İçinden geçenleri yaz...")
        if st.button("Kavanoza Bırak"):
            if mesaj:
                supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": mesaj}).execute()
                st.rerun()

    st.write("")
    # HATA BURADA ÇÖZÜLDÜ: desc=True
    all_notes = supabase.table("ani_kavanozu").select("*").order("created_at", desc=True).execute()
    for n in all_notes.data:
        st.markdown(f"""
            <div class='note-card'>
                <strong>{n['yazar']}:</strong> <span>{n['metin']}</span>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: YENİ ANI EKLE
with tab3:
    with st.form("yeni_ani_formu", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        baslik = st.text_input("Başlık", placeholder="O günün adı...")
        detay = st.text_area("Detay", placeholder="Kısaca o günü anlat...")
        yuklenen_resim = st.file_uploader("Fotoğraf Ekle (İsteğe bağlı)", type=["jpg", "png", "jpeg"])
        
        submit = st.form_submit_button("Anıyı Kaydet")
        
        if submit:
            if baslik and detay:
                resim_url = ""
                if yuklenen_resim:
                    with st.spinner("Fotoğraf Yükleniyor..."):
                        resim_url = upload_image(yuklenen_resim)
                
                supabase.table("zaman_tuneli").insert({
                    "tarih": str(tarih),
                    "baslik": baslik,
                    "detay": detay,
                    "resim_url": resim_url
                }).execute()
                st.success("Anı başarıyla kaydedildi! ✨")
                st.rerun()
            else:
                st.warning("Lütfen başlık ve detay alanlarını doldurunuz.")
