"""
RAG Sistemi - Tarih Bilgi Rehberi
FAISS index'ten arama yapar ve Gemini ile yanıt üretir
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

# src klasörünü path'e ekle - KRİTİK!
sys.path.append(str(Path(__file__).parent))

from retrieval import FAISSRetriever

# Environment variables yükle
load_dotenv()


class RAGSystem:
    """Tarih RAG sistemi sınıfı - Retrieval ve Generation işlemleri"""
    
    def __init__(self, index_dir: str = "models/faiss_index"):
        """
        Args:
            index_dir: FAISS index dizini
        """
        self.index_dir = Path(index_dir)

        # Lokal modelin yolu
        LOCAL_MODEL_PATH = "models/embeddings/paraphrase-multilingual-MiniLM-L12-v2"
        
        # Embedding model yükle
        print(f"🔄 Embedding model yükleniyor... (Lokal: {LOCAL_MODEL_PATH})")
        self.embedding_model = SentenceTransformer(
            LOCAL_MODEL_PATH
        )       
        
        # FAISS index yükle
        print("🔄 FAISSRetriever başlatılıyor ve index yükleniyor...")
        self.retriever = FAISSRetriever(index_path=index_dir)
        
        # Metadata yükle
        with open(self.index_dir / "metadata.json", 'r', encoding='utf-8') as f:
            # metadata.json zaten bir liste, dict değil
            self.chunks = json.load(f) 
            self.metadata = self.chunks # veya self.metadata'yı hiç kullanmayın
        
        # Gemini API yapılandır
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        genai.configure(api_key=api_key)

        # Gemini model - önce 2.0 dene, yoksa 2.5'a geç
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        print(f"✅ Tarih RAG sistemi hazır (Toplam chunk: {len(self.chunks)})\n")
    
    def retrieve(self, query: str, top_k: int = 5, threshold: float = 0.3) -> List[Dict]:
        """
        Sorgu için en alakalı chunk'ları bulur
        
        Args:
            query: Kullanıcı sorusu
            top_k: Döndürülecek chunk sayısı
            threshold: Minimum benzerlik skoru (0-1 arası)
            
        Returns:
            Alakalı chunk'ların listesi
        """
        # Sorgu için embedding oluştur
        query_embedding = self.embedding_model.encode([query])[0]
        
        # FAISS ile arama yap
        similarities, indices = self.retriever.search(query_embedding, top_k)

        # Sonuçları hazırla
        results = []
        for similarity_score, idx in zip(similarities, indices):
            # Gelen değer zaten benzerlik skoru!
            # similarity = 1 / (1 + dist) <-- BU SATIRI SİLİN
            
            if similarity_score >= threshold:
                # data_processing.py'nin kaydettiği formatı kullan
                # (self.chunks[idx] zaten hem 'content' hem 'metadata' içerir)
                chunk_data = self.chunks[idx].copy() 
                chunk_data['similarity_score'] = float(similarity_score)
                # distance'ı (1-sim) olarak hesaplayabilirsiniz (opsiyonel)
                chunk_data['distance'] = float(1 - similarity_score) 
                results.append(chunk_data)
        
        return results
    
    def generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Context chunk'larını kullanarak yanıt üretir
        
        Args:
            query: Kullanıcı sorusu
            context_chunks: Alakalı chunk'lar
            
        Returns:
            Üretilen yanıt
        """
        if not context_chunks:
            return "Üzgünüm, bu konu hakkında bilgim bulunmuyor. Lütfen farklı bir soru sorun veya sorunuzu daha spesifik hale getirin."
        
        # Context'i hazırla (tarihsel metadata dahil)
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            metadata = chunk.get('metadata', {})
            donem = metadata.get('donem', 'Bilinmiyor')
            yil = metadata.get('yil', '')
            kaynak = metadata.get('kaynak', 'Bilinmiyor')
            
            context_part = f"Kaynak {i} ({donem}"
            if yil:
                context_part += f", {yil}"
            context_part += f" - {kaynak}):\n{chunk['content']}"
            
            context_parts.append(context_part)
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        # Prompt oluştur (Tarih asistanı için özelleştirilmiş)
        prompt = f"""Sen Türk Tarihi konusunda uzmanlaşmış bir yapay zeka asistanısın. Görevin, sana verilen BİLGİ BANKASI'ndaki tarihsel verileri kullanarak kullanıcının KULLANICI SORUSU'na akademik, net ve öğretici bir yanıt vermektir.

            BİLGİ BANKASI:
            {context_text}

            KULLANICI SORUSU:
            {query}

            YANIT KURALLARI:
            1. Sadece verilen bilgi bankasındaki bilgileri kullan
            2. Türkçe, akademik ama anlaşılır bir dil kullan
            3. Tarihsel olayları kronolojik sırada ve bağlamıyla anlat
            4. Tarihleri, isimleri ve yerleri net olarak belirt
            5. Kaynak referanslarını belirt (Türk Tarih Kurumu, TDK vb.)
            6. Bilgi bankasında yoksa, "Bu konuda şu an elimde detaylı bilgi yok" de
            7. Emoji kullanma, ciddi ve akademik ol
            8. Karmaşık olayları basit ve anlaşılır şekilde açıkla
            9. Önemli tarihleri ve isimleri vurgula

            YANIT:
        """
        
        try:
            # Gemini ile yanıt üret
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Yanıt üretilirken bir hata oluştu: {str(e)}"
    
    def query(self, user_question: str, top_k: int = 5) -> Dict:
        """
        Tam RAG pipeline: Retrieve + Generate
        
        Args:
            user_question: Kullanıcı sorusu
            top_k: Aranacak chunk sayısı
            
        Returns:
            Yanıt ve metadata içeren dictionary
        """
        print(f"\n📝 Soru: {user_question}")
        
        # 1. Retrieve
        print("🔍 İlgili tarihsel bilgiler aranıyor...")
        retrieved_chunks = self.retrieve(user_question, top_k=top_k)
        
        print(f"✅ {len(retrieved_chunks)} alakalı kayıt bulundu")
        
        # 2. Generate
        print("🤖 Yanıt oluşturuluyor...")
        response = self.generate_response(user_question, retrieved_chunks)
        
        print("✅ Yanıt hazır\n")
        
        # Sonuçları döndür
        return {
            "query": user_question,
            "response": response,
            "sources": [
                {
                    "content": chunk['content'][:200] + "...",
                    "donem": chunk['metadata'].get('donem', 'Bilinmiyor'),
                    "yil": chunk['metadata'].get('yil', ''),
                    "kaynak": chunk['metadata'].get('kaynak', 'Bilinmiyor'),
                    "similarity": chunk['similarity_score']  # ← 'similarity' yerine 'similarity_score'
                }
                for chunk in retrieved_chunks
            ],
            "num_sources": len(retrieved_chunks)
        }


def main():
    """Test fonksiyonu"""
    print("\n" + "="*60)
    print("TARİH BİLGİ REHBERİ - RAG SİSTEMİ TEST")
    print("="*60 + "\n")
    
    # RAG sistemi başlat
    try:
        rag = RAGSystem()
    except FileNotFoundError:
        print("❌ FAISS index bulunamadı!")
        print("Lütfen önce veri işleme script'ini çalıştırın:")
        print("   python src/data_processing.py")
        return
    except Exception as e:
        print(f"❌ Hata: {e}")
        return
    
    # Test soruları
    test_questions = [
        "Osmanlı Devleti ne zaman ve kim tarafından kuruldu?",
        "Milli Mücadele'deki önemli kongreler nelerdir?",
        "Göktürklerin Türk tarihindeki önemi nedir?",
        "Atatürk'ün ilkeleri nelerdir?",
        "Malazgirt Savaşı'ndan sonra kurulan beylikler hangileridir?"           
    ]
    
    for question in test_questions:
        result = rag.query(question)
        
        print("="*60)
        print(f"SORU: {result['query']}")
        print("-"*60)
        print(f"YANIT:\n{result['response']}")
        print("-"*60)
        print(f"KAYNAKLAR: {result['num_sources']} kayıt kullanıldı")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. Dönem: {source['donem']}")
            if source['yil']:
                print(f"     Yıl: {source['yil']}")
            print(f"     Benzerlik: {source['similarity']:.2f}")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()