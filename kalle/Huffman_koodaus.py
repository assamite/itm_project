# Huffman-koodaus:

from heapq import heappush, heappop, heapify
from collections import defaultdict
 
def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


# Pieni koodaustesti itse keksityllä lukujonolla:

tieto1 = [1, 3, 5, 4, 4, 1, 7]
lista1 = defaultdict(int)      # Luodaan dynaaminen 'sanakirja', jonne halutaan tallentaa frekvenssit

for k in tieto1:
   lista1[k] += 1       # Kirjataan sanakirjaan eri numeroiden frekvenssit

huff1 = encode(lista1)      # Tuotetaan Huffman-koodit kullekin numerosymbolille


# Datan koodaus, kun meillä on Huffman-koodi symboleille:

koodi = ""
for merkki in tieto1:

  for pair in huff1:
  
    if pair[0] == merkki:
    
      koodi = koodi + pair[1]
      
# Koodin purku: (tässä ei tavitse tietää pakkauksesta muuta kuin se, mikä koodi millekin numerolle on annettu)

koodisana = ""
purettu = []

for merkki in koodi:
  
  koodisana = koodisana + merkki
  for pair in huff1:      # tässä oleva huff1 sisältää Huffman-koodisanat, joten decooderilla pitää olla se tiedossa
  
    if pair[1] == koodisana:
    
      purettu = purettu + [pair[0]]
      koodisana = ""