"""
Setup Script - Tarih Bilgi Rehberi Projesini Otomatik Kurar
Ana dizinde çalıştırılmalıdır: python setup.py
"""

import os
import sys
from pathlib import Path
import subprocess


def print_header(text):
    """Başlık yazdır"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Python versiyonunu kontrol et"""
    print("🔍 Python versiyonu kontrol ediliyor...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 veya üzeri gerekli!")
        print(f"   Mevcut versiyon: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Uygun")


def create_directories():
    """Gerekli dizinleri oluştur"""
    print("\n📁 Dizinler oluşturuluyor...")
    
    directories = [
        "data/raw",
        "data/processed",
        "models/embeddings",
        "models/faiss_index",
        "src"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}")
    
    print("✅ Tüm dizinler oluşturuldu")


def create_env_file():
    """Environment dosyası oluştur"""
    print("\n🔐 Environment dosyası kontrol ediliyor...")
    
    if Path(".env").exists():
        print("⚠️  .env dosyası zaten mevcut")
        response = input("   Üzerine yazmak istiyor musunuz? (e/h): ")
        if response.lower() != 'e':
            print("   .env dosyası değiştirilmedi")
            return
    
    env_content = """# Google Gemini API Key
# https://ai.google.dev/ adresinden ücretsiz API key alabilirsiniz
GOOGLE_API_KEY=your_gemini_api_key_here

# Opsiyonel Ayarlar
CHUNK_SIZE=512
CHUNK_OVERLAP=50
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.3
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ .env dosyası oluşturuldu")
    print("⚠️  UYARI: .env dosyasını düzenleyip GOOGLE_API_KEY'inizi ekleyin!")


def install_requirements():
    """Requirements'i yükle"""
    print("\n📦 Python paketleri yükleniyor...")
    print("   Bu işlem birkaç dakika sürebilir...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("\n✅ Tüm paketler başarıyla yüklendi")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Paket yükleme hatası: {e}")
        sys.exit(1)


def check_json_files():
    """JSON veri dosyalarını kontrol et"""
    print("\n📚 JSON veri dosyaları kontrol ediliyor...")
    
    data_dir = Path("data/raw")
    json_files = list(data_dir.glob("*.json"))
    
    if not json_files:
        print("⚠️  data/raw/ klasöründe JSON dosyası bulunamadı!")
        print("\n   Beklenen dosyalar:")
        print("   • islamiyet_oncesi.json")
        print("   • ilk_turk_islam_devletleri.json")
        print("   • anadolu_beylikleri.json")
        print("   • osmanli_devleti.json")
        print("   • milli_mucadele.json")
        print("   • cumhuriyet.json")
        print("\n   Lütfen JSON veri dosyalarınızı data/raw/ klasörüne koyun.")
        return False
    
    print(f"✅ {len(json_files)} JSON dosyası bulundu:")
    for json_file in json_files:
        print(f"   ✓ {json_file.name}")
    
    return True


def process_data():
    """Verileri işle ve FAISS index oluştur"""
    print("\n🔧 Veri işleme ve FAISS index oluşturuluyor...")
    
    # Önce JSON dosyalarını kontrol et
    if not check_json_files():
        print("\n⚠️  JSON dosyaları bulunamadığı için veri işleme atlanıyor.")
        print("   JSON dosyalarınızı ekledikten sonra şu komutu çalıştırın:")
        print("   python src/data_processing.py")
        return
    
    print("   Bu işlem 5-10 dakika sürebilir...\n")
    
    response = input("   Devam edilsin mi? (e/h): ")
    if response.lower() != 'e':
        print("   Veri işleme atlandı")
        print("   Daha sonra şu komutu çalıştırabilirsiniz:")
        print("   python src/data_processing.py")
        return
    
    try:
        subprocess.check_call([sys.executable, "src/data_processing.py"])
        print("\n✅ Veri işleme tamamlandı")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Veri işleme hatası: {e}")


def check_api_key():
    """API key'i kontrol et"""
    print("\n🔑 API Key kontrol ediliyor...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key or api_key == "your_gemini_api_key_here":
            print("⚠️  GOOGLE_API_KEY bulunamadı veya geçersiz!")
            print("\n   Lütfen şu adımları izleyin:")
            print("   1. https://ai.google.dev/ adresine gidin")
            print("   2. 'Get API Key' butonuna tıklayın")
            print("   3. Yeni bir API key oluşturun")
            print("   4. .env dosyasını açın ve GOOGLE_API_KEY'e yapıştırın")
            print("   5. Bu scripti tekrar çalıştırın\n")
            return False
        
        print("✅ API Key bulundu")
        return True
    except ImportError:
        print("⚠️  python-dotenv modülü yüklenmemiş, API key kontrolü atlanıyor")
        return True


def run_tests():
    """Basit testleri çalıştır"""
    print("\n🧪 Testler çalıştırılıyor...")
    
    try:
        # Import testleri
        print("   📦 Modül import testleri...")
        import sentence_transformers
        import faiss
        import streamlit
        import google.generativeai
        print("   ✅ Tüm modüller başarıyla import edildi")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import hatası: {e}")
        return False


def show_next_steps():
    """Sonraki adımları göster"""
    print_header("KURULUM TAMAMLANDI!")
    
    print("✅ Tüm bileşenler başarıyla kuruldu!\n")
    
    print("📋 SONRAKİ ADIMLAR:\n")
    
    print("1️⃣  JSON Veri Dosyalarını Ekleyin:")
    print("   • data/raw/ klasörüne JSON dosyalarınızı kopyalayın")
    print("   • islamiyet_oncesi.json")
    print("   • ilk_turk_islam_devletleri.json")
    print("   • anadolu_beylikleri.json")
    print("   • osmanli_devleti.json")
    print("   • milli_mucadele.json")
    print("   • cumhuriyet.json\n")
    
    print("2️⃣  API Key'inizi Ayarlayın:")
    print("   • .env dosyasını açın")
    print("   • GOOGLE_API_KEY değerini güncelleyin")
    print("   • https://ai.google.dev/ adresinden ücretsiz key alın\n")
    
    print("3️⃣  Veri İşleme Yapın (JSON dosyaları ekledikten sonra):")
    print("   python src/data_processing.py\n")
    
    print("4️⃣  Uygulamayı Başlatın:")
    print("   streamlit run app.py\n")
    
    print("5️⃣  Tarayıcınızda Açın:")
    print("   http://localhost:8501\n")
    
    print("📚 DOKÜMANTASYON:")
    print("   • README.md - Genel bilgiler")
    print("   • SETUP.md - Detaylı kurulum")
    print("   • ARCHITECTURE.md - Teknik detaylar")
    print("   • USER_GUIDE.md - Kullanım kılavuzu\n")
    
    print("🆘 YARDIM:")
    print("   • Sorun yaşarsanız SETUP.md'deki 'Sorun Giderme' bölümüne bakın")
    print("   • GitHub Issues: <repository-url>/issues\n")
    
    print("🚀 İyi çalışmalar!")
    print("="*60 + "\n")


def main():
    """Ana kurulum fonksiyonu"""
    print_header("TARİH BİLGİ REHBERİ CHATBOT - OTOMATIK KURULUM")
    
    print("Bu script Tarih Bilgi Rehberi projesini otomatik olarak kuracaktır.\n")
    print("Kurulum adımları:")
    print("  1. Python versiyonu kontrolü")
    print("  2. Dizin yapısı oluşturma")
    print("  3. Environment dosyası oluşturma")
    print("  4. Python paketlerini yükleme")
    print("  5. JSON veri dosyalarını kontrol etme")
    print("  6. Veri işleme ve index oluşturma (opsiyonel)")
    print("  7. Test çalıştırma\n")
    
    response = input("Devam etmek istiyor musunuz? (e/h): ")
    if response.lower() != 'e':
        print("Kurulum iptal edildi.")
        sys.exit(0)
    
    # Kurulum adımları
    check_python_version()
    create_directories()
    create_env_file()
    install_requirements()
    
    # Opsiyonel adımlar
    process_data()
    
    # Testler
    if not run_tests():
        print("\n⚠️  Bazı testler başarısız oldu. Lütfen hataları kontrol edin.")
    
    # API key kontrolü
    api_key_valid = check_api_key()
    
    # Sonuç
    show_next_steps()
    
    if not api_key_valid:
        print("⚠️  API key ayarlanmadan uygulama çalıştırılamaz.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Kurulum kullanıcı tarafından iptal edildi.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)