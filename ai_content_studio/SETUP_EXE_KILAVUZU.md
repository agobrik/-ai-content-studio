# 📦 AI Content Studio - Standalone EXE Kurulum Kılavuzu

## 🎯 Hedef
Bu uygulamayı **istediğiniz bilgisayara** kurulum yapmadan çalıştırabilir hale getirmek.

## 🚀 Hızlı Başlangıç (3 Dakika)

### Yöntem 1: Tek Dosya EXE (En Kolay) ⭐

```bash
# 1. EXE'yi oluştur
build_exe.bat

# 2. Dosyayı al
dist\AI_Content_Studio.exe

# 3. İstediğin PC'ye kopyala ve çalıştır!
```

**Avantajlar:**
- ✅ Tek dosya
- ✅ Kurulum yok
- ✅ Hemen çalışır
- ✅ USB'ye atıp götürebilirsin

**Dezavantajlar:**
- ⚠️ Dosya boyutu büyük (~500 MB)
- ⚠️ İlk açılış yavaş (PyInstaller unpacking)

---

## 📋 Detaylı Kurulum Yöntemleri

### Yöntem 2: Profesyonel Installer (Önerilen)

#### Adım 1: EXE Oluştur
```bash
build_exe.bat
```

#### Adım 2: Inno Setup Yükle
1. İndir: https://jrsoftware.org/isdl.php
2. Kur: Inno Setup 6.x

#### Adım 3: Installer Oluştur
1. `installer.iss` dosyasını Inno Setup ile aç
2. `Build > Compile` tıkla
3. Oluşan `AI_Content_Studio_Setup.exe` dosyasını al

#### Adım 4: Dağıt
- `AI_Content_Studio_Setup.exe` dosyasını paylaş
- Kullanıcı çift tıklayıp kurar
- Start menüsü + Masaüstü kısayolu otomatik

**Avantajlar:**
- ✅ Profesyonel görünüm
- ✅ Start menüsü entegrasyonu
- ✅ Kolay kaldırma
- ✅ Lisans gösterimi

---

### Yöntem 3: Portable ZIP

#### Adım 1: Portable Oluştur
```bash
# 1. EXE oluştur
build_exe.bat

# 2. Portable paket oluştur
create_portable.bat
```

#### Adım 2: ZIP'le
```bash
# portable klasörünü sıkıştır
Sağ tık > Sıkıştır > AI_Content_Studio_Portable.zip
```

#### Adım 3: Dağıt
- ZIP dosyasını paylaş
- Kullanıcı açar ve çalıştırır
- Kurulum gerektirmez

**Avantajlar:**
- ✅ Kurulum yok
- ✅ USB'den çalışır
- ✅ Sistem kirletmez
- ✅ Kolay taşınır

---

## 🛠️ Build Script Açıklamaları

### build_exe.bat
```batch
# Tek dosya EXE oluşturur
# Tüm bağımlılıkları içerir
# 5-10 dakika sürer
```

### build_installer.py
```python
# 3 tip installer scripti oluşturur:
# 1. PyInstaller spec
# 2. NSIS script
# 3. Inno Setup script
```

### create_portable.bat
```batch
# Portable klasör yapısı oluşturur
# Kurulum gerektirmez
# USB'ye atılabilir
```

---

## 📦 Dosya Boyutları

| Yöntem | Boyut | Açıklama |
|--------|-------|----------|
| Tek EXE | ~500 MB | Tüm bağımlılıklar dahil |
| Installer | ~500 MB | + kurulum arayüzü |
| Portable ZIP | ~500 MB | Sıkıştırılmış ~200 MB |

---

## 🔧 Gelişmiş Ayarlar

### EXE İkonunu Değiştir

1. `assets/icon.ico` dosyası oluştur (256x256 px)

2. `build_exe.bat` düzenle:
```batch
pyinstaller --icon=assets\icon.ico ^
    --name="AI_Content_Studio" ^
    ...
```

### Dosya Boyutunu Küçült

1. **UPX kullan:**
```batch
pyinstaller --upx-dir=upx ^
    --name="AI_Content_Studio" ^
    ...
```

2. **İsteğe bağlı kütüphaneleri çıkar:**
```batch
# requirements.txt'den gereksiz paketleri kaldır
# Örn: matplotlib, scipy (3D için gerekmiyorsa)
```

3. **One-folder yerine:**
```batch
# --onefile yerine --onedir kullan
# Daha hızlı başlatma
# Ama birden fazla dosya
```

---

## 🐛 Sorun Giderme

### Problem: "Missing module" hatası
**Çözüm:**
```batch
# build_exe.bat içine ekle:
--hidden-import eksik_modul_adi
```

### Problem: EXE çalışmıyor
**Çözüm:**
```batch
# --windowed yerine --console kullan
# Hata mesajlarını görebilirsiniz
```

### Problem: Dosya çok büyük
**Çözüm:**
```batch
# PyTorch CUDA'sız kur:
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Problem: Yavaş başlatma
**Çözüm:**
```batch
# --onedir kullan (--onefile yerine)
# Klasör olur ama daha hızlı
```

---

## 📋 Checklist: EXE Dağıtımdan Önce

- [ ] `build_exe.bat` çalıştırıldı
- [ ] `dist\AI_Content_Studio.exe` oluştu
- [ ] EXE test edildi (kendi PC'de)
- [ ] Başka bir PC'de test edildi
- [ ] İnternet bağlantısı ile test edildi
- [ ] İnternet olmadan test edildi (2. çalıştırma)
- [ ] README/Kılavuz hazır
- [ ] Lisans dahil edildi

---

## 🚀 Hızlı Komutlar

### Tek EXE Oluştur
```bash
build_exe.bat
```

### Tam Paket Oluştur
```bash
# 1. EXE
build_exe.bat

# 2. Installer
python build_installer.py

# 3. Portable
create_portable.bat
```

### Test Et
```bash
# Test EXE
dist\AI_Content_Studio.exe

# Test Portable
portable\AI_Content_Studio.bat
```

---

## 📊 Dağıtım Karşılaştırması

| Özellik | Tek EXE | Installer | Portable |
|---------|---------|-----------|----------|
| Kurulum | Yok | Var | Yok |
| Dosya sayısı | 1 | 1 | Çok |
| Başlatma hızı | Yavaş | Hızlı | Orta |
| Kaldırma | Manuel | Otomatik | Manuel |
| Profesyonellik | Orta | Yüksek | Düşük |
| Taşınabilirlik | ✅ | ❌ | ✅ |

---

## 💡 Öneriler

### Kişisel Kullanım
→ **Tek EXE** (build_exe.bat)

### Şirket İçi Dağıtım
→ **Installer** (Inno Setup)

### USB/Portable
→ **Portable ZIP** (create_portable.bat)

### Geniş Kitle
→ **Installer + Portable** (ikisini de sun)

---

## 🎯 Final Checklist

Dağıtmadan önce:

```bash
# 1. Clean build
rmdir /s /q build dist
build_exe.bat

# 2. Test
dist\AI_Content_Studio.exe

# 3. README ekle
copy beniokumalisin.md dist\

# 4. Lisans ekle
copy LICENSE dist\

# 5. ZIP oluştur (opsiyonel)
# dist klasörünü sıkıştır

# 6. Dağıt! 🚀
```

---

## 📞 Destek

### Hata Loglama
EXE hata verirse:
1. `--console` modunda derle
2. Hata mesajlarını kaydet
3. `build_exe.bat` içinde `--windowed` yerine `--console` kullan

### Debug Modu
```batch
# Debug için:
pyinstaller --debug all ^
    --name="AI_Content_Studio_Debug" ^
    src\main.py
```

---

## 🎉 Başarılar!

Artık uygulamanızı **istediğiniz PC'ye** kurabilirsiniz!

```bash
# Hemen başla:
build_exe.bat
```

---

**Son Güncelleme**: 2025-10-16
**Versiyon**: 1.0.0
