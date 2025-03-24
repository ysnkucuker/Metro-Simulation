# Metro-Simulation
Metro-Simulation is a Python-based metro system simulation project (Global AI Hub - Introduction to AI)

This project contains a metro network simulation and is written in Python. It allows users to find the fastest and least transfer routes through features such as metro stations, connections between lines, and routes. Additionally, the graph for each line and a combined map of the entire metro network are visually presented.

## Project Overview

In this project, users can find the fastest and least transfer route between two metro stations. The relationships between metro stations, lines, and connections have been analyzed using BFS (Breadth-First Search) and A* algorithms. Additionally, the metro network's graphical representation is created using the `networkx` and `matplotlib` libraries.

## Features

- **Metro Network Modeling:** Stations, lines, and connections can be created.
- **Least Transfer Route:** Using the BFS algorithm, users can find the route with the least transfers between two stations.
- **Fastest Route:** Using the A* algorithm, users can learn the fastest route and total time between two stations.
- **Metro Line Visualization:** Graphs for each metro line can be created and visually presented.
- **Complete Metro Network:** The complete metro system's visual map can be shown as a combined map.

## BFS
- **1.** Checking the Start and Destination Station
  - if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
    return None
- **2.** Acquisition of Start and Target Stations
  - baslangic = self.istasyonlar[baslangic_id]
    hedef = self.istasyonlar[hedef_id]
- **3.** Initializing the Queue
  - kuyruk = deque([(baslangic, [baslangic])])  # (mevcut istasyon, şu ana kadar olan rota)
- **4.** Set of visited nodes
  - ziyaret_edildi = set()
- **5.** BFS Loops
  - while kuyruk:
    mevcut_istasyon, yol = kuyruk.popleft()
- **6.** If we reach the station
  - if mevcut_istasyon == hedef:
    return yol  # Hedefe ulaştık, en kısa aktarma rotasını döndür
- **7.** Going to neighboor nodes
  - for komsu, _ in mevcut_istasyon.komsular:
    if komsu not in ziyaret_edildi:
        ziyaret_edildi.add(komsu)
        kuyruk.append((komsu, yol + [komsu]))  # Yeni rota oluştur ve kuyruğa ekle

## A*
- **1.** Starting and destination
 -   if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
        return None
- **2.** Queue
  -  pq = [(0, id(baslangic), baslangic, [baslangic])]  # (toplam süre, öncelik, istasyon, rota)
- **3.** The loop continues as long as the queue is not empty. In each loop, the most suitable station (lowest time) will be taken from the queue.
  -  while pq:
     if mevcut_istasyon == hedef:
            return yol, toplam_sure
- **4.** Passes through neighbors of existing station
  -         for komsu, sure in mevcut_istasyon.komsular:
            yeni_sure = toplam_sure + sure
            heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yol + [komsu]))


