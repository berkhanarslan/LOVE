import streamlit as st
import datetime
from supabase import create_client, Client
import uuid

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="İlayda & Berkhan | Bizim Alanımız",
    page_icon="❤️",
    layout="wide"
)

# 2. SUPABASE BAĞLANTISI
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase: Client = init_connection()

# 3. GÖRSEL TASARIM (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp { background-color: #FAF9F6; font-family: 'Inter', sans-serif; color: #2A2A2A; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif; color: #1A1A1A; }
    
    .quote-card {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #d4af37;
        margin-bottom: 30px;
    }
    .timeline-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #D4AF37;
    }
    .note-card {
        background-color: #F3F1EB;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px dashed #D4AF37;
    }
    </style>
""", unsafe_allow_html=True)

# 4. ŞİFRE KORUMASI
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align:center;'>🔐 Bizim Alanımız</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("Giriş Şifresi", type="password")
        if st.button("Giriş Yap"):
            if password == "1608":
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- YARDIMCI FONKSİYONLAR ---
def upload_image(file):
    """Resmi Supabase Storage'a yükler ve URL döner."""
    file_extension = file.name.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    # 'media' bucket'ına yükle
    storage_path = f"photos/{file_name}"
    res = supabase.storage.from_("media").upload(storage_path, file.getvalue())
    # Public URL'yi al
    return supabase.storage.from_("media").get_public_url(storage_path)

# --- ANA İÇERİK ---
st.title("❤️ İlayda & Berkhan")

# 5. GÜNÜN SÖZÜ (En son eklenen sevgi notu)
st.markdown("### 🖋️ Günün Kalbinden")
try:
    last_note = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).limit(1).execute()
    if last_note.data:
        note = last_note.data[0]
        st.markdown(f"""
            <div class='quote-card'>
                <h2 style='font-style: italic;'>"{note['metin']}"</h2>
                <p style='text-align: right; color: #707070;'>— {note['yazar']}</p>
            </div>
        """, unsafe_allow_html=True)
except:
    st.write("Henüz bir söz bırakılmamış...")

tab1, tab2, tab3 = st.tabs(["⏳ Zaman Tünelimiz", "🍯 Anı Kavanozu", "📸 Yeni Anı Ekle"])

# TAB 1: ZAMAN TÜNELİ (LİSTELEME)
with tab1:
    st.markdown("### ⏳ Birlikte Geçen Günler")
    try:
        memories = supabase.table("zaman_tuneli").select("*").order("tarih", descending=True).execute()
        for m in memories.data:
            col_text, col_img = st.columns([2, 1])
            with col_text:
                st.markdown(f"""
                    <div class='timeline-card'>
                        <p style='color:#D4AF37; font-weight:bold;'>{m['tarih']}</p>
                        <h4>{m['baslik']}</h4>
                        <p>{m['detay']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_img:
                if m.get('resim_url'):
                    st.image(m['resim_url'], use_container_width=True)
            st.write("---")
    except Exception as e:
        st.error("Anılar yüklenirken bir hata oluştu.")

# TAB 2: ANI KAVANOZU
with tab2:
    st.markdown("### 🍯 Sevgi Kavanozu")
    
    with st.expander("✨ Yeni Not Bırak"):
        yazar = st.radio("Kimden?", ["İlayda", "Berkhan"], horizontal=True)
        mesaj = st.text_area("Mesajın...")
        if st.button("Kavanoza Gönder"):
            if mesaj:
                supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": mesaj}).execute()
                st.success("Notun kalbe ulaştı! ❤️")
                st.rerun()

    st.write("#### 📜 Geçmiş Notlar")
    all_notes = supabase.table("ani_kavanozu").select("*").order("created_at", descending=True).execute()
    for n in all_notes.data:
        st.markdown(f"""
            <div class='note-card'>
                <strong>{n['yazar']}:</strong> {n['metin']} <br>
                <small style='color:gray;'>{n['created_at'][:10]}</small>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: YENİ ANI EKLE (RESİMLİ)
with tab3:
    st.markdown("### 📸 Yeni Bir Anı Kaydet")
    with st.form("yeni_ani_formu", clear_on_submit=True):
        tarih = st.date_input("Ne zamandı?", datetime.date.today())
        baslik = st.text_input("Anının Başlığı", placeholder="Örn: İlk Akşam Yemeği")
        detay = st.text_area("Neler oldu?", placeholder="O günü kısaca anlat...")
        yuklenen_resim = st.file_uploader("O günden bir kare seç", type=["jpg", "png", "jpeg"])
        
        submit = st.form_submit_button("Anıyı Ölümsüzleştir ✨")
        
        if submit:
            if baslik and detay:
                resim_url = ""
                if yuklenen_resim:
                    with st.spinner("Resim yükleniyor..."):
                        resim_url = upload_image(yuklenen_resim)
                
                supabase.table("zaman_tuneli").insert({
                    "tarih": str(tarih),
                    "baslik": baslik,
                    "detay": detay,
                    "resim_url": resim_url
                }).execute()
                st.success("Anı başarıyla eklendi!")
                st.rerun()
            else:
                st.warning("Lütfen başlık ve detay alanlarını doldur.")
