# If first time running these scripts, 
# you must: 1.create a venv. 2.activate venv. and 3.install requirements in bash:
# 1: python3 -m venv .venv
# 2: . ./venv/bin/activate
# 3: pip install -r requirements.txt
# PS: If you have run the script before, you might just have to do step 2(activate venv)

from PIL import Image, ImageEnhance, ImageFilter
import os

# Edit path and pathOut to your folders
# Add effects to tailor the images to your specific needs. Enjoy!

path = "/Users/torarnebirkeland/Downloads/Testfolder_bilder"  # mappe for originale bilder
pathOut = "/Users/torarnebirkeland/Downloads/Testfolder_bilder/Edited"  # mappe for redigerte bilder

# Sjekk om pathOut eksisterer, hvis ikke opprett den
if not os.path.exists(pathOut):
    os.makedirs(pathOut)

# Gå gjennom alle filer i path
for filename in os.listdir(path):
    try:
        # Åpne bildet
        img = Image.open(os.path.join(path, filename))

        # Rediger bildet
        # Først øker vi skarpheten
        edit = img.filter(ImageFilter.SHARPEN)

        # "Glow"-effekt (Mild blur + skarphet)
        glow = edit.filter(ImageFilter.GaussianBlur(radius=2))
        glow = glow.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=1))

        # Kombinerer det opprinnelige bildet med "glow"-effekten for å få en subtil effekt
        edit = Image.blend(edit, glow, alpha=0.2)  # Juster alpha-verdien for å kontrollere intensiteten

        # Uncomment the following line to convert the image to black and white
        # edit = edit.convert('L')

        # Øker kontrasten
        enhancer = ImageEnhance.Contrast(edit)
        edit = enhancer.enhance(1.5)

        # Lagre det redigerte bildet
        clean_name = os.path.splitext(filename)[0]
        edit.save(f'{pathOut}/{clean_name}_edited.jpg')

        print(f"{filename} ble redigert og lagret som {clean_name}_edited.jpg")

    except Exception as e:
        print(f"Feil ved behandling av {filename}: {str(e)}")
