@echo off
REM AI Content Studio - Tam Otomatik Kurulum (Windows)
REM Bu script tüm kurulum adımlarını otomatik olarak gerçekleştirir

echo ====================================================================
echo   AI Content Studio - Otomatik Kurulum
echo ====================================================================
echo.
echo Bu script asagidaki islemleri gerceklestirecek:
echo 1. Python versiyonunu kontrol edecek
echo 2. Sanal ortam olusturacak
echo 3. Bagimliliklari yukleyecek
echo 4. Yapay zeka modellerini indirecek (15-20 GB)
echo 5. Kurulumu dogrulayacak
echo.
echo NOT: Bu islem 30-60 dakika surebilir!
echo.
pause

REM Python kontrolü
echo.
echo [1/5] Python versiyonu kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.9+ yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo OK: Python bulundu

REM Sanal ortam oluşturma
echo.
echo [2/5] Sanal ortam olusturuluyor...
if exist "venv\" (
    echo Mevcut sanal ortam siliniyor...
    rmdir /s /q venv
)
python -m venv venv
if errorlevel 1 (
    echo HATA: Sanal ortam olusturulamadi!
    pause
    exit /b 1
)
echo OK: Sanal ortam olusturuldu

REM Sanal ortamı aktifleştir
call venv\Scripts\activate.bat

REM Pip güncelleme
echo.
echo [3/5] Pip guncelleniyor ve bagimliliklari yukleniyor...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo UYARI: Pip guncellenemedi, devam ediliyor...
)

REM Bağımlılıkları yükleme
echo.
echo Bagimliliklari yukleniyor (bu 10-20 dakika surebilir)...
pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: Bagimliliklari yuklenirken hata olustu!
    echo Lutfen internet baglantinizi kontrol edin.
    pause
    exit /b 1
)
echo OK: Bagimliliklari yuklendi

REM GPU kontrolü ve PyTorch kurulumu
echo.
echo GPU kontrolu yapiliyor...
python -c "import torch; print('GPU:', torch.cuda.is_available())" 2>nul
if errorlevel 1 (
    echo UYARI: PyTorch yuklenemedi, temel kurulum tamamlandi
) else (
    python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>nul
    if errorlevel 1 (
        echo.
        echo NVIDIA GPU bulundu mu? GPU destegi icin PyTorch CUDA yuklemek ister misiniz?
        echo Bu islem daha hizli islem yapmanizi saglar.
        echo.
        choice /C YN /M "PyTorch CUDA yukle (Y) veya CPU ile devam et (N)"
        if errorlevel 2 goto skip_cuda
        if errorlevel 1 (
            echo PyTorch CUDA yukleniyor...
            pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
            if errorlevel 1 (
                echo UYARI: PyTorch CUDA yuklenemedi, CPU ile devam ediliyor
            )
        )
    )
)
:skip_cuda

REM Model indirme
echo.
echo [4/5] Yapay zeka modelleri indiriliyor...
echo Bu islem 15-20 GB veri indirecek ve 20-40 dakika surebilir.
echo.
choice /C YN /M "Modelleri simdi indirmek istiyor musunuz"
if errorlevel 2 goto skip_models
if errorlevel 1 (
    echo.
    echo Modeller indiriliyor... (Bu uzun surebilir, lutfen bekleyin)
    python download_models.py
    if errorlevel 1 (
        echo UYARI: Modeller tamamen indirilemedi.
        echo Modelleri daha sonra "python download_models.py" ile indirebilirsiniz.
    ) else (
        echo OK: Modeller basariyla indirildi
    )
)
:skip_models

REM Kurulum doğrulama
echo.
echo [5/5] Kurulum dogrulanıyor...
python verify_installation.py
if errorlevel 1 (
    echo.
    echo UYARI: Bazi kontroller basarisiz oldu.
    echo Uygulamayi yine de calistirmayi deneyebilirsiniz.
) else (
    echo.
    echo OK: Kurulum basariyla tamamlandi!
)

REM Özet
echo.
echo ====================================================================
echo   KURULUM TAMAMLANDI!
echo ====================================================================
echo.
echo Uygulamayi baslatmak icin:
echo   1. start.bat dosyasina cift tiklayin
echo   veya
echo   2. "python src\main.py" komutunu calistirin
echo.
echo Yardim icin beniokumalisin.md dosyasini okuyun.
echo.
pause
