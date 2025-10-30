"""
Veri İşleme Modülü - Tarih Bilgi Rehberi
Bu modül JSON formatındaki tarih verilerini yükler, işler ve FAISSRetriever
sınıfını kullanarak bir FAISS index'i oluşturur ve kaydeder.
"""
import json
from pathlib import Path
from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from utils import clean_text 

class DataProcessor:
    """Tarih verisi işleme ve embedding oluşturma sınıfı"""
    
    def __init__(self, data_dir: str = "data/raw", model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Args:
            data_dir: JSON veri dosyalarının bulunduğu dizin
            model_name: Kullanılacak embedding model(Lokal yoldan)
        """
        self.data_dir = Path(data_dir)
        print(f"🔄 Embedding model yükleniyor... (Hugging Face: {model_name})")
        self.embedding_model = SentenceTransformer(model_name)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""]
        )
        
    def load_json_data(self) -> List[Document]:
        """
        JSON formatındaki tarih verilerini yükler ve Document'lere dönüştürür
        
        Returns:
            Document nesnelerinin listesi
        """
        documents = []
        
        print(f"📂 Tarih verileri yükleniyor: {self.data_dir}")
        
        # JSON dosyalarını bul
        json_files = list(self.data_dir.glob('*.json'))
        
        if not json_files:
            print("⚠️  Hiç JSON dosyası bulunamadı!")
            return documents
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # JSON yapısı kontrol et
                if not isinstance(data, list):
                    print(f"  ⚠️  {json_file.name}: Liste formatında değil, atlanıyor")
                    continue
                
                # Her tarihsel kayıt için Document oluştur
                for item in data:
                    # Veri formatı kontrolü
                    if not isinstance(item, dict):
                        continue
                    
                    # İçerik oluştur: konu + icerik + anahtar kelimeler
                    content_parts = []
                    
                    # Konu başlığı
                    if 'konu' in item:
                        content_parts.append(f"Konu: {item['konu']}")
                    
                    # Ana içerik
                    if 'icerik' in item:
                        content_parts.append(item['icerik'])
                    
                    # Anahtar kelimeleri ekle (arama için önemli)
                    if 'anahtar_kelimeler' in item and item['anahtar_kelimeler']:
                        keywords = ', '.join(item['anahtar_kelimeler'])
                        content_parts.append(f"Anahtar Kelimeler: {keywords}")
                    
                    # İçeriği birleştir
                    content = '\n\n'.join(content_parts)
                    
                    if not content.strip():
                        continue
                    
                    # Metadata oluştur (zengin metadata RAG için kritik)
                    metadata = {
                        'id': item.get('id', 'unknown'),
                        'donem': item.get('donem', ''),
                        'alt_donem': item.get('alt_donem', ''),
                        'kategori_ana': item.get('kategori', {}).get('ana', ''),
                        'kategori_alt': item.get('kategori', {}).get('alt', ''),
                        'konu': item.get('konu', ''),
                        'yil': item.get('yil', 0),
                        'etiketler': item.get('etiketler', []),
                        'kaynak': item.get('kaynak', ''),
                        'kaynak_turu': item.get('kaynak_turu', ''),
                        'referans_link': item.get('referans_link', ''),
                        'source': str(json_file),
                        'filename': json_file.name
                    }
                    
                    # Document oluştur
                    doc = Document(
                        page_content=content,
                        metadata=metadata
                    )
                    documents.append(doc)
                
                print(f"  ✓ {json_file.name}: {len([x for x in data if isinstance(x, dict)])} kayıt yüklendi")
                
            except json.JSONDecodeError as e:
                print(f"  ✗ {json_file.name}: JSON parse hatası - {str(e)}")
            except Exception as e:
                print(f"  ✗ {json_file.name}: {str(e)}")
        
        print(f"\n✅ Toplam {len(documents)} tarihsel kayıt yüklendi\n")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Dokümanları chunk'lara böler
        
        Args:
            documents: Document listesi
            
        Returns:
            Chunk'lanmış document listesi
        """
        print("✂️  Dokümanlar chunk'lara bölünüyor...")
        
        all_chunks = []
        for doc in documents:
            # Metni temizle (utils'den gelen fonksiyonu kullan)
            cleaned_content = clean_text(doc.page_content)
            doc.page_content = cleaned_content
            
            # Chunk'lara böl
            chunks = self.text_splitter.split_documents([doc])
            
            # Her chunk'a orijinal metadata'yı koru
            for chunk in chunks:
                chunk.metadata.update(doc.metadata)
            
            all_chunks.extend(chunks)
        
        print(f"✅ {len(all_chunks)} chunk oluşturuldu\n")
        return all_chunks
    
    def create_embeddings(self, chunks: List[Document]) -> np.ndarray:
        """
        Chunk'lar için embedding vektörleri oluşturur
        
        Args:
            chunks: Document chunk'ları
            
        Returns:
            Embedding vektörü matrisi (n_chunks x dimension)
        """
        print("🧮 Embedding'ler oluşturuluyor...")
        
        texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32
        )
        
        # Kosinüs benzerliği için L2 Normalizasyonu ekle
        embeddings = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings)
        print("✅ Embedding'ler normalize edildi (L2)")
        
        print(f"✅ {len(embeddings)} embedding oluşturuldu\n")
        return embeddings
    
    def create_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        FAISS index oluşturur
        
        Args:
            embeddings: Embedding vektörleri
            
        Returns:
            FAISS index
        """
        print("🔍 FAISS index oluşturuluyor...")
        
        # L2 (Euclidean) yerine IP (Inner Product/Cosine) kullan
        index = faiss.IndexFlatIP(self.dimension)
        
        # Embeddings'i ekle
        index.add(embeddings.astype('float32'))
        
        print(f"✅ FAISS index (IndexFlatIP) oluşturuldu (toplam vektör: {index.ntotal})\n")
        return index
    
    def save_index(self, index: faiss.Index, chunks: List[Document], output_dir: str = "models/faiss_index"):
        """
        FAISS index'i ve metadata'yı kaydeder
        
        Args:
            index: FAISS index
            chunks: Document chunk'ları
            output_dir: Kayıt dizini
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Index kaydediliyor: {output_path}")
        
        # FAISS index'i kaydet
        faiss.write_index(index, str(output_path / "index.faiss"))
        
        # Metadata'yı FAISSRetriever'ın beklediği gibi
        # doğrudan bir "chunk listesi" olarak kaydet.
        metadata_list = [
            {
                "content": chunk.page_content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
        
        with open(output_path / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Index ve metadata (chunk listesi) kaydedildi\n")
        
        # İstatistikleri ayrı bir dosyaya (veya sadece konsola) yaz
        stats = {
            "total_chunks": len(chunks),
            "dimension": self.dimension,
            "model_name": self.embedding_model._modules['0'].auto_model.name_or_path,
            "data_source": "Tarih Bilgi Rehberi - Türk Tarihi",
            "periods": list(set([chunk.metadata.get('donem', '') for chunk in chunks if chunk.metadata.get('donem')]))
        }
        with open(output_path / "stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print("✅ İstatistikler 'stats.json' dosyasına kaydedildi.")

    
    def process_all(self):
        """Tüm veri işleme pipeline'ını çalıştırır"""
        print("\n" + "="*60)
        print("TARİH BİLGİ REHBERİ - VERİ İŞLEME PİPELİNE")
        print("="*60 + "\n")
        
        # 1. JSON verilerini yükle
        documents = self.load_json_data()
        
        if not documents:
            print("⚠️  Hiç veri bulunamadı!")
            print("📋 Beklenen format:")
            print("   data/raw/islamiyet_oncesi.json")
            print("   data/raw/ilk_turk_islam_devletleri.json")
            print("   data/raw/anadolu_beylikleri.json")
            print("   data/raw/osmanli_devleti.json")
            print("   data/raw/milli_mucadele.json")
            print("   data/raw/cumhuriyet.json")
            return
        
        # 2. Chunk'lara böl
        chunks = self.split_documents(documents)
        
        # 3. Embedding'leri oluştur
        embeddings = self.create_embeddings(chunks)
        
        # 4. FAISS index oluştur
        index = self.create_faiss_index(embeddings)
        
        # 5. Kaydet
        self.save_index(index, chunks)
        
        print("="*60)
        print("✅ VERİ İŞLEME TAMAMLANDI!")
        print("="*60 + "\n")
        print(f"📊 İstatistikler:")
        print(f"   • Toplam tarihsel kayıt: {len(documents)}")
        print(f"   • Toplam chunk: {len(chunks)}")
        print(f"   • Embedding boyutu: {self.dimension}")
        print(f"   • Model: {self.embedding_model._modules['0'].auto_model.name_or_path}")
        
        # Dönem bazlı istatistikler
        donem_counts = {}
        for chunk in chunks:
            donem = chunk.metadata.get('donem', 'Bilinmiyor')
            donem_counts[donem] = donem_counts.get(donem, 0) + 1
        
        print(f"\n📚 Dönem Bazlı Dağılım:")
        for donem, count in sorted(donem_counts.items()):
            print(f"   • {donem}: {count} chunk")
        print()


def main():
    """Ana fonksiyon"""
    # Veri dizini kontrolü
    data_dir = Path("data/raw")
    
    if not data_dir.exists():
        print("⚠️  data/raw klasörü bulunamadı. Oluşturuluyor...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print("\n📋 Lütfen JSON veri dosyalarınızı data/raw/ klasörüne koyun:")
        print("   • islamiyet_oncesi.json")
        print("   • ilk_turk_islam_devletleri.json")
        print("   • anadolu_beylikleri.json")
        print("   • osmanli_devleti.json")
        print("   • milli_mucadele.json")
        print("   • cumhuriyet.json")
        return
    
    # JSON dosyası var mı kontrol et
    json_files = list(data_dir.glob('*.json'))
    if not json_files:
        print("⚠️  data/raw klasöründe JSON dosyası bulunamadı!")
        print("\n📋 Beklenen dosyalar:")
        print("   • islamiyet_oncesi.json")
        print("   • ilk_turk_islam_devletleri.json")
        print("   • anadolu_beylikleri.json")
        print("   • osmanli_devleti.json")
        print("   • milli_mucadele.json")
        print("   • cumhuriyet.json")
        return
    
    # Veri işleme pipeline'ını başlat
    processor = DataProcessor()
    processor.process_all()


if __name__ == "__main__":
    main()