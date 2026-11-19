from PIL import Image
import re
import pytesseract
resim_yolu = "rapor.jpeg"

resim = Image.open(resim_yolu)

print("Görüntü boyutu:", resim.size)
gri_resim = resim.convert("L")
gri_resim.save("gri_rapor.png")
genislik, yukseklik = gri_resim.size

sol = int(genislik * 0.38)
sag = int(genislik * 0.75)

fis = gri_resim.crop((sol, 0, sag, yukseklik))
fis = fis.resize((fis.width * 3, fis.height * 3), Image.Resampling.LANCZOS)
fis.save("fis_kirpildi.png")
print("Gri görüntü kaydedildi.")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

metin = pytesseract.image_to_string(fis, lang="tur+eng")
print("OCR sonucu:")
print(metin)
z_eslesme = re.search(r"[Z2]\s*RAPORU\s*(\d{3,})", metin, re.IGNORECASE)

if z_eslesme:
    print("Z numarası:", z_eslesme.group(1))
else:
    print("Z numarası bulunamadı.")
    
tarih_eslesme = re.search(r"(\d{2}/\d{2}/\d{4})", metin)

if tarih_eslesme:
    print("Tarih:", tarih_eslesme.group(1))
else:
    print("Tarih bulunamadı.")


kart_eslesme = re.search(r"Banka/Kredi Kartı\s*\*?\s*([\d.]+,\d{2})", metin, re.IGNORECASE)

if kart_eslesme:
    print("Kart tutarı:", kart_eslesme.group(1))
else:
    print("Kart tutarı bulunamadı.")

toplam_eslesme = re.search(
    r"TOPLAM SATI[SŞ]\s*\*?\s*([\d.]+,\d{2})",
    metin,
    re.IGNORECASE
)

if toplam_eslesme:
    print("Toplam satış:", toplam_eslesme.group(1))
else:
    print("Toplam satış bulunamadı.")



if kart_eslesme and toplam_eslesme:
    toplam_satis = float(
        toplam_eslesme.group(1).replace(".", "").replace(",", ".")
    )
    kart_tutari = float(
        kart_eslesme.group(1).replace(".", "").replace(",", ".")
    )

    nakit_tutari = round(toplam_satis - kart_tutari, 2)
    print("Nakit tutarı:", nakit_tutari)
else:
    print("Nakit hesaplanamadı.")

kdv_eslesmeleri = re.findall(
   r"^KDV[^\d\r\n]*(\d{1,2})[^\d\r\n]*([\d.]+,\d{2})",
    metin,
    re.IGNORECASE | re.MULTILINE
)

kdv_eslesmeleri = [
    ("0" if oran == "9" and tutar == "0,00" else oran, tutar)
    for oran, tutar in kdv_eslesmeleri
]

print("KDV oranı ve tutarları:", kdv_eslesmeleri)

kdv_satislari = re.findall(
    r"^\s*TOPLAM\s*%?([01])\D*([\d.]+,\d{2})",
    metin,
    re.IGNORECASE | re.MULTILINE
)
print("KDV oranına göre satışlar:", kdv_satislari)



