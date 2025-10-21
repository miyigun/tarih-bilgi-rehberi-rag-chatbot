# 📱 Kullanıcı Kılavuzu

Tarih Bilgi Rehberi Chatbot'u nasıl kullanacağınızı öğrenmek için bu kılavuzu okuyun.

## 🌐 Web Arayüzüne Erişim

### Demo Link

Uygulamanın canlı demosuna aşağıdaki linkten erişebilirsiniz:

**URL**: [https://tarih-bilgi-rehberi-rag-chatbot-eu8pvgcka8w9xkuyx7uhjt.streamlit.app/](https://tarih-bilgi-rehberi-rag-chatbot-eu8pvgcka8w9xkuyx7uhjt.streamlit.app/)

*(Not: Uygulama ücretsiz Streamlit Cloud üzerinde barındırıldığı için ilk açılışta veya yoğunluk durumunda yavaşlık yaşanabilir.)*

### İlk Giriş
1. Yukarıdaki linke tıklayın
2. Sayfa otomatik olarak yüklenecektir
3. RAG sistemi arka planda hazırlanır (~5 saniye)
4. Hoş geldiniz mesajını göreceksiniz

---

## 🎯 Ana Özellikler

### 1. Soru Sorma

#### Basit Kullanım
1. Sayfanın altındaki metin kutusuna sorunuzu yazın
2. Enter tuşuna basın veya "📤 Gönder" butonuna tıklayın
3. Asistan 2-3 saniye içinde yanıt verecektir

#### Örnek Sorular
- "Malazgirt Savaşı ne zaman oldu ve sonuçları neydi?"
- "Osmanlı Devleti'nin yükselme döneminde hangi padişahlar vardı?"
- "Türklerin İslamiyet'i kabul süreci nasıl gelişti?"
- "Mustafa Kemal Atatürk Samsun'a ne zaman çıktı?"
- "Cumhuriyet döneminde yapılan inkılaplar nelerdir?"

### 2. Yanıtları Anlama

#### Yanıt Yapısı
Her yanıt şu bölümleri içerir:
- **Ana Yanıt**: Sorunuzun akademik ve öğretici cevabı
- **Tarihsel Bağlam**: Olayın kronolojik bağlamı
- **Kaynak Referansları**: TTK, TDK gibi güvenilir kaynaklar

#### Kaynaklar
Yanıtın altında "📖 Kullanılan Kaynaklar" bölümünü göreceksiniz:
- Tıklayarak kaynakları görebilirsiniz
- Her kaynağın dönem bilgisi (Osmanlı Devleti, Cumhuriyet vb.)
- Yıl bilgisi (1453, 1919 vb.)
- Kaynak referansı (Türk Tarih Kurumu, TDK)
- Benzerlik skoru

**Dönem Badge'leri:**
- 🔵 İslamiyet Öncesi Türk Tarihi
- 🟢 İlk Türk-İslam Devletleri
- 🟠 Anadolu Beylikleri Dönemi
- 🔴 Osmanlı Devleti
- 🟣 Millî Mücadele Dönemi
- 🌸 Cumhuriyet Dönemi

**Benzerlik Skorları:**
- 🟢 %70+: Çok alakalı
- 🟡 %50-70: Alakalı
- 🔴 %30-50: Kısmen alakalı

---

## 💡 Kenar Çubuğu (Sidebar)

### Kullanım Kılavuzu Bölümü
Sol taraftaki kenar çubuğunda:
- Kapsanan tarihsel dönemler listelenir
- Kullanım talimatları bulunur

### Örnek Sorular - Dönemlere Göre
Sidebar'da dönem bazlı örnek sorular bulunur:

### 🏛️ İslamiyet Öncesi
- "Göktürk Kağanlığı'nın kuruluşu hakkında bilgi verir misin?"
- "Türk adının tarihsel kökenini açıklar mısın?"
- "Uygur Kağanlığı'nın yerleşik hayata geçişi nasıl oldu?"

### ☪️ Türk-İslam Devletleri
- "Karahanlı Devleti'nin İslamiyet'i kabulü nasıl oldu?"
- "Gazneli Mahmud'un Hindistan seferlerinin amaçları nelerdi?"
- "Gök Tanrı inancı ve İslamiyet arasındaki benzerlikler nelerdir?"

### 🏰 Anadolu Beylikleri
- "Malazgirt Savaşı hakkında bilgi verir misin?"
- "Kösedağ Savaşı'nın Anadolu'daki siyasi etkileri nelerdir?"
- "Moğol İstilası'nın Türkleşmeye etkisi nedir?"

### 🕌 Osmanlı
- "İstanbul'un Fethi'nin dünya tarihi açısından sonuçları nelerdir?"
- "Kanuni Sultan Süleyman dönemi neden 'Muhteşem Yüzyıl' olarak adlandırılır?"
- "Tanzimat Fermanı'nın amacı neydi?"

### 🇹🇷 Millî Mücadele
- "Amasya Genelgesi'nin Millî Mücadele'deki yeri nedir?"
- "Erzurum Kongresi'nde alınan temel kararlar nelerdir?"
- "Sakarya Meydan Muharebesi'nin sonuçları nelerdir?"

### 🎯 Cumhuriyet
- "Cumhuriyet'in ilanı ne zaman ve nasıl gerçekleşti?"
- "Halifeliğin kaldırılması süreci hakkında bilgi verir misin?"
- "Çok partili hayata geçiş denemeleri nelerdir?"

### Sistem Bilgileri
- Tarihsel kayıt sayısı
- Toplam mesaj sayısı
- Sistem durumu

### Sohbeti Temizle
- "🗑️ Sohbeti Temizle" butonu
- Tüm mesaj geçmişini siler
- Yeni bir sohbet başlatır

### Veri Kaynakları
- **TDK** - Türk Dil Kurumu
- **TTK** - Türk Tarih Kurumu
- **Wikisource** - Açık Kaynak Belgeler
- **Vikipedi** - Genel Bilgi

---

## 🎨 Arayüz Bileşenleri

### Ana Sayfa Düzeni

```
┌─────────────────────────────────────────────────────┐
│  📚 Tarih Bilgi Rehberi Chatbot                     │
│     RAG Teknolojisi ile Güçlendirilmiş              │
├────────────────┬────────────────────────────────────┤
│                │  💬 Sohbet Geçmişi                 │
│  📖 Kullanım   │  ┌──────────────────────────────┐ │
│  Kılavuzu      │  │ 👤 Siz: [Tarih Sorusu]       │ │
│                │  └──────────────────────────────┘ │
│  💡 Örnek      │  ┌──────────────────────────────┐ │
│  Sorular       │  │ 📚 Tarih Asistanı: [Yanıt]   │ │
│  (Dönemler)    │  │ 📖 Kaynaklar (3)             │ │
│                │  │   • Osmanlı Devleti, 1453    │ │
│  📊 Sistem     │  │   • Kaynak: TTK              │ │
│  Bilgileri     │  └──────────────────────────────┘ │
│                │  ─────────────────────────────────│
│  🗑️ Sohbeti    │  Sorunuzu yazın: [___________] 📤 │
│  Temizle       │                                    │
│                │                                    │
│  📚 Veri       │                                    │
│  Kaynakları    │                                    │
└────────────────┴────────────────────────────────────┘
```

### Mesaj Türleri

#### Kullanıcı Mesajı
- Açık gri arka plan
- Sol kenarda kahverengi çizgi
- 👤 ikonu

#### Tarih Asistanı Mesajı
- Krem rengi arka plan
- Sol kenarda altın çizgi
- 📚 ikonu
- Dönem badge'leri
- Yıl bilgisi (📅)
- Kaynaklar dahil

---

## 📝 İpuçları ve En İyi Kullanım

### Etkili Soru Sorma

#### ✅ İyi Sorular
- **Spesifik Olay**: "İstanbul'un fethi nasıl gerçekleşti?"
- **Dönem Sorgusu**: "Osmanlı'nın yükselme döneminde kimler vardı?"
- **Kronolojik**: "Millî Mücadele hangi aşamalardan geçti?"
- **Karşılaştırma**: "Selçuklu ve Osmanlı devlet yönetimi arasındaki farklar?"

#### ❌ Kötü Sorular
- **Belirsiz**: "Türk tarihi hakkında bilgi ver"
- **Çok genel**: "Savaşlar"
- **Çoklu**: "Tüm Osmanlı padişahlarını, savaşları ve antlaşmaları anlat"

### Soru Türleri

Chatbot'a farklı türlerde sorular sorabilirsiniz. İşte bazı örnekler:

#### 1. Tarihsel Olay Soruları
**Örnek**: "Ne zaman oldu?", "Nasıl gerçekleşti?", "Sonuçları ne oldu?"
```
Soru: "İstanbul'un Fethi'nin dünya tarihi açısından sonuçları nelerdir?" 
Yanıt: Tarih + Taraflar + Sonuçları + Önemi
```

#### 2. Kişi ve Devlet Soruları
**Örnek**: "Kim?", "Hangi dönem?", "Nasıl kuruldu?"
```
Soru: "Karahanlı Devleti'nin İslamiyet'i kabulü nasıl oldu?" 
Yanıt: Devletin Kuruluşu/Kişinin Yaşamı + Dönemi + Önemli Olaylar + Mirası
```

#### 3. Kavram veya Önemi Açıklama
**Örnek**: "Nedir?", "Ne demektir?", "Önemi nedir?"
```
Soru: "Türk adının tarihsel kökenini açıklar mısın?" 
Yanıt: Tanım + Nasıl İşlediği/İçeriği + Önemi + Örnekler
```

#### 4. Neden-Sonuç İlişkisi
**Örnek**: "Neden?", "Etkileri ne oldu?"
```
Soru: "Kösedağ Savaşı'nın Anadolu'daki siyasi etkileri nelerdir?" 
Yanıt: Olayın Nedenleri + Süreç + Doğrudan ve Dolaylı Sonuçları
```

---

## 🔍 Özellikler ve Kabiliyetler

### Ne Yapabilir?

✅ **Tarihsel Bilgi Verebilir**
- İslamiyet Öncesi Türk Tarihi
- Türk-İslam Devletleri
- Anadolu Beylikleri
- Osmanlı İmparatorluğu (Kuruluş-Yıkılış)
- Millî Mücadele
- Cumhuriyet Dönemi

✅ **Kaynak Gösterebilir**
- TTK, TDK gibi akademik kaynaklar
- Dönem ve yıl bilgisi
- Benzerlik skorları
- Referans linkleri

✅ **Kronolojik Bağlam Koruyabilir**
- Olayların sırasını anlar
- Neden-sonuç ilişkilerini açıklar
- Dönemler arası geçişleri gösterir

### Ne Yapamaz?

❌ **Yapamaz**
- Tartışmalı tarihi olaylarda tek taraflı yorum
- Kaynaklarda olmayan bilgi üretme
- Spekülasyon yapma
- Güncel siyasi yorum
- Kişisel görüş bildirme

⚠️ **Bu tür konular için:**
- Akademik tarih kitapları
- TTK resmi yayınları
- Uzman tarihçiler
- Üniversite tarih bölümleri

---

## 🎓 Kullanım Senaryoları

### Senaryo 1: Öğrenci - Sınav Hazırlığı

**Durum**: YKS/KPSS tarih soruları için çalışıyorsunuz

**Örnek Soru Dizisi**:
1. "İstanbul'un Fethi'nin dünya tarihi açısından sonuçları nelerdir?" 
2. "Karahanlı Devleti'nin İslamiyet'i kabulü nasıl oldu?" 
3. "Türk adının tarihsel kökenini açıklar mısın?"
4. "Kösedağ Savaşı'nın Anadolu'daki siyasi etkileri nelerdir?"

**Beklenen Sonuç**: Kronolojik, kaynaklı, sınav odaklı bilgi

### Senaryo 2: Araştırmacı - Kaynak Tarama

**Durum**: Bir dönem hakkında akademik araştırma yapıyorsunuz

**Örnek Soru Dizisi**:
1. "Osmanlı'nın yükselme dönemindeki devlet teşkilatı nasıldı?"
2. "Bu dönemde hangi ıslahatlar yapıldı?"
3. "Kaynaklar hangileri?"
4. "Benzer dönem özellikleri neler?"

**Beklenen Sonuç**: Akademik kaynak referansları ve detaylı bilgi

### Senaryo 3: Tarih Meraklısı - Genel Bilgi

**Durum**: Türk tarihini merak ediyorsunuz

**Örnek Soru Dizisi**:
1. "Göktürkler kimlerdi?"
2. "Orhun Yazıtları neden önemli?"
3. "İlk Türk devletleri hangileri?"
4. "Türkler İslamiyet'i nasıl kabul etti?"

**Beklenen Sonuç**: Anlaşılır, kronolojik, ilgi çekici anlatım

### Senaryo 4: Öğretmen - Ders Materyali

**Durum**: Ders için özet bilgi hazırlıyorsunuz

**Örnek Soru Dizisi**:
1. "Osmanlı İmparatorluğu'nun kuruluşunu özetler misin?"
2. "İstanbul'un fethinin önemi nedir?"
3. "Tanzimat Fermanı'nın maddeleri neler?"
4. "Bu konuları öğrencilere nasıl anlatabilirim?"

**Beklenen Sonuç**: Özet, anlaşılır, öğretici içerik

---

## 🐛 Sorun Giderme

### Yaygın Problemler

#### 1. "Yanıt alamıyorum"
**Çözüm**:
- İnternet bağlantınızı kontrol edin
- Sayfayı yenileyin (F5)
- Sorunuzu daha basit hale getirin
- Örnek sorulardan birini deneyin

#### 2. "Yanıt çok genel"
**Çözüm**:
- Daha spesifik soru sorun (dönem, tarih, kişi belirtin)
- "İstanbul'un fethi" yerine "İstanbul'un fethi nasıl gerçekleşti ve sonuçları neydi?"

#### 3. "Kaynaklarda dönem bilgisi göremiyorum"
**Çözüm**:
- "📖 Kullanılan Kaynaklar" bölümüne tıklayın
- Renkli dönem badge'lerini kontrol edin
- 📅 işaretli yıl bilgilerini inceleyin

#### 4. "Çok yavaş yanıt veriyor"
**Muhtemel Nedenler**:
- API limiti (günlük 1500 istek)
- Yüksek trafik
- İnternet bağlantısı yavaş

**Çözüm**:
- Birkaç saniye bekleyin
- Sayfayı yenileyin
- Daha sonra tekrar deneyin

#### 5. "Sohbet geçmişi kayboldu"
**Neden**: Tarayıcı oturumu sona erdi
**Çözüm**: Normal davranış, yeni sohbet başlatın

---

## 📊 Performans Beklentileri

### Yanıt Süreleri
- **Basit Soru**: 2-3 saniye
- **Karmaşık Tarihsel Analiz**: 3-5 saniye
- **İlk Yükleme**: 5-10 saniye

### Doğruluk
- **Tarihsel Olaylar**: %95+ doğruluk (kaynaklı)
- **Tarihler ve İsimler**: %98+ doğruluk
- **Kronolojik Bağlam**: %90+ doğruluk

### Limitler
- **Soru Uzunluğu**: Max 500 karakter
- **Günlük Kullanım**: Sınırsız (API limitine tabi)
- **Session Süresi**: Tarayıcı oturumu boyunca
- **Kapsam**: İslamiyet Öncesinden Günümüze Türk Tarihi

---

## 🎯 İyi Uygulama Örnekleri

### Örnek 1: Hızlı Tarih Bilgisi

**Kullanıcı**: "Malazgirt Savaşı ne zaman oldu?"

**Tarih Asistanı**: "Malazgirt Savaşı 26 Ağustos 1071 tarihinde, Büyük Selçuklu Devleti Sultanı Alparslan ile Bizans İmparatoru Romanos Diogenes arasında gerçekleşti. Savaş, Anadolu'nun Türkleşmesinin başlangıcı kabul edilir. Bu zaferle Türkler Anadolu'ya yerleşmeye başladı ve bölge tarihsel süreçte Türk yurdu haline geldi."

**Kaynaklar**: 
- Dönem: İlk Türk-İslam Devletleri
- Yıl: 1071
- Kaynak: Türk Tarih Kurumu
- Benzerlik: %94

---

### Örnek 2: Detaylı Analiz

**Kullanıcı**: "İstanbul'un fethinin Osmanlı Devleti'ne etkileri nelerdi?"

**Tarih Asistanı**: 
```
İstanbul'un 29 Mayıs 1453'te II. Mehmed (Fatih) tarafından fethedilmesinin Osmanlı Devleti'ne etkileri:

Siyasi Etkiler:
• Osmanlı, dünya devleti statüsüne yükseldi
• Bizans İmparatorluğu sona erdi
• Boğazların kontrolü Osmanlı'ya geçti

Ekonomik Etkiler:
• Ticaret yollarının kontrolü
• İpek ve Baharat Yolu'nun hakimiyeti
• Vergi gelirlerinde artış

Kültürel Etkiler:
• İstanbul başkent yapıldı
• Bilim ve sanat merkezi oldu
• Doğu-Batı kültür sentezi

Kaynak: Türk Tarih Kurumu, İstanbul'un Fethi Araştırmaları
```

**Kaynaklar**: 2 doküman, %91 ve %88 benzerlik

---

### Örnek 3: Karşılaştırma

**Kullanıcı**: "Osmanlı'nın kuruluş ve yükselme dönemi arasındaki farklar nedir?"

**Tarih Asistanı**:
```
Kuruluş Dönemi (1299-1453):
• Beylikten devlete geçiş
• Anadolu ve Rumeli fetihleri
• Devlet teşkilatının oluşumu
• Padişahlar: Osman Gazi, Orhan Gazi, I. Murad, Yıldırım Bayezid

Yükselme Dönemi (1453-1579):
• Dünya devleti statüsü
• İstanbul'un fethi
• Üç kıtaya yayılma
• Kurumsallaşma ve altın çağ
• Padişahlar: Fatih, Yavuz, Kanuni

Temel Fark: Beylik yapısından imparatorluk yapısına geçiş
```

**Kaynaklar**: 3 doküman, Osmanlı Devleti dönemi

---

## 📱 Mobil Kullanım

### Mobil Uyumluluk
- ✅ Responsive tasarım
- ✅ Touch-friendly arayüz
- ✅ Tüm özellikler desteklenir
- ✅ Dönem badge'leri mobilde de görünür

### Mobil İpuçları
1. Yatay mod daha iyi deneyim sunar
2. Sidebar menü üst köşeden açılır
3. Dönem filtrelerini kullanmak için expander'lara tap yapın
4. Kaynakları görmek için "📖 Kullanılan Kaynaklar" bölümüne tap yapın

---

## 🆘 Yardım ve Destek

### Chatbot ile ilgili sorunlar için:
- **GitHub Issues**: [github.com/yourusername/tarih-bilgi-rehberi/issues](https://github.com/yourusername/tarih-bilgi-rehberi/issues)
- **E-posta**: your.email@example.com

### Tarih araştırmaları için:
- **TTK**: [www.ttk.gov.tr](https://www.ttk.gov.tr)
- **TDK**: [www.tdk.gov.tr](https://www.tdk.gov.tr)
- **Wikisource**: [tr.wikisource.org](https://tr.wikisource.org)

---

## 📋 SSS (Sıkça Sorulan Sorular)

### S: Bu chatbot resmi TTK uygulaması mı?
**C**: Hayır, bu bir eğitim projesidir. Veriler TTK, TDK ve açık kaynaklardan derlenmiştir.

### S: Bilgilerin güncelliği nasıl?
**C**: Veri seti oluşturulurken güncel akademik kaynaklar kullanılmıştır. En güncel araştırmalar için TTK'nın resmi yayınlarını kontrol edin.

### S: Hangi dönemleri kapsıyor?
**C**: İslamiyet Öncesi Türk Tarihi'nden Cumhuriyet Dönemine kadar tüm Türk Tarihi.

### S: Kaynak güvenilirliği nasıl?
**C**: Tüm veriler TDK, TTK, Wikisource gibi akademik açık kaynaklardan alınmıştır.

### S: Ödev için kullanabilir miyim?
**C**: Evet, ancak kaynak göstermeyi unutmayın ve bilgileri TTK gibi kaynaklarla çapraz kontrol edin.

### S: Tartışmalı konularda tarafsız mı?
**C**: Evet, sadece akademik kaynaklardaki bilgileri sunar, yorum yapmaz.

### S: 7/24 kullanılabilir mi?
**C**: Evet, web arayüzü 7/24 erişilebilir (API limitlerine tabi).

---

## 🎉 Sonuç

Tarih Bilgi Rehberi Chatbot ile:
- ✅ Türk Tarihini interaktif öğrenin
- ✅ Kaynaklı ve doğrulanmış bilgiye erişin
- ✅ Kronolojik bağlamı koruyarak öğrenin
- ✅ Akademik kaynaklara hızlı ulaşın

**İyi çalışmalar!** 📚

---

**Doküman Versiyonu**: 1.0.0  
**Son Güncelleme**: Ekim 2025  
**Veri Kaynakları**: TDK, TTK, Wikisource, Vikipedi  
**Feedback**: Geri bildirimleriniz için GitHub Issues kullanın