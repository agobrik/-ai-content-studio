# 🎯 Text-to-3D Prompt Rehberi

## ⚠️ ÖNEMLİ: Basit Tutun!

Text-to-3D **tek obje** üretimi için optimize edilmiştir. Karmaşık sahneler ÇALIŞMAZ!

### ✅ İYİ Promptlar (Bunları kullanın!)

```
coffee mug
wooden chair
ceramic vase
glass bottle
metal trophy
blue teapot
red apple
soccer ball
table lamp
flower pot
simple crown
golden coin
ceramic bowl
wooden spoon
metal key
```

### ❌ KÖTÜ Promptlar (Bunları kullanmayın!)

```
❌ kitchen scene with coffee mug and spoon on table
   → Çok karmaşık, çok obje

❌ a person holding a coffee mug in a cafe
   → İnsan içeriyor, sahne var

❌ beautiful landscape with mountains and lake
   → Manzara, 3D obje değil

❌ abstract art with multiple geometric shapes
   → Çok şekil, soyut

❌ detailed city skyline with buildings
   → Çok karmaşık, çok bina
```

---

## 📋 Prompt Yazma Kuralları

### Kural 1: TEK OBJE
```
✅ "coffee mug"
❌ "coffee mug with spoon and plate"
```

### Kural 2: BASİT TANIMLA
```
✅ "wooden chair"
❌ "antique victorian chair with intricate carvings and golden details"
```

### Kural 3: MALZEME BELİRT (Opsiyonel)
```
✅ "ceramic vase"
✅ "metal trophy"
✅ "glass bottle"
✅ "wooden table"
```

### Kural 4: RENK EKLEYEBİLİRSİNİZ (Opsiyonel)
```
✅ "blue coffee mug"
✅ "red apple"
✅ "golden trophy"
```

### Kural 5: TEMEL ŞEKİL BELİRTİN (Opsiyonel)
```
✅ "cylindrical vase"
✅ "spherical lamp"
✅ "cubic container"
```

---

## 🎨 Kategori Bazlı Örnekler

### Mutfak Eşyaları
```
coffee mug
teapot
ceramic bowl
wooden spoon
glass cup
plate
fork
knife
cutting board
salt shaker
```

### Mobilya
```
wooden chair
table lamp
desk
stool
bookshelf
cabinet
wardrobe
bed frame
sofa
ottoman
```

### Dekorasyon
```
ceramic vase
flower pot
picture frame
candle holder
statue
sculpture
ornament
wall clock
mirror frame
decorative bowl
```

### Spor Eşyaları
```
soccer ball
basketball
tennis ball
baseball bat
golf club
trophy
medal
dumbbell
yoga mat
water bottle
```

### Ofis Malzemeleri
```
pen
pencil holder
stapler
desk organizer
lamp
notebook
ruler
scissors
tape dispenser
calculator
```

### Mücevherat & Aksesuarlar
```
ring
bracelet
necklace
earring
crown
tiara
brooch
pendant
watch
cufflinks
```

### Teknoloji (Basit)
```
computer mouse
keyboard
USB drive
headphones
speaker
microphone
camera
phone case
laptop stand
cable organizer
```

### Doğa Objeleri
```
red apple
orange
banana
pear
pumpkin
mushroom
seashell
stone
wood log
pinecone
```

### Oyuncaklar
```
toy car
building block
teddy bear
rubber duck
spinning top
yo-yo
ball
puzzle piece
toy boat
toy airplane
```

### Aletler
```
hammer
screwdriver
wrench
pliers
saw
drill
measuring tape
level
chisel
mallet
```

---

## 💡 Gelişmiş İpuçları

### 1. Stil Ekleme (Opsiyonel)

Sistem otomatik olarak "product photography" ve "studio lighting" ekliyor, ama siz de stil belirtebilirsiniz:

```
coffee mug, modern style
wooden chair, minimalist design
ceramic vase, traditional style
metal trophy, futuristic design
```

### 2. Görünüm Açısı (Otomatik)

Sistem otomatik olarak "isometric view" ve "centered" ekliyor. Elle eklemenize gerek yok.

### 3. Materyal Vurgusu

Materyal belirtmek genellikle daha iyi sonuç verir:

```
✅ "ceramic coffee mug"
✅ "wooden chair"
✅ "metal trophy"
✅ "glass vase"
```

### 4. Basit Geometri

Basit geometrik şekiller en iyi sonucu verir:

```
✅ "cylindrical vase"
✅ "spherical lamp"
✅ "rectangular box"
✅ "conical hat"
```

### 5. Renk Kullanımı

Tek, belirgin renkler kullanın:

```
✅ "blue mug"
✅ "red apple"
✅ "golden trophy"
✅ "white vase"

❌ "rainbow colored multi-pattern mug"
```

---

## 🔧 Troubleshooting: Kötü Sonuç Aldıysanız

### Problem: Alakasız obje üretildi

**Çözüm**:
1. Prompt'u **daha basit** yapın
2. **Tek kelime** deneyin: "mug" yerine "coffee mug"
3. Materyal ekleyin: "mug" → "ceramic mug"
4. Modeli yeniden başlatın (uygulamayı kapat/aç)

**Örnek**:
```
Kötü sonuç: "a beautiful decorative coffee mug with geometric patterns"
İyileştir: "coffee mug"
Daha iyi: "blue coffee mug"
En iyi: "ceramic coffee mug"
```

### Problem: Çok karmaşık/bozuk çıktı

**Çözüm**:
1. **Tek obje** olduğundan emin olun
2. **Basit geometri** seçin
3. **Detaylı açıklamalar** çıkarın
4. **Extrusion depth** azaltın (0.3-0.4)

### Problem: Renksiz/gri çıktı

**Çözüm**:
1. Prompt'a **renk** ekleyin
2. 2D görseli kontrol edin (temp_3d klasörü)
3. Eğer 2D görsel kötüyse, prompt'u değiştirin

### Problem: Çok düz/ince 3D

**Çözüm**:
1. **Extrusion depth** artırın (0.7-1.0)
2. Daha yüksek kontrastlı renkler kullanın
3. Prompt'a "3D style" ekleyin

---

## 🎯 Hızlı Başlangıç

### Adım 1: Basit başlayın
```
Prompt: coffee mug
→ Generate
→ Sonucu görün
```

### Adım 2: İyileştirin
```
Prompt: blue coffee mug
→ Generate
→ Daha iyi!
```

### Adım 3: Malzeme ekleyin
```
Prompt: ceramic blue coffee mug
→ Generate
→ En iyi!
```

---

## 📊 Beklenti Yönetimi

### Bu Sistem NE YAPAB İLİR ✅

- ✅ Basit, tek objeler üretebilir
- ✅ Product-style 3D modeller oluşturur
- ✅ GLB/OBJ/STL formatında export
- ✅ Renkli, textureli meshler
- ✅ 30-60 saniyede sonuç

### Bu Sistem NE YAPAMAZ ❌

- ❌ Karmaşık sahneler
- ❌ Çoklu objeler
- ❌ İnsan/yüz modelleme
- ❌ Animasyon
- ❌ Gerçekçi 3D tarama kalitesi
- ❌ Detaylı anatomik yapılar

---

## 🚀 En İyi 20 Prompt (Test Edildi)

### Mutfak (5)
1. `coffee mug`
2. `ceramic teapot`
3. `glass bottle`
4. `wooden bowl`
5. `metal spoon`

### Mobilya (5)
6. `wooden chair`
7. `table lamp`
8. `simple desk`
9. `stool`
10. `picture frame`

### Dekorasyon (5)
11. `ceramic vase`
12. `flower pot`
13. `candle holder`
14. `decorative bowl`
15. `small statue`

### Diğer (5)
16. `soccer ball`
17. `trophy`
18. `red apple`
19. `toy car`
20. `golden crown`

---

## 💡 Pro İpuçları

1. **İlk denemede mükemmel beklemeyin** - 2-3 deneme yapın
2. **2D görseli kontrol edin** - `output/temp_3d` klasöründe
3. **Extrusion depth ile oynayın** - 0.3 ile 1.0 arası deneyin
4. **Stable Diffusion öğrenme sürecinde** - Her prompt farklı sonuç verebilir
5. **Basit = Daha iyi** - Daha az detay = Daha iyi 3D

---

## 📞 Yardım

### Model yeniden indirme
Eğer sürekli kötü sonuçlar alıyorsanız:

```bash
# output/models klasörünü silin
# Uygulama modeli tekrar indirecek
```

### 2D görseli kontrol
```bash
# Konum: output/temp_3d/
# 2D görsel burada kaydediliyor
# Eğer 2D kötüyse, 3D de kötü olur
```

---

**Son Güncelleme**: 2025-10-16
**Model**: Stable Diffusion v1.5
**Optimum Prompt Uzunluğu**: 2-5 kelime

## 🎯 Özet: 3 Altın Kural

1. **TEK OBJE** - Sadece bir şey isteyin
2. **BASİT** - Az kelime kullanın
3. **NET** - "coffee mug" gibi açık tanımlayın

**Hemen deneyin**: `coffee mug` 🚀
