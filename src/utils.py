"""
Yardımcı Fonksiyonlar Modülü
Genel kullanım için yardımcı fonksiyonlar
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


# ==================== DİZİN İŞLEMLERİ ====================

def ensure_dir(directory: str) -> Path:
    """
    Dizinin var olduğundan emin ol, yoksa oluştur
    
    Args:
        directory: Dizin yolu
        
    Returns:
        Path objesi
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def list_files(directory: str, extensions: List[str] = None) -> List[Path]:
    """
    Dizindeki dosyaları listele
    
    Args:
        directory: Dizin yolu
        extensions: Filtrelenecek uzantılar (örn: ['.txt', '.pdf'])
        
    Returns:
        Dosya Path listesi
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return []
    
    if extensions:
        files = []
        for ext in extensions:
            files.extend(dir_path.glob(f"*{ext}"))
        return sorted(files)
    else:
        return sorted([f for f in dir_path.iterdir() if f.is_file()])


def get_file_size(filepath: str) -> str:
    """
    Dosya boyutunu human-readable formatta döndür
    
    Args:
        filepath: Dosya yolu
        
    Returns:
        Boyut string (örn: "1.5 MB")
    """
    size_bytes = os.path.getsize(filepath)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"


# ==================== METIN İŞLEMLERİ ====================

def clean_text(text: str) -> str:
    """
    Metni temizle
    
    Args:
        text: Ham metin
        
    Returns:
        Temizlenmiş metin
    """
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text)
    
    # Özel karakterleri temizle (Türkçe karakterleri koru)
    text = re.sub(r'[^\w\sğüşıöçĞÜŞİÖÇ.,!?():;/-]', '', text)
    
    # Baştan ve sondan boşlukları kaldır
    text = text.strip()
    
    return text


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Metni belirli uzunlukta kes
    
    Args:
        text: Metin
        max_length: Maksimum uzunluk
        suffix: Ek (örn: "...")
        
    Returns:
        Kesilmiş metin
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-len(suffix)] + suffix


def count_words(text: str) -> int:
    """
    Metindeki kelime sayısını say
    
    Args:
        text: Metin
        
    Returns:
        Kelime sayısı
    """
    return len(text.split())


def extract_sentences(text: str) -> List[str]:
    """
    Metni cümlelere ayır
    
    Args:
        text: Metin
        
    Returns:
        Cümle listesi
    """
    # Basit cümle ayırma (nokta, ünlem, soru işareti)
    sentences = re.split(r'[.!?]+', text)
    
    # Boş cümleleri temizle
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


# ==================== JSON İŞLEMLERİ ====================

def load_json(filepath: str) -> Any:
    """
    JSON dosyası yükle
    
    Args:
        filepath: Dosya yolu
        
    Returns:
        JSON içeriği
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, filepath: str, indent: int = 2):
    """
    Veriyi JSON olarak kaydet
    
    Args:
        data: Kaydedilecek veri
        filepath: Kayıt yolu
        indent: Girinti seviyesi
    """
    ensure_dir(os.path.dirname(filepath))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ==================== TİMER İŞLEMLERİ ====================

class Timer:
    """Basit timer sınıfı"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Timer'ı başlat"""
        self.start_time = time.time()
    
    def stop(self) -> float:
        """Timer'ı durdur ve geçen süreyi döndür"""
        self.end_time = time.time()
        return self.elapsed()
    
    def elapsed(self) -> float:
        """Geçen süreyi döndür (saniye)"""
        if self.start_time is None:
            return 0.0
        
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def elapsed_str(self) -> str:
        """Geçen süreyi string olarak döndür"""
        elapsed = self.elapsed()
        
        if elapsed < 1:
            return f"{elapsed*1000:.0f}ms"
        elif elapsed < 60:
            return f"{elapsed:.1f}s"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            return f"{minutes}m {seconds:.0f}s"


def measure_time(func):
    """Fonksiyon çalışma süresini ölçen decorator"""
    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()
        result = func(*args, **kwargs)
        elapsed = timer.stop()
        print(f"⏱️  {func.__name__} tamamlandı: {timer.elapsed_str()}")
        return result
    return wrapper


# ==================== LOGGER ====================

class SimpleLogger:
    """Basit logger sınıfı"""
    
    def __init__(self, log_file: Optional[str] = None, verbose: bool = True):
        """
        Args:
            log_file: Log dosyası yolu (opsiyonel)
            verbose: Konsola yazdır
        """
        self.log_file = log_file
        self.verbose = verbose
        
        if log_file:
            ensure_dir(os.path.dirname(log_file))
    
    def _write(self, level: str, message: str):
        """Log mesajı yaz"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        # Konsola yazdır
        if self.verbose:
            print(log_message)
        
        # Dosyaya yaz
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
    
    def info(self, message: str):
        """Info log"""
        self._write("INFO", message)
    
    def warning(self, message: str):
        """Warning log"""
        self._write("WARNING", message)
    
    def error(self, message: str):
        """Error log"""
        self._write("ERROR", message)
    
    def debug(self, message: str):
        """Debug log"""
        self._write("DEBUG", message)


# ==================== PROGRESS BAR ====================

class ProgressBar:
    """Basit progress bar"""
    
    def __init__(self, total: int, prefix: str = "", width: int = 50):
        """
        Args:
            total: Toplam adım sayısı
            prefix: Ön ek
            width: Bar genişliği
        """
        self.total = total
        self.prefix = prefix
        self.width = width
        self.current = 0
    
    def update(self, step: int = 1):
        """Progress'i güncelle"""
        self.current += step
        self._print()
    
    def _print(self):
        """Progress bar'ı yazdır"""
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        
        print(f"\r{self.prefix} |{bar}| {percent*100:.1f}% ({self.current}/{self.total})", end='')
        
        if self.current >= self.total:
            print()  # Yeni satır


# ==================== VERI YAPILARI ====================

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Listeyi chunk'lara böl
    
    Args:
        lst: Liste
        chunk_size: Chunk boyutu
        
    Returns:
        Chunk listesi
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    İç içe listeyi düzleştir
    
    Args:
        nested_list: İç içe liste
        
    Returns:
        Düz liste
    """
    return [item for sublist in nested_list for item in sublist]


def remove_duplicates(lst: List[Any], key=None) -> List[Any]:
    """
    Listeden tekrarları kaldır
    
    Args:
        lst: Liste
        key: Karşılaştırma key fonksiyonu (opsiyonel)
        
    Returns:
        Benzersiz öğelerin listesi
    """
    if key is None:
        return list(dict.fromkeys(lst))
    
    seen = set()
    result = []
    for item in lst:
        k = key(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    
    return result


# ==================== FORMAT İŞLEMLERİ ====================

def format_number(num: float, decimals: int = 2) -> str:
    """
    Sayıyı formatla (binlik ayraçlı)
    
    Args:
        num: Sayı
        decimals: Ondalık basamak sayısı
        
    Returns:
        Formatlanmış string
    """
    return f"{num:,.{decimals}f}".replace(',', '.')


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Yüzde formatla
    
    Args:
        num: 0-1 arası sayı
        decimals: Ondalık basamak sayısı
        
    Returns:
        Yüzde string (örn: "75.5%")
    """
    return f"{num*100:.{decimals}f}%"


def format_duration(seconds: float) -> str:
    """
    Süreyi formatla
    
    Args:
        seconds: Saniye
        
    Returns:
        Formatlanmış süre (örn: "2m 30s")
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


# ==================== TEST FONKSİYONU ====================

def test_utils():
    """Utility fonksiyonlarını test et"""
    print("\n" + "="*60)
    print("UTILS MODÜLÜ TEST")
    print("="*60 + "\n")
    
    # Timer testi
    print("⏱️  Timer testi:")
    timer = Timer()
    timer.start()
    time.sleep(0.5)
    print(f"   Geçen süre: {timer.elapsed_str()}\n")
    
    # Metin işleme testi
    print("📝 Metin işleme testi:")
    text = "   Bu    bir  test   metnidir!!! Çok  fazla  boşluk   var.   "
    cleaned = clean_text(text)
    print