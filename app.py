"""
Tarih Bilgi Rehberi Chatbot - Streamlit Arayüzü
"""
import sys
from pathlib import Path
import streamlit as st

# HTML bileşeni için (gerekli değil ancak iyi pratiktir, 
# st.components.v1.html() zaten çalışır)
import streamlit.components.v1 as components

# src modülünü import edebilmek için path ekle - KRİTİK!
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from rag_system import RAGSystem
except ImportError:
    st.error("HATA: 'rag_system' modülü bulunamadı. 'src' klasörünün path'e eklendiğinden emin olun.")
    st.stop()
except Exception as e:
    st.error(f"Modül yüklenirken beklenmedik bir hata oluştu: {e}")
    st.stop()


# ==================== SAYFA AYARLARI ====================
st.set_page_config(
    page_title="Tarih Bilgi Rehberi",
    page_icon="🇹🇷",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/KalyanKS-NLP/llm-engineer-toolkit',
        'Report a bug': "https://github.com/KalyanKS-NLP/llm-engineer-toolkit/issues",
        'About': """
        **Tarih Bilgi Rehberi Chatbot**
        
        Akbank GenAI Bootcamp Projesi
        Geliştirici: Murat İYİGÜN
        
        Bu chatbot, RAG mimarisi kullanarak Türk Tarihi hakkında 
        kaynaklara dayalı bilgiler sunar.
        """
    }
)

# ==================== FUTURİSTİK STIL AYARLARI ====================
st.markdown("""
<style>
    /* Ana Arka Plan - Koyu Futuristik Gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
    }
    
    /* Sidebar - Türk Bayrağı ve Futuristik Tasarım */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0f1419 100%);
        border-right: 2px solid #e30a17;
        box-shadow: 5px 0 25px rgba(227, 10, 23, 0.3);
    }
    
    /* Sidebar İçerik - Daha İyi Kontrast */
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    /* Sidebar Başlıklar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(227, 10, 23, 0.5);
    }
    
    /* Ana Başlık - Işıklı Efekt */
    h1 {
        color: #ffffff !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(227, 10, 23, 0.8),
                     0 0 40px rgba(227, 10, 23, 0.5);
        padding: 20px;
        border-bottom: 2px solid #e30a17;
        margin-bottom: 30px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(227, 10, 23, 0.8), 0 0 40px rgba(227, 10, 23, 0.5); }
        to { text-shadow: 0 0 30px rgba(227, 10, 23, 1), 0 0 60px rgba(227, 10, 23, 0.8); }
    }
    
    /* Chat Mesaj Kutuları - Neon Çerçeveler */
    .stChatMessage {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(227, 10, 23, 0.3);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(227, 10, 23, 0.2),
                    inset 0 0 15px rgba(227, 10, 23, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Kullanıcı Mesajı */
    [data-testid="stChatMessageContent"] {
        color: #e8e8e8 !important;
    }
    
    /* Input Kutusu - Futuristik */
    .stTextInput input {
        background: rgba(26, 31, 58, 0.8) !important;
        border: 2px solid #e30a17 !important;
        border-radius: 10px;
        color: #ffffff !important;
        padding: 12px;
        box-shadow: 0 0 20px rgba(227, 10, 23, 0.3),
                    inset 0 0 10px rgba(227, 10, 23, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #ff3344 !important;
        box-shadow: 0 0 30px rgba(227, 10, 23, 0.6),
                    inset 0 0 15px rgba(227, 10, 23, 0.2);
    }
    
    /* Input Placeholder */
    .stTextInput input::placeholder {
        color: #b8b8b8 !important;
        opacity: 0.7 !important;
    }
    
    /* Butonlar - Neon Efekt */
    .stButton button {
        background: linear-gradient(135deg, #e30a17 0%, #c41e3a 100%) !important;
        color: white !important;
        border: 2px solid #ff3344 !important;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(227, 10, 23, 0.5);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #ff3344 0%, #e30a17 100%) !important;
        box-shadow: 0 0 30px rgba(227, 10, 23, 0.8);
        transform: translateY(-2px);
    }
    
    /* Expander - Işıklı Çerçeve */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 58, 0.6) !important;
        border: 1px solid rgba(227, 10, 23, 0.4);
        border-radius: 10px;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(227, 10, 23, 0.2);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #e30a17 !important;
        box-shadow: 0 0 25px rgba(227, 10, 23, 0.4);
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 20, 25, 0.8) !important;
        border: 1px solid rgba(227, 10, 23, 0.2);
        border-radius: 0 0 10px 10px;
        padding: 15px;
    }
    
    /* Info Box - Özel Stil */
    .stAlert {
        background: rgba(26, 31, 58, 0.7) !important;
        border-left: 4px solid #e30a17 !important;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(227, 10, 23, 0.2);
        color: #e8e8e8 !important;
    }
    
    /* Container - Kaynak Kutuları */
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: rgba(26, 31, 58, 0.5) !important;
        border: 1px solid rgba(227, 10, 23, 0.3);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(227, 10, 23, 0.2);
    }
    
    /* Markdown İçeriği */
    .stMarkdown {
        color: #e8e8e8 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #e30a17 !important;
    }
    
    /* Spinner Text - Araştırılıyor yazısı */
    .stSpinner > div > div {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(227, 10, 23, 0.5);
    }
    
    /* st.spinner içindeki tüm metinler */
    [data-testid="stSpinner"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSpinner"] * {
        color: #ffffff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 20, 25, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #e30a17 0%, #c41e3a 100%);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(227, 10, 23, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff3344 0%, #e30a17 100%);
    }
    
    /* Form Submit Button Özel Stil */
    .stForm button[kind="primary"] {
        background: linear-gradient(135deg, #e30a17 0%, #c41e3a 100%) !important;
        border: 2px solid #ff3344 !important;
        box-shadow: 0 0 25px rgba(227, 10, 23, 0.6);
    }
    
    /* Divider */
    hr {
        border-color: rgba(227, 10, 23, 0.3) !important;
        box-shadow: 0 0 10px rgba(227, 10, 23, 0.2);
    }
</style>
""", unsafe_allow_html=True)


# ==================== SİSTEM YÜKLEME ====================

@st.cache_resource
def load_rag_system():
    """
    RAG sistemini yükler ve cache'ler.
    Hata durumunda None döner.
    """
    try:
        system = RAGSystem()
        return system
    except FileNotFoundError:
        st.error(
            "❌ Sistem yüklenemedi: FAISS index dosyaları (models/faiss_index) bulunamadı.\n"
            "Lütfen terminalde `python src/data_processing.py` komutunu çalıştırarak index dosyalarını oluşturun."
        )
        return None
    except Exception as e:
        st.error(f"❌ Sistem yüklenemedi: {type(e).__name__}: {e}")
        st.exception(e)
        return None

# RAG sistemini yükle
if 'rag_system' not in st.session_state:
    with st.spinner("📜 Tarih Bilgi Rehberi sistemi yükleniyor..."):
        st.session_state.rag_system = load_rag_system()

# Sohbet geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================== YARDIMCI FONKSİYONLAR ====================

def display_message(role, content, sources=None):
    """
    Sohbet mesajını ve kaynaklarını gösterir
    """
    with st.chat_message(role, avatar="📜" if role == "assistant" else "👤"):
        
        st.write(content)
        
        # Kaynakları göster (sadece asistan mesajları için)
        if sources and role == "assistant":
            kaynak_sayisi = len(sources)
            expander_title = f"📚 Kullanılan Kaynaklar ({kaynak_sayisi})"
            
            with st.expander(expander_title):
                for i, source in enumerate(sources, 1):
                    # Kaynak metnini formatla
                    source_text = source.get('content', 'İçerik bulunamadı.')
                    
                    # Metadata'yı al
                    donem = source.get('donem', 'Bilinmiyor')
                    yil = source.get('yil', '')
                    kaynak = source.get('kaynak', 'Bilinmiyor')
                    similarity = source.get('similarity', 0.0)
                    
                    # Başlık oluştur
                    title = f"**{i}. {donem}**"
                    if yil:
                        title += f" (Yıl: {yil})"
                    
                    st.markdown(title)
                    st.markdown(f"> _{kaynak}_ - (Benzerlik: {similarity:.2f})")
                    
                    st.container(border=True).markdown(f"_{source_text}_")


# ==================== ANA ARAYÜZ (MAIN) ====================

def main():
    
    # Sistem yüklenmediyse devam etme
    if not st.session_state.rag_system:
        st.error("Sistem başlatılamadı. Lütfen hata mesajlarını kontrol edin.")
        return

        # === SIDEBAR ===
    with st.sidebar:
        # TÜRK BAYRAĞI BAŞLIK
        # Sohbet sayısını hesapla (Her sohbet 1 kullanıcı + 1 asistan mesajından oluşur)
        sohbet_sayisi = len(st.session_state.messages) // 2
        try:
            # flag.jpg dosyasını yükle ve göster
            from PIL import Image
            flag_image = Image.open("flag.jpg")
            
            # Bayrak görselini ortala ve göster
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(flag_image, use_column_width=True)
            
            # Başlık ve sohbet sayısını göster
            st.markdown(f"""
            <div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'>
                <h1 style='color: #ffffff; font-size: 28px; margin: 0; text-shadow: 0 0 15px rgba(227, 10, 23, 0.8);'>
                    Tarih Bilgi Rehberi
                </h1>
                <p style='color: #e8e8e8; font-size: 14px; margin-top: 10px;'>
                    RAG Tabanlı Türk Tarihi Asistanı
                </p>
                <div style='margin-top: 15px; padding: 5px; background: rgba(227, 10, 23, 0.1); border-radius: 10px; border: 1px solid rgba(227, 10, 23, 0.3);'>
                    <p style='color: #ffffff; font-size: 16px; font-weight: bold; margin: 0; text-shadow: 0 0 8px rgba(255, 255, 255, 0.7);'>
                        {sohbet_sayisi} Sohbet Kaydı
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except FileNotFoundError:
            # Eğer flag.jpg bulunamazsa, emoji kullan
            st.markdown(f"""
            <div style='text-align: center; padding: 20px 0; margin-bottom: 20px;'>
                <div style='font-size: 80px; margin-bottom: 10px; line-height: 1; filter: drop-shadow(0 0 10px rgba(227, 10, 23, 0.8));'>
                    🇹🇷
                </div>
                <h1 style='color: #ffffff; font-size: 28px; margin: 0; text-shadow: 0 0 15px rgba(227, 10, 23, 0.8);'>
                    Tarih Bilgi Rehberi
                </h1>
                <p style='color: #e8e8e8; font-size: 14px; margin-top: 10px;'>
                    RAG Tabanlı Türk Tarihi Asistanı
                </p>
                <!-- YENİ EKLENEN BÖLÜM -->
                <div style='margin-top: 15px; padding: 5px; background: rgba(227, 10, 23, 0.1); border-radius: 10px; border: 1px solid rgba(227, 10, 23, 0.3);'>
                    <p style='color: #ffffff; font-size: 16px; font-weight: bold; margin: 0; text-shadow: 0 0 8px rgba(255, 255, 255, 0.7);'>
                        {sohbet_sayisi} Sohbet Kaydı
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.warning("⚠️ flag.jpg dosyası bulunamadı. Emoji kullanılıyor.")
        
        st.markdown("---")
        
        st.markdown("### 📖 Kullanım Kılavuzu")
        st.info(
            """
            1.  **Soru Sorun**: Sağdaki chat kutusuna Türk tarihi ile ilgili sorunuzu yazın.
            2.  **Yanıt Alın**: Yapay zeka, bilgi bankasındaki kayıtlara göre yanıt üretecektir.
            3.  **Kaynakları İnceleyin**: Yanıtın altındaki "Kullanılan Kaynaklar" bölümünden bilginin hangi dokümandan geldiğini kontrol edebilirsiniz.
            """
        )
        
        with st.expander("ℹ️ Proje Hakkında"):
            st.markdown(
                """
                **Geliştirici:** Murat İYİGÜN  
                **Bootcamp:** Akbank GenAI Bootcamp
                
                Bu proje, **RAG (Retrieval-Augmented Generation)** mimarisini kullanmaktadır. 
                
                Yanılarınız, doğrudan Gemini API'ye sorulmak yerine, önce Türk Tarihi veri setimizden 
                alakalı bilgiler bulunur (Retrieval) ve bu bilgiler ışığında Gemini tarafından 
                üretilir (Generation). Bu sayede cevaplar daha doğru ve kaynaklıdır.
                """
            )
        
        st.markdown("---")
        
        # Sidebar tıklama mantığı
        def handle_sidebar_click(question):
            st.session_state.run_query_from_sidebar = True
            st.session_state.current_question = question

        st.markdown("### 💡 Örnek Sorular (Veri Setinden)")
        
        with st.expander("📜 İslamiyet Öncesi"):
            questions_1 = [
                "Göktürk Kağanlığı'nın kuruluşu hakkında bilgi verir misin?",
                "Türk adının tarihsel kökenini açıklar mısın?",
                "Uygur Kağanlığı'nın yerleşik hayata geçişi nasıl oldu?"
            ]
            for q in questions_1:
                if st.button(q, key=f"q1_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun() 
        
        with st.expander("🕌 Türk-İslam Devletleri"):
            questions_2 = [
                "Karahanlı Devleti'nin İslamiyet'i kabulü nasıl oldu?",
                "Gazneli Mahmud'un Hindistan seferlerinin amaçları nelerdi?",
                "Gök Tanrı inancı ve İslamiyet arasındaki benzerlikler nelerdir?"
            ]
            for q in questions_2:
                if st.button(q, key=f"q2_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun()

        with st.expander("🏰 Anadolu Dönemi"):
            questions_3 = [
                "Malazgirt Savaşı hakkında bilgi verir misin?",
                "Kösedağ Savaşı'nın Anadolu'daki siyasi etkileri nelerdir?",
                "Moğol İstilası'nın Türkleşmeye etkisi nedir?"
            ]
            for q in questions_3:
                if st.button(q, key=f"q3_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun()
        
        with st.expander("🏰 Osmanlı Dönemi"):
            questions_4 = [
                "İstanbul'un Fethi'nin dünya tarihi açısından sonuçları nelerdir?",
                "Kanuni Sultan Süleyman dönemi neden 'Muhteşem Yüzyıl' olarak adlandırılır?",
                "Tanzimat Fermanı'nın amacı neydi?"
            ]
            for q in questions_4:
                if st.button(q, key=f"q4_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun()

        with st.expander("🇹🇷 Millî Mücadele"):
            questions_5 = [
                "Amasya Genelgesi'nin Millî Mücadele'deki yeri nedir?",
                "Erzurum Kongresi'nde alınan temel kararlar nelerdir?",
                "Sakarya Meydan Muharebesi'nin sonuçları nelerdir?"
            ]
            for q in questions_5:
                if st.button(q, key=f"q5_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun()

        with st.expander("🛡️ Cumhuriyet Dönemi"):
            questions_6 = [
                "Cumhuriyet'in ilanı ne zaman ve nasıl gerçekleşti?",
                "Halifeliğin kaldırılması süreci hakkında bilgi verir misin?",
                "Çok partili hayata geçiş denemeleri nelerdir?"
            ]
            for q in questions_6:
                if st.button(q, key=f"q6_{q[:20]}", use_container_width=True):
                    handle_sidebar_click(q)
                    # st.rerun()


    # === ANA CHAT BÖLÜMÜ ===
    st.title("Tarih Bilgi Rehberi Chatbot")

    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        display_message(message["role"], message["content"], message.get("sources"))
    

    # Chat input ve sorgulama mantığı
    st.markdown("---")
    
    # Chat input kutusu
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_question_from_box = st.text_input(
                "Sorunuzu yazın:",
                placeholder="Örn: İstanbul'un Fethi'nin dünya tarihi açısından sonuçları nelerdir?",
                label_visibility="collapsed",
                value="" 
            )
        with col2:
            submit_button = st.form_submit_button("🔤 Gönder", use_container_width=True)

    
    # SORGULAMA KONTROL BLOĞU
    
    query_to_run = None
    
    # 1. Formdan (manuel) mi geldi?
    if submit_button and user_question_from_box:
        query_to_run = user_question_from_box
    
    # 2. Sidebar'dan mı geldi?
    elif st.session_state.get('run_query_from_sidebar', False):
        query_to_run = st.session_state.get('current_question', '')
        # İşaretleri temizle
        st.session_state.run_query_from_sidebar = False
        if 'current_question' in st.session_state:
            del st.session_state.current_question

    # Soruyu işle
    if query_to_run:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({
            "role": "user",
            "content": query_to_run
        })
        
        # Yanıt üret
        with st.spinner("🤔 Tarihsel kayıtlar araştırılıyor..."):
            try:
                result = st.session_state.rag_system.query(query_to_run)
                
                # Bot yanıtını ekle
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["response"],
                    "sources": result["sources"]
                })

                # Bir sonraki render'da en alta scroll yapılması için bayrağı ayarla
                st.session_state.scroll_to_bottom = True
                
                # Ekranı yeniden çiz
                st.rerun()

            except Exception as e:
                st.error(f"Sorgu işlenirken bir hata oluştu: {str(e)}")
                
    # Eğer bir önceki adımda yeni mesaj eklendiyse (bayrak True ise),
    # sayfanın en altına kaydırmak için JS enjekte et.
    if st.session_state.get('scroll_to_bottom', False):
        components.html(
            """
            <script>
                // DOM'un güncellenmesi ve yeni mesajın eklenmesi için 
                // 300ms'lik bir gecikme ekliyoruz.
                window.setTimeout(function() {
                    // Tüm sohbet mesajı elementlerini bul
                    const messages = window.parent.document.querySelectorAll('.stChatMessage');
                    
                    if (messages.length > 0) {
                        // Son mesaj elementini bul
                        const lastMessage = messages[messages.length - 1];
                        
                        // Son mesajı görüntü alanına kaydır (en alta hizalayarak)
                        lastMessage.scrollIntoView({ behavior: 'smooth', block: 'end' });
                    }
                }, 300);
            </script>
            """,
            height=0,  # HTML bileşeninin yer kaplamaması için
        )
        # Bayrağı tekrar False yap (gereksiz kaydırmaları önle)
        st.session_state.scroll_to_bottom = False

# Uygulamayı çalıştır
if __name__ == "__main__":
    main()