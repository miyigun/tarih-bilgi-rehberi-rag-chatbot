"""
Retrieval İşlemleri Modülü
FAISS ile similarity search ve retrieval işlemleri
"""

import faiss
import numpy as np
from typing import List, Dict, Tuple
import json
from pathlib import Path


class FAISSRetriever:
    """FAISS tabanlı retrieval sınıfı"""
    
    def __init__(self, index_path: str = "models/faiss_index", dimension: int = 384):
        """
        Args:
            index_path: FAISS index dizini
            dimension: Embedding vektör boyutu
        """
        self.index_path = Path(index_path)
        self.dimension = dimension
        self.index = None
        self.chunk_list = []
        
        # Index varsa yükle
        if (self.index_path / "index.faiss").exists():
            self.load_index()
    
    def create_index(self, embeddings: np.ndarray, metadata: List[Dict] = None):
        """
        Yeni FAISS index oluştur
        
        Args:
            embeddings: Embedding vektörleri matrisi (n_docs x dimension)
            metadata: Her embedding için metadata listesi
        """
        print("🔧 FAISS index oluşturuluyor...")
        
        # L2 (Euclidean) distance yerine IndexFlatIP (Inner Product) kullan
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Embeddings'i ekle
        embeddings = embeddings.astype('float32')
        # Not: data_processing.py'nin vektörleri L2-normalize etmesi GEREKİR
        self.index.add(embeddings)
        
        print(f"✅ Index oluşturuldu (toplam vektör: {self.index.ntotal})")
        
        # Metadata'yı sakla
        if metadata:
           self.chunk_list = metadata
    
    def save_index(self, metadata_list: List[Dict] = None):
        """
        Index'i diske kaydet
        
        Args:
            metadata_list: Kaydedilecek metadata listesi
        """
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # FAISS index'i kaydet
        index_file = self.index_path / "index.faiss"
        faiss.write_index(self.index, str(index_file))
        print(f"💾 FAISS index kaydedildi: {index_file}")
        
        # Metadata'yı kaydet
        if metadata_list or self.chunk_list:
            metadata_file = self.index_path / "metadata.json"
            metadata_to_save = metadata_list if metadata_list else self.chunk_list
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_to_save, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Metadata (chunk listesi) kaydedildi: {metadata_file}")
    
    def load_index(self):
        """Index'i diskten yükle"""
        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.json"
        
        if not index_file.exists():
            raise FileNotFoundError(f"Index dosyası bulunamadı: {index_file}")
        
        # FAISS index'i yükle
        self.index = faiss.read_index(str(index_file))
        print(f"📂 FAISS index yüklendi: {self.index.ntotal} vektör")
        
        # Metadata'yı yükle
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                self.chunk_list = json.load(f)  # Bu artık bir liste
            print(f"📂 Metadata yüklendi: {len(self.chunk_list)} kayıt")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Query için benzer vektörleri bul
        
        Args:
            query_embedding: Query embedding vektörü
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            (distances, indices) tuple'ı
        """
        if self.index is None:
            raise ValueError("Index yüklenmemiş! Önce create_index veya load_index çağırın.")
        
        # Query'yi uygun formata çevir
        query_embedding = query_embedding.astype('float32').reshape(1, -1)

        # IndexFlatIP için sorgu vektörünü normalize et ***
        faiss.normalize_L2(query_embedding)
        
        # Arama yap
        # IndexFlatIP kullanıldığında, 'distances' aslında 'similarity scores' (benzerlik skorları) olur
        similarities, indices = self.index.search(query_embedding, top_k)
        
        return similarities[0], indices[0]
    
    def retrieve(self, query_embedding: np.ndarray, 
                top_k: int = 5, 
                threshold: float = None) -> List[Dict]:
        """
        Query için alakalı dokümanları al
        
        Args:
            query_embedding: Query embedding vektörü
            top_k: Döndürülecek sonuç sayısı
            threshold: Minimum benzerlik eşiği (opsiyonel)
            
        Returns:
            Alakalı dokümanların metadata listesi
        """
        # Arama yap
        similarities, indices = self.search(query_embedding, top_k)
        
        # Sonuçları hazırla
        results = []
        for similarity_score, idx in zip(similarities, indices):
            
            # Threshold kontrolü
            if threshold and similarity_score < threshold:
                continue
            
            # Metadata'yı ekle
            result = {
                "index": int(idx),
                "distance": float(1 - similarity_score), # Mesafeyi 1-similarity olarak hesapla
                "similarity": float(similarity_score)
            }
            
            # Metadata varsa ekle
            if self.chunk_list and idx < len(self.chunk_list):
                result.update(self.chunk_list[idx])
            
            results.append(result)
        
        return results
    
    def add_vectors(self, new_embeddings: np.ndarray, new_metadata: List[Dict] = None):
        """
        Mevcut index'e yeni vektörler ekle
        
        Args:
            new_embeddings: Yeni embedding vektörleri
            new_metadata: Yeni metadata listesi
        """
        if self.index is None:
            raise ValueError("Index yüklenmemiş!")
        
        # Vektörleri ekle
        new_embeddings = new_embeddings.astype('float32')
        # *** Yeni vektörleri de normalize et ***
        faiss.normalize_L2(new_embeddings)
        self.index.add(new_embeddings)
        
        # Metadata'yı güncelle
        if new_metadata and self.chunk_list is not None:
            self.chunk_list.extend(new_metadata)
        
        print(f"✅ {len(new_embeddings)} yeni vektör eklendi (toplam: {self.index.ntotal})")
    
    def get_stats(self) -> Dict:
        """
        Index istatistiklerini döndür
        
        Returns:
            İstatistik dictionary
        """
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "index_type": type(self.index).__name__ if self.index else None,
            "metadata_count": len(self.chunk_list) if self.chunk_list else 0
        }


class HybridRetriever:
    """Hybrid retrieval (semantic + keyword) sınıfı"""
    
    def __init__(self, faiss_retriever: FAISSRetriever, alpha: float = 0.7):
        """
        Args:
            faiss_retriever: FAISS retriever instance
            alpha: Semantic search ağırlığı (0-1 arası)
        """
        self.faiss_retriever = faiss_retriever
        self.alpha = alpha  # Semantic weight
        self.beta = 1 - alpha  # Keyword weight
    
    def keyword_search(self, query: str, documents: List[str], top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Basit keyword tabanlı arama
        
        Args:
            query: Arama sorgusu
            documents: Doküman listesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            (index, score) tuple'larının listesi
        """
        query_words = set(query.lower().split())
        
        scores = []
        for idx, doc in enumerate(documents):
            doc_words = set(doc.lower().split())
            
            # Jaccard similarity
            intersection = len(query_words.intersection(doc_words))
            union = len(query_words.union(doc_words))
            
            score = intersection / union if union > 0 else 0
            scores.append((idx, score))
        
        # Skora göre sırala
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def hybrid_search(self, query_embedding: np.ndarray, 
                     query_text: str,
                     documents: List[str],
                     top_k: int = 5) -> List[Dict]:
        """
        Hybrid search: semantic + keyword
        
        Args:
            query_embedding: Query embedding vektörü
            query_text: Query metni
            documents: Doküman listesi
            top_k: Döndürülecek sonuç sayısı
            
        Returns:
            Sonuç listesi
        """
        # Semantic search
        semantic_results = self.faiss_retriever.retrieve(query_embedding, top_k=top_k*2)
        
        # Keyword search
        keyword_results = self.keyword_search(query_text, documents, top_k=top_k*2)
        
        # Skorları birleştir
        combined_scores = {}
        
        for result in semantic_results:
            idx = result['index']
            combined_scores[idx] = self.alpha * result['similarity']
        
        for idx, score in keyword_results:
            if idx in combined_scores:
                combined_scores[idx] += self.beta * score
            else:
                combined_scores[idx] = self.beta * score
        
        # Sırala ve top-k'yı al
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        # Sonuçları formatla
        final_results = []
        for idx, score in sorted_results:
            result = {
                "index": idx,
                "hybrid_score": score,
                "document": documents[idx] if idx < len(documents) else None
            }
            final_results.append(result)
        
        return final_results


def test_retrieval():
    """Retrieval modülünü test et"""
    print("\n" + "="*60)
    print("RETRIEVAL MODÜLÜ TEST (IndexFlatIP)")
    print("="*60 + "\n")
    
    # Test embeddings oluştur
    print("🔧 Test embeddings oluşturuluyor...")
    dimension = 384
    n_docs = 10
    
    # Random embeddings (test için)
    np.random.seed(42)
    embeddings = np.random.randn(n_docs, dimension).astype('float32')

    # Normalize et (IP için ZORUNLU)
    faiss.normalize_L2(embeddings)
    
    # Metadata oluştur (Artık chunk listesi formatında)
    metadata = [
        {"content": f"Test dokümanı {i+1}", "metadata": {"source": f"doc_{i+1}.txt"}}
        for i in range(n_docs)
    ]
    
    # Retriever oluştur
    retriever = FAISSRetriever(index_path="models/test_index", dimension=dimension)
    
    # Index oluştur
    retriever.create_index(embeddings, metadata)
    
    # Index'i kaydet
    retriever.save_index() # Artık metadata'yı (chunk_list) doğru kaydediyor
    
    # Test query
    print("\n🔍 Test query oluşturuluyor...")
    query_embedding = np.random.randn(dimension).astype('float32')
    
    # Arama yap
    print("\n📊 Arama yapılıyor...")
    results = retriever.retrieve(query_embedding, top_k=5)
    
    print(f"✅ {len(results)} sonuç bulundu:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Doküman: {result.get('content', 'N/A')}")
        print(f"   Similarity: {result['similarity']:.4f}") # Artık bu direkt Kosinüs Benzerliği
        print(f"   Distance: {result['distance']:.4f}\n") # Bu (1 - Similarity)
    
    # İstatistikler
    stats = retriever.get_stats()
    print("📈 Index İstatistikleri:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ TEST TAMAMLANDI")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_retrieval()