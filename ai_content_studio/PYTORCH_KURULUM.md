# PyTorch Kurulum Kılavuzu - DLL Hatası Çözümü

## 🔴 Problem: DLL Başlatma Hatası

Eğer şu hatayı alıyorsanız:
```
[WinError 1114] Devingen bağlantı kitaplığını (DLL) başlatma işlemi başarısız.
Error loading "C:\...\torch\lib\c10.dll" or one of its dependencies.
```

## ✅ Çözüm: PyTorch'u Doğru Şekilde Kurun

### Yöntem 1: Otomatik Kurulum (Önerilen)

```bash
# 1. Sanal ortamı aktifleştirin
venv\Scripts\activate.bat

# 2. Eski PyTorch'u kaldırın
pip uninstall torch torchvision torchaudio -y

# 3. Doğru PyTorch'u yükleyin (CUDA 11.8 ile)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Yöntem 2: CPU-Only Versiyon (GPU Yok)

GPU'nuz yoksa veya CPU kullanmak istiyorsanız:

```bash
# 1. Sanal ortamı aktifleştirin
venv\Scripts\activate.bat

# 2. Eski PyTorch'u kaldırın
pip uninstall torch torchvision torchaudio -y

# 3. CPU-only PyTorch yükleyin
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 🧪 Kurulumu Test Edin

```bash
# PyTorch'un doğru yüklendiğini test edin
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

Beklenen çıktı:
```
PyTorch: 2.7.1+cu118
CUDA: True
```

## 📊 PyTorch Versiyonları

| Versiyon | URL | Açıklama |
|----------|-----|----------|
| CUDA 11.8 | `https://download.pytorch.org/whl/cu118` | NVIDIA GPU ile (önerilen) |
| CUDA 12.1 | `https://download.pytorch.org/whl/cu121` | Yeni NVIDIA GPU'lar |
| CPU Only | `https://download.pytorch.org/whl/cpu` | GPU yok veya gerekli değil |

## 🔧 Sorun Giderme

### Problem: CUDA bulunamadı

**Belirtiler:**
```
CUDA: False
```

**Çözüm:**
- NVIDIA GPU'nuz var mı kontrol edin
- GPU varsa NVIDIA sürücülerini güncelleyin: https://www.nvidia.com/drivers
- Yoksa CPU-only versiyon kullanın

### Problem: Hala DLL hatası alıyorum

**Çözüm 1: Microsoft Visual C++ Yükleyin**
1. İndirin: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Kurun ve bilgisayarı yeniden başlatın
3. PyTorch'u tekrar yükleyin

**Çözüm 2: PyTorch'u Tamamen Sıfırlayın**
```bash
# Sanal ortamı silin ve yeniden oluşturun
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate.bat

# PyTorch'u yeniden yükleyin
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Problem: İndirme çok yavaş

**Çözüm:**
```bash
# Farklı mirror kullanın
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 --timeout 1000
```

## 📝 Notlar

- **Dosya Boyutu**: PyTorch CUDA versiyonu ~2.8 GB indirir
- **CPU Versiyonu**: Daha küçük (~200 MB) ama daha yavaş
- **GPU Avantajı**: Görsel üretimi 10-50x daha hızlı
- **İlk Kullanım**: Diffusion modelleri ilk çalıştırmada indirilir (~4-6 GB)

## ✅ Başarılı Kurulum Kontrol Listesi

- [ ] PyTorch başarıyla import ediliyor
- [ ] CUDA durumu gösteriliyor (True veya False)
- [ ] DLL hatası yok
- [ ] Uygulama başlatılıyor
- [ ] Görsel üretme çalışıyor

## 🚀 Sonraki Adım

Kurulum tamamlandıysa:

```bash
# Uygulamayı başlatın
start.bat
```

veya

```bash
python src\main.py
```

---

**Son Güncelleme**: 2025-10-16
**Çözüm**: PyTorch 2.7.1+cu118 ile test edildi ✅
