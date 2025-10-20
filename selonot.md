# AI Content Studio - Başka Bilgisayarda Kurulum Rehberi

Bu rehber, projenizi GitHub'dan başka bir bilgisayara indirip çalıştırmak için gereken tüm adımları içerir.

## Sistem Gereksinimleri

- **Python 3.11** (Önemli: 3.11 versiyonu olmalı)
- **Git**
- **CUDA destekli NVIDIA GPU** (3D model oluşturma için önerilir)
- **En az 8GB RAM** (16GB önerilir)
- **En az 20GB boş disk alanı**

---

## Adım 1: Gerekli Yazılımları Yükleyin

### Python 3.11 Kurulumu

1. https://www.python.org/downloads/ adresine gidin
2. Python 3.11.x sürümünü indirin
3. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
4. Kurulumu tamamlayın

**Kontrol:**
```bash
python --version
```
veya
```bash
py -3.11 --version
```

### Git Kurulumu

1. https://git-scm.com/downloads adresine gidin
2. İşletim sisteminize uygun versiyonu indirin
3. Kurulumu varsayılan ayarlarla tamamlayın

**Kontrol:**
```bash
git --version
```

---

## Adım 2: Projeyi GitHub'dan İndirin

Terminali açın (CMD, PowerShell veya Git Bash) ve şu komutları çalıştırın:

```bash
cd C:\Projects
git clone https://github.com/agobrik/-ai-content-studio.git
cd -ai-content-studio
```

---

## Adım 3: Virtual Environment Oluşturun

```bash
cd ai_content_studio
python -m venv venv
```

veya Python 3.11'i özel olarak belirtmek için:

```bash
py -3.11 -m venv venv
```

---

## Adım 4: Virtual Environment'ı Aktifleştirin

### Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

### Windows (CMD):
```cmd
.\venv\Scripts\activate.bat
```

### Linux/Mac:
```bash
source venv/bin/activate
```

**Not:** Virtual environment aktifken terminalinizde `(venv)` yazısı görünür.

---

## Adım 5: PyTorch'u Yükleyin (CUDA Destekli)

PyTorch'u CUDA 12.1 desteğiyle yükleyin:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**PyTorch Kurulumunu Test Edin:**
```bash
python test_pytorch.py
```

Çıktıda şunları görmelisiniz:
- PyTorch version
- CUDA available: True
- CUDA version
- GPU adı

---

## Adım 6: Diğer Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

Bu komut şunları yükleyecek:
- diffusers (Stable Diffusion için)
- transformers (AI modelleri için)
- accelerate (GPU hızlandırma)
- PyQt6 (GUI için)
- pyttsx3 (Text-to-Speech)
- Pillow (Görüntü işleme)
- safetensors
- ve diğer gerekli kütüphaneler

---

## Adım 7: 3D Model Kütüphanelerini Kurun

### Hunyuan3D-2 Kurulumu

```bash
cd ..
git clone https://github.com/Tencent/Hunyuan3D-2.git
cd Hunyuan3D-2
pip install -r requirements.txt
pip install -e .
cd ../ai_content_studio
```

### Stable-Fast-3D Kurulumu

```bash
cd ..
git clone https://github.com/Stability-AI/stable-fast-3d.git
cd stable-fast-3d
pip install -r requirements.txt
pip install -e .
cd ../ai_content_studio
```

---

## Adım 8: AI Modellerini İndirin

Modeller ilk çalıştırmada otomatik olarak indirilecektir, ancak manuel olarak indirmek isterseniz:

```bash
python download_models.py
```

**İndirilecek Modeller:**
- Stable Diffusion v1.5 (görüntü oluşturma)
- Hunyuan3D-2 model dosyaları (3D model oluşturma)
- Diğer gerekli model dosyaları

**Not:** Model dosyaları çok büyüktür (10-20GB+), indirme uzun sürebilir.

---

## Adım 9: Kurulumu Doğrulayın

Tüm bileşenlerin düzgün çalıştığını kontrol edin:

```bash
python verify_installation.py
```

Her test için ✓ işareti görmelisiniz.

---

## Adım 10: Uygulamayı Başlatın

### Windows:
```bash
start.bat
```

veya

```bash
python src/main.py
```

### Linux/Mac:
```bash
./start.sh
```

veya

```bash
python src/main.py
```

---

## Proje Yapısı

```
-ai-content-studio/
├── ai_content_studio/          # Ana proje klasörü
│   ├── src/                    # Kaynak kodlar
│   │   ├── core/               # Ana işlevsellik
│   │   │   ├── image_generator.py      # Görüntü oluşturma
│   │   │   ├── tts_generator.py        # Text-to-Speech
│   │   │   └── model_3d_generator.py   # 3D model oluşturma
│   │   ├── gui/                # Grafik arayüz
│   │   │   ├── main_window.py
│   │   │   └── tabs/           # Sekmeler
│   │   └── main.py             # Ana program
│   ├── config/                 # Yapılandırma dosyaları
│   ├── models/                 # İndirilen AI modelleri
│   ├── output/                 # Oluşturulan dosyalar
│   ├── tests/                  # Test dosyaları
│   ├── requirements.txt        # Python paketleri
│   ├── start.bat              # Windows başlatıcı
│   └── start.sh               # Linux/Mac başlatıcı
├── Hunyuan3D-2/               # 3D model kütüphanesi
├── stable-fast-3d/            # 3D model kütüphanesi
└── .gitignore                 # Git göz ardı listesi
```

---

## Kullanım

### 1. Görüntü Oluşturma
- "Image Generation" sekmesine gidin
- Prompt girin (örn: "a beautiful sunset over mountains")
- "Generate" butonuna tıklayın
- Oluşan görüntü gösterilecek ve kaydedilecektir

### 2. Text-to-Speech
- "Text-to-Speech" sekmesine gidin
- Metninizi yazın
- Ses ayarlarını yapın
- "Generate Speech" butonuna tıklayın

### 3. 3D Model Oluşturma
- "3D Model Generation" sekmesine gidin
- Text-to-3D veya Image-to-3D seçin
- Prompt girin veya görüntü yükleyin
- "Generate 3D Model" butonuna tıklayın
- OBJ, GLB veya GLTF formatında model oluşturulur

---

## Sorun Giderme

### Python 3.11 Bulunamıyor
```bash
# Python versiyonlarını listeleyin
py --list

# Python 3.11'i kullanın
py -3.11 -m venv venv
```

### CUDA Bulunamıyor
1. NVIDIA GPU sürücülerinizi güncelleyin
2. CUDA Toolkit'i yükleyin: https://developer.nvidia.com/cuda-downloads
3. PyTorch'u yeniden yükleyin

### ModuleNotFoundError
```bash
# Virtual environment aktif olduğundan emin olun
# Sonra paketleri yeniden yükleyin
pip install -r requirements.txt
```

### Modeller İndirilemiyor
- İnternet bağlantınızı kontrol edin
- Hugging Face'e erişiminiz olduğundan emin olun
- Gerekirse VPN kullanın

### GPU Bellek Hatası
- Daha küçük batch size kullanın
- Görüntü çözünürlüğünü azaltın
- Diğer GPU kullanan programları kapatın

---

## Git Komutları

### Değişiklikleri GitHub'dan Çekin
```bash
git pull
```

### Yaptığınız Değişiklikleri Yükleyin
```bash
git add .
git commit -m "Değişiklik açıklaması"
git push
```

### Değişiklikleri Kontrol Edin
```bash
git status
git diff
```

### Branch Oluşturun
```bash
git checkout -b yeni-ozellik
```

---

## Önemli Notlar

1. **Virtual environment her zaman aktif olmalı** - Her terminal açtığınızda aktifleştirin
2. **Model dosyaları git'e yüklenmez** - Her bilgisayarda ayrı indirilir
3. **CUDA gereklidir** - 3D özellikler için NVIDIA GPU şart
4. **İlk çalıştırma yavaş olabilir** - Modeller indiriliyor
5. **Disk alanına dikkat** - Modeller çok yer kaplar

---

## Ek Kaynaklar

- **Proje GitHub:** https://github.com/agobrik/-ai-content-studio
- **PyTorch Dokümantasyonu:** https://pytorch.org/docs/
- **Hunyuan3D-2:** https://github.com/Tencent/Hunyuan3D-2
- **Stable Diffusion:** https://huggingface.co/runwayml/stable-diffusion-v1-5

---

## Yardım ve Destek

Sorun yaşarsanız:

1. `verify_installation.py` çalıştırın
2. Test dosyalarını çalıştırın (`tests/` klasöründe)
3. Hata mesajlarını kontrol edin
4. GitHub Issues'da sorun bildirin

---

**Başarılar!** 🚀
