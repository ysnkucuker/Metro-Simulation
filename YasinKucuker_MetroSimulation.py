from collections import defaultdict, deque  
import heapq  
from typing import Dict, List, Set, Tuple, Optional  
import networkx as nx  # Graph oluşturma, analiz ve görselleştirme için NetworkX kütüphanesi
import matplotlib.pyplot as plt  # Grafik çizimleri ve görselleştirme için Matplotlib
from collections import deque  # 'deque' veri yapısı, hızlı ekleme ve çıkarma işlemleri için kullanılır


class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        kuyruk = deque([(baslangic, [baslangic])])  # (mevcut istasyon, şu ana kadar olan rota)
        ziyaret_edildi = set()

        while kuyruk:
            mevcut_istasyon, yol = kuyruk.popleft()

            if mevcut_istasyon == hedef:
                return yol  # Hedefe ulaştık, en kısa aktarma rotasını döndür

            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, yol + [komsu]))  # Yeni rota oluştur ve kuyruğa ekle

        return None  # Eğer hedefe ulaşamazsak None döndür


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur"""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        pq = [(0, id(baslangic), baslangic, [baslangic])]  # (toplam süre, öncelik, istasyon, rota)
        ziyaret_edildi = {}
        
        while pq:
            toplam_sure, _, mevcut_istasyon, yol = heapq.heappop(pq)
            
            if mevcut_istasyon == hedef:
                return yol, toplam_sure
            
            if mevcut_istasyon in ziyaret_edildi and ziyaret_edildi[mevcut_istasyon] <= toplam_sure:
                continue
            
            ziyaret_edildi[mevcut_istasyon] = toplam_sure
            
            for komsu, sure in mevcut_istasyon.komsular:
                yeni_sure = toplam_sure + sure
                heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yol + [komsu]))
        
        return None


class MetroGraph:
    def __init__(self, metro_agi):
        self.metro_agi = metro_agi
        self.graph = nx.Graph()
    
    def hat_grafigi_olustur(self, hat_adi):
        """Belirli bir hattın grafiğini oluşturur."""
        if hat_adi not in self.metro_agi.hatlar:
            print(f"{hat_adi} bulunamadı! Mevcut hatlar: {list(self.metro_agi.hatlar.keys())}")
            return
        
        kuyruk = deque(self.metro_agi.hatlar[hat_adi])
        while kuyruk:
            istasyon = kuyruk.popleft()
            for komsu, sure in istasyon.komsular:
                if komsu.hat == hat_adi:  # Sadece aynı hat içindeki bağlantılar
                    self.graph.add_edge(istasyon.ad, komsu.ad, weight=sure)
    
    def tum_metro_grafigi_olustur(self):
        """Tüm metro sistemini tek bir grafik olarak oluşturur."""
        for istasyon in self.metro_agi.istasyonlar.values():
            for komsu, sure in istasyon.komsular:
                self.graph.add_edge(istasyon.ad, komsu.ad, weight=sure)
    
    def grafigi_goster(self, baslik="Metro Haritası"):
        """Grafiği çizip gösterir."""
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(self.graph)  # Düğümleri yerleştir
        
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        
        plt.title(baslik)
        plt.show()



# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma

    # Grafiği çizme
    metro_graph = MetroGraph(metro)
    metro_graph.hat_grafigi_olustur("Kırmızı Hat")
    metro_graph.grafigi_goster("Kırmızı Hat Haritası")

    metro_graph.hat_grafigi_olustur("Mavi Hat")
    metro_graph.grafigi_goster("Mavi Hat Haritası")

    metro_graph.hat_grafigi_olustur("Turuncu Hat")
    metro_graph.grafigi_goster("Turuncu Hat Haritası")


    # Tüm metro ağını çizme
    metro_graph.tum_metro_grafigi_olustur()
    metro_graph.grafigi_goster("Tüm Metro Haritası")
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
