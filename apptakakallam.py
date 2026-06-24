import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Takallam AI - Pembelajaran Maharah Kalam",
    page_icon="💬",
    layout="centered"
)

# --- STYLE CSS (Desain Modern, Elegan & Islami Khas MA) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1E4D2B; 
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .setup-box {
        background-color: #F4F7F5;
        border-radius: 15px;
        padding: 25px;
        border-left: 5px solid #1E4D2B;
        margin-bottom: 25px;
    }
    
    .arabic-text {
        font-family: 'Traditional Arabic', 'Amiri', serif;
        font-size: 1.6rem;
        direction: rtl;
        text-align: right;
        margin-bottom: 8px;
        color: #111111;
        font-weight: bold;
    }
    
    .indonesia-text {
        font-size: 1rem;
        text-align: left;
        color: #444444;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER APLIKASI ---
st.markdown("<div class='main-header'>تَكَلَّمْ AI (Takallam AI)</div>", unsafe_allow_html=True)
# PERBAIKAN 1: Mengubah unsafe_allow_header menjadi unsafe_allow_html agar tidak crash
st.markdown("<div class='sub-header'>Aplikasi Interaktif AI untuk Mengasah Maharah Kalam — Kelas X Madrasah Aliyah</div>", unsafe_allow_html=True)

# --- SIDEBAR: Autentikasi & Konfigurasi ---
st.sidebar.header("🔑 Akses & Konfigurasi")

with st.sidebar:
    username = st.text_input("Username", placeholder="Masukkan nama Anda...")
    api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="AIzaSy...")
    
    st.markdown("---")
    st.header("👤 Pilih Guru (Persona)")
    ustadz_pilihan = st.radio("Pilih Ustadz/Ustadzah:", ["Ustadz Faisal", "Ustadzah Ainun"])
    
    st.header("📚 Pilih Materi Kelas X")
    materi_pilihan = st.selectbox(
        "Pilih Topik Pembelajaran:",
        [
            "Al-Hayat al-Yaumiyah (الْحَيَاةُ الْيَوْمِيَّةُ — Kehidupan Sehari-hari)",
            "Al-Hiwayah (الْهِوَايَةُ — Hobi)",
            "At-Tashawwuq (التَّسَوُّقُ — Berbelanja)"
        ]
    )
    
    st.markdown("---")
    if st.button("🚪 Keluar / Reset Aplikasi", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- VALIDASI INPUT ---
if not username or not api_key:
    st.markdown("""
    <div class='setup-box'>
        <h4>👋 Ahlan wa Sahlan!</h4>
        <p>Silakan masukkan <b>Username</b> dan <b>Google Studio AI API Key</b> Anda di menu sebelah kiri untuk memulai percakapan interaktif menggunakan bahasa Arab.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- KONFIGURASI GOOGLE GEMINI ---
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Gagal mengonfigurasi API Key: {e}")
    st.stop()

# --- PROMPT SYSTEM ---
system_instruction = f"""
Anda adalah seorang guru bahasa Arab profesional untuk kelas X Madrasah Aliyah di Indonesia bernama {ustadz_pilihan}.
Fokus pembelajaran hari ini adalah Maharah Kalam (keterampilan berbicara) dengan materi: {materi_pilihan}.
Target audiens Anda adalah remaja usia sekolah Aliyah, gunakan gaya bahasa yang ramah, memotivasi, dan penuh apresiasi.

Aturan Wajib Output:
1. Setiap merespon, gunakan struktur berikut secara ketat:
   [ARAB] (Tulis kalimat bahasa Arab yang interaktif, jelas, berharakat lengkap, dan mengajak siswa merespon).
   [TERJEMAHAN] (Tulis terjemahan bahasa Indonesianya secara ramah).
2. Jangan gunakan format Markdown tebal/miring biasa untuk percakapan. Cukup gunakan penanda [ARAB] dan [TERJEMAHAN].
3. Ajukan satu pertanyaan pendek di setiap giliran agar siswa mudah merespon.
"""

# --- INISIALISASI SESI CHAT ---
if "chat_session" not in st.session_state:
    try:
        # PERBAIKAN 2: Menggunakan model terupdate 'gemini-2.5-flash' yang didukung penuh di backend
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", 
            system_instruction=system_instruction
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.messages = []
        
        panggilan_ustadz = "Ustadz Faisal" if ustadz_pilihan == "Ustadz Faisal" else "Ustadzah Ainun"
        
        if "Al-Hayat" in materi_pilihan:
            greeting_arab = "أَهْلًا وَسَهْلًا يَا طَالِبِي الْعَزِيزِ! أَنَا الْمُشْرِفُ عَنْ مَادَّةِ الْحَيَاةِ الْيَوْمِيَّةِ. مَاذَا تَفْعَلُ بَعْدَ الصَّلَاةِ الصُّبْحِ؟"
            greeting_indo = f"Ahlan wa sahlan, muridku tersayang! Saya {panggilan_ustadz}, pembimbingmu dalam materi Kehidupan Sehari-hari. Apa yang kamu lakukan setelah salat subuh?"
        elif "Al-Hiwayah" in materi_pilihan:
            greeting_arab = "مَرْحَبًا بِكَ! هَيَّا نَتَكَلَّمْ عَنِ الْهِوَايَةِ. أَنَا أُحِبُّ الْقِرَاءَةَ، وَأَنْتَ... مَا هِيَ هِوَايَتُكَ الْمُفَضَّلَةُ؟"
            greeting_indo = f"Selamat datang! Mari kita berbicara tentang Hobi. Saya suka membaca, kalau kamu... apa hobi favoritmu?"
        else:
            greeting_arab = "أَهْلًا بِكَ فِي دَرْسِ التَّسَوُّقِ! هَلْ تُحِبُّ أَنْ تَذْهَبَ إِلَى السُّوقِ التَّقْلِيدِيِّ أَمِ السُّوقِ الْحَدِيثِ؟"
            greeting_indo = f"Selamat datang di pelajaran Berbelanja! Apakah kamu lebih suka pergi ke pasar tradisional atau pasar modern?"

        st.session_state.messages.append({
            "role": "assistant",
            "arab": greeting_arab,
            "indo": greeting_indo
        })
    except Exception as e:
        st.error(f"Gagal memuat model AI. Detail: {e}")
        st.stop()

# --- TAMPILKAN RIWAYAT PERCAKAPAN ---
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='arabic-text'>{message['arab']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='indonesia-text'>{message['indo']}</div>", unsafe_allow_html=True)

# --- INPUT CHAT DARI SISWA ---
if user_input := st.chat_input("Tulis jawaban atau respon bahasa Arab Anda di sini..."):
    
    with st.chat_message("user"):
        st.write(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        with st.spinner(f"{ustadz_pilihan} sedang berpikir..."):
            response = st.session_state.chat_session.send_message(user_input)
            response_text = response.text
            
            arab_part = ""
            indo_part = ""
            
            if "[TERJEMAHAN]" in response_text:
                parts = response_text.split("[TERJEMAHAN]")
                arab_part = parts[0].replace("[ARAB]", "").strip()
                indo_part = parts[1].strip()
            else:
                arab_part = response_text
                indo_part = "Terjemahan otomatis sedang tidak tersedia."

        with st.chat_message("assistant"):
            st.markdown(f"<div class='arabic-text'>{arab_part}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='indonesia-text'>{indo_part}</div>", unsafe_allow_html=True)
            
        st.session_state.messages.append({
            "role": "assistant",
            "arab": arab_part,
            "indo": indo_part
        })
        
    except Exception as e:
        st.error(f"Terjadi kendala saat menghubungi ustadz/ustadzah: {e}")