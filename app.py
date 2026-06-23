import streamlit as st
import datetime
from datetime import timedelta, timezone
from supabase import create_client, Client
import uuid
import requests
from PIL import Image, ImageOps  # YENİ: ImageOps eklendi
import io

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

# 3. GÖRSEL TASARIM (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp { background-color: #ffffff !important; font-family: 'Inter', sans-serif; color: #000000 !important; }
    h1, h2, h3, h4, h5, h6, p, span, div { font-family: 'Inter', sans-serif; color: #000000 !important; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
    
    .quote-card, .timeline-card, .note-card {
        background-color: #fcfcfc !important; border-radius: 20px; padding: 20px; margin-bottom: 20px;
        border: 1px solid #eeeeee !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04); 
    }
    
    div[data-baseweb="input"] > div, div[data-baseweb="base-input"], div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important; border-radius: 12px !important; border: 1px solid #cccccc !important; 
    }
    
    input, textarea { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
    input::placeholder, textarea::placeholder { color: #888888 !important; -webkit-text-fill-color: #888888 !important; }

    [data-testid="stFileUploaderDropzone"] { background-color: #ffffff !important; border: 2px dashed #06beb6 !important; border-radius: 15px !important; }
    [data-testid="stFileUploaderDropzone"] * { color: #000000 !important; }

    div[data-testid="stButton"] > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #06beb6 0%, #48b1bf 100%) !important; 
        color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: none !important;
        border-radius: 15px !important; padding: 10px 25px !important; font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(6, 190, 182, 0.3) !important; transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important; box-shadow: 0 6px 15px rgba(6, 190, 182, 0.5) !important;
    }
    
    hr { border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(6, 190, 182, 0.2), rgba(0, 0, 0, 0)); margin: 30px 0; }
    </style>
""", unsafe_allow_html=True)

# 4. ŞİFRE KORUMASI VE OTURUM HATIRLAMA
if st.query_params.get("token") == "bizim_alanimiz_2306":
    st.session_state['authenticated'] = True
elif 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align:center;'>🤍 Bizim Alanımız</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="Şifre")
        if st.button("Giriş Yap"):
            if password == "2306":
                st.session_state['authenticated'] = True
                st.query_params["token"] = "bizim_alanimiz_2306"
                st.rerun()
            else:
                st.error("Hatalı şifre.")
    st.stop()

# --- YARDIMCI FONKSİYONLAR ---
def upload_media(file):
    """Dosyanın türünü algılar; fotoğrafsa sıkıştırır ve düzeltir, videoyasa doğrudan yükler."""
    file_extension = file.name.split(".")[-1].lower()
    
    # EĞER VİDEO İSE DOĞRUDAN YÜKLE
    if file_extension in ['mp4', 'mov', 'avi']:
        file_name = f"{uuid.uuid4()}.{file_extension}"
        storage_path = f"photos/{file_name}"
        supabase.storage.from_("media").upload(
            path=storage_path, 
            file=file.getvalue(), 
            file_options={"content-type": file.type}
        )
        return supabase.storage.from_("media").get_public_url(storage_path)
        
    # EĞER FOTOĞRAF İSE PİLLOW İLE OPTİMİZE ET
    else:
        image = Image.open(file)
        
        # YENİ: Telefondan gelen fotoğrafların yönünü (EXIF) düzeltir
        image = ImageOps.exif_transpose(image)
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        max_width = 1080
        if image.width > max_width:
            oran = max_width / float(image.width)
            yeni_boyut = (max_width, int(float(image.height) * float(oran)))
            image = image.resize(yeni_boyut, Image.Resampling.LANCZOS)
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
        img_byte_arr = img_byte_arr.getvalue()

        file_name = f"{uuid.uuid4()}.jpg"
        storage_path = f"photos/{file_name}"
        
        supabase.storage.from_("media").upload(
            path=storage_path, 
            file=img_byte_arr, 
            file_options={"content-type": "image/jpeg"}
        )
        return supabase.storage.from_("media").get_public_url(storage_path)

def send_telegram_notification(yazar, metin):
    try:
        bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        
        if bot_token and chat_id:
            mesaj = f"💌 {yazar} kavanoza yeni bir not bıraktı:\n\n{metin}"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": mesaj})
    except Exception:
        pass 

# --- ANA İÇERİK ---
st.title("🤍 İlayda & Berkhan")

# Son 24 Saati Hesaplama
son_24_saat = (datetime.datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

# 5. GÜNÜN SÖZÜ
try:
    last_note = supabase.table("ani_kavanozu").select("*").gte("created_at", son_24_saat).order("created_at", desc=True).limit(1).execute()
    if last_note.data:
        note = last_note.data[0]
        # ŞİİR FORMATI: Satır atlamalarını HTML <br> etiketine çeviriyoruz
        formatli_metin = note['metin'].replace('\n', '<br>')
        
        st.markdown(f"""
            <div class='quote-card' style='text-align: center; padding: 30px;'>
                <h2 style='font-style: italic;'>"{formatli_metin}"</h2>
                <p style='text-align: right; margin-top: 10px; font-weight: bold;'>— {note['yazar']}</p>
            </div>
        """, unsafe_allow_html=True)
except:
    pass 

tab1, tab2, tab3, tab4 = st.tabs(["⏳ Anılar", "🍯 Notlar", "📸 Yeni Ekle", "🎵 Müzik"])

# TAB 1: ZAMAN TÜNELİ
with tab1:
    st.write("")
    siralama = st.radio(
        "Sıralama Seçimi", 
        ["🔽 En Yeniden En Eskiye", "🔼 En Eskiden En Yeniye"], 
        horizontal=True, 
        label_visibility="collapsed"
    )
    
    is_descending = True if "🔽" in siralama else False
    st.write("")

    try:
        memories = supabase.table("zaman_tuneli").select("*").order("tarih", desc=is_descending).execute()
        
        for m in memories.data:
            col_text, col_media = st.columns([2, 1])
            with col_text:
                st.markdown(f"""
                    <div class='timeline-card'>
                        <p style='font-weight:600; font-size:0.9em; margin-bottom:5px; color:#48b1bf !important;'>{m['tarih']}</p>
                        <h4 style='margin-top:0;'>{m['baslik']}</h4>
                        <p>{m['detay']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col_media:
                medya_url = m.get('gorsel_linki')
                if medya_url:
                    if medya_url.lower().endswith(('.mp4', '.mov', '.avi')):
                        st.video(medya_url)
                    else:
                        st.image(medya_url, use_container_width=True)
            
            with st.expander("✏️ Fotoğraf/Video Değiştir", expanded=False):
                yeni_medya = st.file_uploader("Yeni bir kare/video seç", type=["jpg", "png", "jpeg", "mp4", "mov"], key=f"up_{m['id']}")
                if st.button("Güncelle", key=f"btn_{m['id']}"):
                    if yeni_medya:
                        with st.spinner("Medya yükleniyor..."):
                            yeni_url = upload_media(yeni_medya)
                            supabase.table("zaman_tuneli").update({"gorsel_linki": yeni_url}).eq("id", m['id']).execute()
                        st.success("İçerik başarıyla değiştirildi! ✨")
                        st.rerun()
                    else:
                        st.warning("Lütfen yüklemek için bir dosya seç.")
            
            with st.expander("🗑️ Anıyı Sil", expanded=False):
                st.warning("Bu anıyı tamamen silmek istediğine emin misin? Bu işlem geri alınamaz.")
                if st.button("Evet, Anıyı Sil", key=f"del_{m['id']}"):
                    try:
                        supabase.table("zaman_tuneli").delete().eq("id", m['id']).execute()
                        st.success("Anı başarıyla silindi!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Silinirken bir hata oluştu: {e}")
            
            st.markdown("<hr>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Anılar yüklenirken bir sorun oluştu: {e}")

# TAB 2: ANI KAVANOZU
with tab2:
    with st.expander("✨ Yeni Not Ekle", expanded=True):
        yazar = st.radio("", ["İlayda", "Berkhan"], horizontal=True, label_visibility="collapsed")
        mesaj = st.text_area("", placeholder="İçinden geçenleri yaz...")
        if st.button("Kavanoza Bırak"):
            if mesaj:
                basarili = False
                try:
                    supabase.table("ani_kavanozu").insert({"yazar": yazar, "metin": mesaj}).execute()
                    send_telegram_notification(yazar, mesaj)
                    basarili = True
                except Exception as e:
                    st.error(f"Veritabanı hatası detayı: {e}")
                
                if basarili:
                    st.rerun()

    st.write("")
    try:
        all_notes = supabase.table("ani_kavanozu").select("*").gte("created_at", son_24_saat).order("created_at", desc=True).execute()
        
        if len(all_notes.data) == 0:
            st.info("Kavanoz şu an boş. İlk notu sen bırak! 🤍")
        else:
            for n in all_notes.data:
                # ŞİİR FORMATI: Alt alta yazılan yazıları korur
                formatli_not = n['metin'].replace('\n', '<br>')
                
                st.markdown(f"""
                    <div class='note-card'>
                        <strong>{n['yazar']}:</strong> <span>{formatli_not}</span>
                    </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Notlar şu an listelenemiyor. Hata detayı: {e}")

# TAB 3: YENİ ANI EKLE
with tab3:
    st.info("💡 **İpucu:** Telefondan yüklüyorsanız, fotoğrafı o an çekmek (Kamera) yerine **'Fotoğraf Arşivi'nden (Galeriden)** seçmeniz, bağlantının kopmasını engelleyecek ve çok daha sağlıklı yüklenecektir.")
    
    with st.form("yeni_ani_formu", clear_on_submit=True):
        tarih = st.date_input("Tarih", datetime.date.today())
        baslik = st.text_input("Başlık", placeholder="O günün adı...")
        detay = st.text_area("Detay", placeholder="Kısaca o günü anlat...")
        yuklenen_medya = st.file_uploader("Fotoğraf veya Video Ekle (İsteğe bağlı)", type=["jpg", "png", "jpeg", "mp4", "mov"])
        
        submit = st.form_submit_button("Anıyı Kaydet")
        
        if submit:
            if baslik and detay:
                basarili = False
                resim_url = ""
                try:
                    if yuklenen_medya:
                        with st.spinner("İçerik işleniyor ve yükleniyor... (Lütfen bitene kadar bekleyin)"):
                            resim_url = upload_media(yuklenen_medya)
                    
                    supabase.table("zaman_tuneli").insert({
                        "tarih": str(tarih),
                        "baslik": baslik,
                        "detay": detay,
                        "gorsel_linki": resim_url
                    }).execute()
                    basarili = True
                except Exception as e:
                    st.error(f"Kaydedilirken hata oluştu detayı: {e}")
                
                if basarili:
                    st.success("Anı başarıyla kaydedildi! ✨")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Lütfen başlık ve detay alanlarını doldurunuz.")

# TAB 4: MÜZİK
with tab4:
    st.markdown("<h3 style='color: #48b1bf; text-align: center;'>🎧 Bizim Şarkılarımız</h3>", unsafe_allow_html=True)
    st.write("Bu listede çalan her şarkı bizim bir anımıza eşlik ediyor...")
    st.write("")
    
    spotify_html = """
    <iframe style="border-radius:12px" 
    src="https://open.spotify.com/embed/playlist/2XPYlaYVuR34GWeMrkm9oy?utm_source=generator" 
    width="100%" height="450" frameBorder="0" allowfullscreen="" 
    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
    loading="lazy"></iframe>
    """
    st.markdown(spotify_html, unsafe_allow_html=True)
