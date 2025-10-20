# 🔧 Kurulum Kılavuzu

Bu dokümanda Tarih Bilgi Rehberi Chatbot projesini yerel ortamınızda çalıştırmak için gereken tüm adımlar detaylı olarak açıklanmıştır.

## 📋 Ön Gereksinimler

- Python 3.9 veya üzeri
- pip (Python paket yöneticisi)
- Git
- Google Gemini API Key ([buradan](https://ai.google.dev/) alabilirsiniz)
- En az 4GB RAM
- 2GB boş disk alanı

## 🚀 Kurulum Adımları

### 1. Repoyu Klonlama

```bash
git clone https://github.com/yourusername/tarih-bilgi-rehberi-chatbot.git
cd tarih-bilgi-rehberi-chatbot
```

### 2. Virtual Environment Oluşturma

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Virtual environment aktif olduğunda terminal başında `(venv)` görünmelidir.

### 3. Gerekli Kütüphaneleri Yükleme

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt içeriği:**
```
langchain==0.1.0
langchain-google-genai==0.0.5
streamlit==1.29.0
google-generativeai==0.3.1
sentence-transformers==2.2.2
faiss-cpu==1.7.4
python-dotenv==1.0.0
numpy==1.24.3
pandas==2.0.3
```

### 4. API Key Yapılandırması

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyerek API key'inizi ekleyin:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Gemini API Key Alma:**
1. [Google AI Studio](https://ai.google.dev/) adresine gidin
2. "Get API Key" butonuna tıklayın
3. Yeni bir API key oluşturun
4. API key'i kopyalayıp `.env` dosyasına yapıştırın

⚠️ **ÖNEMLİ**: `.env` dosyası hassas bilgiler içerir, asla Git'e commit etmeyin!

### 5. Veri Setini Hazırlama

#### JSON Veri Dosyalarını Yerleştirme

Tarih veri setinizi `data/raw/` klasörüne kopyalayın:

```bash
data/raw/
├── islamiyet_oncesi.json
├── ilk_turk_islam_devletleri.json
├── anadolu_beylikleri.json
├── osmanli_devleti.json
├── milli_mucadele.json
└── cumhuriyet.json
```

**Desteklenen format:** `.json`

**JSON Veri Yapısı:**
```json
[
  {
    "id": "osmanli_001",
    "donem": "Osmanlı Devleti",
    "alt_donem": "Yükselme Dönemi",
    "kategori": {
      "ana": "Siyasi Olaylar",
      "alt": "Fetihler"
    },
    "konu": "İstanbul'un Fethi",
    "icerik": "İstanbul, 29 Mayıs 1453 tarihinde II. Mehmed tarafından fethedilmiştir...",
    "yil": 1453,
    "anahtar_kelimeler": ["İstanbul", "Fatih Sultan Mehmed", "Fetih"],
    "etiketler": ["fetih", "askeri strateji"],
    "kaynak": "Türk Tarih Kurumu",
    "kaynak_turu": "Kitap",
    "referans_link": "https://www.ttk.gov.tr/istanbulun-fethi"
  }
]
```

### 6. Veri İşleme ve Index Oluşturma

```bash
python src/data_processing.py
```

Bu adım:
- JSON dosyalarını okur ve parse eder
- Tarihsel metadata'yı işler (dönem, yıl, kategori)
- Chunk'lara böler
- Embedding'leri oluşturur
- FAISS index'i kaydeder

⏱️ **Beklenen Süre**: ~5-10 dakika (200 tarihsel kayıt için)

İşlem tamamlandığında şu mesajı görmelisiniz:
```
✅ FAISS index başarıyla oluşturuldu: models/faiss_index/
✅ Toplam 200 tarihsel kayıt işlendi
📚 Dönem Bazlı Dağılım:
   • İslamiyet Öncesi Türk Tarihi: 42 chunk
   • Osmanlı Devleti: 78 chunk
   ...
```

### 7. Web Uygulamasını Başlatma

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde çalışacaktır.

Tarayıcınız otomatik olarak açılmazsa, yukarıdaki URL'yi manuel olarak ziyaret edin.

## 🧪 Test Etme

### Basit Test
```bash
python src/rag_system.py
```

Bu script örnek sorularla sistemi test eder ve sonuçları gösterir.

### Manuel Test Soruları
Chatbot'u test etmek için şu soruları deneyebilirsiniz:
- "Malazgirt Savaşı ne zaman oldu?"
- "Osmanlı Devleti'nin yükselme dönemi hangi padişahlar vardı?"
- "Türklerin İslamiyet'i kabulü nasıl oldu?"
- "Mustafa Kemal Samsun'a ne zaman çıktı?"
- "Atatürk inkılapları nelerdir?"

## 🐛 Sorun Giderme

### Hata: "No module named 'faiss'"
**Çözüm:**
```bash
pip uninstall faiss-cpu
pip install faiss-cpu==1.7.4
```

### Hata: "GOOGLE_API_KEY not found"
**Çözüm:**
- `.env` dosyasının proje ana dizininde olduğundan emin olun
- API key'in doğru girildiğini kontrol edin
- Uygulamayı yeniden başlatın

### Hata: "FAISS index not found"
**Çözüm:**
```bash
python src/data_processing.py
```
Data processing script'ini çalıştırarak index'i yeniden oluşturun.

### Hata: "No JSON files found in data/raw/"
**Çözüm:**
- JSON veri dosyalarınızın `data/raw/` klasöründe olduğundan emin olun
- Dosya isimlerini kontrol edin (islamiyet_oncesi.json, osmanli_devleti.json vb.)
- JSON formatının doğru olduğunu kontrol edin

### Streamlit "Port already in use" hatası
**Çözüm:**
```bash
streamlit run app.py --server.port 8502
```
Farklı bir port kullanın.

### Memory Error
**Çözüm:**
- Chunk size'ı küçültün (data_processing.py içinde)
- Daha az JSON dosyası ile test edin
- RAM'i artırın

### Import Error: "No module named 'src'"
**Çözüm:**
app.py dosyasında path ekleme kodunun olduğundan emin olun:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))
```

## 📦 Deployment

### Streamlit Cloud'a Deploy

1. GitHub'a push edin:
```bash
git add .
git commit -m "Initial commit: Tarih Bilgi Rehberi Chatbot"
git push origin main
```

2. [Streamlit Cloud](https://streamlit.io/cloud)'a gidin
3. "New app" butonuna tıklayın
4. GitHub reponuzu seçin
5. Secrets kısmına API key'inizi ekleyin:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```
6. "Deploy" butonuna tıklayın

### Hugging Face Spaces'e Deploy

1. [Hugging Face](https://huggingface.co/spaces) hesabı oluşturun
2. Yeni Space oluşturun (Streamlit SDK seçin)
3. Dosyaları upload edin
4. Settings > Repository secrets'a API key ekleyin
5. Space otomatik olarak deploy olacaktır

## 🔄 Güncelleme

Projeyi güncellemek için:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python src/data_processing.py  # Gerekirse index'i yenileyin
```

## 📚 Veri Seti Güncelleme

Yeni tarihsel veriler eklemek için:

1. Yeni JSON dosyasını `data/raw/` klasörüne ekleyin
2. JSON formatının doğru olduğundan emin olun
3. Veri işleme script'ini yeniden çalıştırın:
```bash
python src/data_processing.py
```

## 📞 Destek

Sorun yaşıyorsanız:
1. Bu dokümantasyonu tekrar okuyun
2. GitHub Issues'da arama yapın
3. Yeni bir issue açın

### Veri Kaynakları
- **TDK**: [tdk.gov.tr](https://www.tdk.gov.tr)
- **TTK**: [ttk.gov.tr](https://www.ttk.gov.tr)
- **Wikisource**: [tr.wikisource.org](https://tr.wikisource.org)

---

**Kurulum ile ilgili sorularınız için**: GitHub Issues bölümünü kullanın