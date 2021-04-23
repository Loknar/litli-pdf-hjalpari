
# litli-pdf-hjalpari

![Litli PDF Hjálpari](/img/litli-pdf-hjalpari.png?raw=true "Litli PDF Hjálpari")

> "Ég er með þessar pdf skrár sem virkar ekki að leita að texta í, gætirðu litið á þær fyrir mig Litli PDF Hjálpari?"

Python skripta sem notar [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) til að textavæða pdf skrár sem eru án textaleitar.

# Forkröfur

## Python 3 og pip

[Python (3.6.8 eða nýrra) og pip pakkastjórnunartólið](https://www.python.org/downloads/) og python pakkar sem tilgreindir eru í `requirements.txt`:

```zsh
pip install -Ur requirements.txt
```

## Tesseract skipanalínutólið (CLI)

### Arch

```zsh
sudo pacman -Syu
sudo pacman -S tesseract tesseract-data-eng tesseract-data-isl
```

Ath: Við sækjum ensku og íslensku fyrir tesseract hér fyrir ofan, til að sjá fleiri tungumál í boði sem tilbúnir pakkar er hægt að keyra t.d. `pacman -Ss tesseract`.

### Debian/Ubuntu

```zsh
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-isl
```

Ath: Við sækjum ensku og íslensku fyrir tesseract hér fyrir ofan, til að sjá fleiri tungumál í boði sem tilbúnir pakkar er hægt að keyra t.d. `apt-cache search tesseract | grep language`.

### MacOS

[Homebrew?](https://formulae.brew.sh/formula/tesseract)

```zsh
brew update
brew install tesseract --with-all-languages
```

### Windows

[Finna, sækja og keyra EXE uppsetningarskrá?](https://medium.com/quantrium-tech/installing-and-using-tesseract-4-on-windows-10-4f7930313f82) Eflaust er líka hægt að smíða tesseract frá kóða .. hef ekki sett mig inn í hvernig það er gert. Veit ekki um pakkatól fyrir windows sem býður upp á að sækja og setja upp tesseract, endilega sendu mér línu kæri lesandi ef þú veist um eitthvað slíkt. Þarf líklega að [bæta tesseract í PATH](https://medium.com/@kevinmarkvi/how-to-add-executables-to-your-path-in-windows-5ffa4ce61a53) að uppsetningu lokinni.

Ath: Ef þú sækir og keyrir einhverja EXE uppsetningarskrá gæti þig langað að velja einhver auka tungumál til að hafa með í tesseract uppsetningunni.

Hægt er að sjá hvaða tungumál hafa verið sett upp fyrir tesseract með að keyra `tesseract --list-langs`.

# Notkun

Opna skipanalínu, vera í viðeigandi möppu og keyra:

```zsh
python litli_pdf_hjalpari.py -h
```

## Nota sem CLI tól, hvar sem er

Viljirðu frekar geta skrifað til dæmis `litli-pdf-hjalpari` hvar sem er í stað þess að þurfa að vera í réttri möppu og keyra `python litli-pdf-hjalpari.py` geturðu einfaldlega bætt viðeigandi symlink í einhverja af bin/PATH möppunum þínum, til dæmis:

### Linux/UNIX (bash)

```zsh
ln -s /path/to/litli-pdf-hjalpari/bin/litli-pdf-hjalpari ~/.local/bin/litli-pdf-hjalpari
```

Ath: Breyta `/path/to/` í slóð að repo möppunni `litli-pdf-hjalpari`.

### Windows (powershell)

```powershell
todo: skrifa bat skrá í stíl við bash skrána?
```

## Nokkur einföld skipanadæmi

```zsh
# bara skrá inn skrá út bing bang bæng
python litli_pdf_hjalpari.py -i "Downloads/scanned.pdf" -o "Documents/scanned_text_searchable.pdf"
# yfirskrifa output skrá sem er nú þegar til
python litli_pdf_hjalpari.py -i "Downloads/scanned.pdf" -o "Documents/scanned_text_searchable.pdf" -ow
# skrá þar sem síður snúa ekki rétt, snúa síðunum 90° réttsælis
python litli_pdf_hjalpari.py -i "Downloads/scanned.pdf" -rc -o "Documents/scanned_text_searchable.pdf"
# skönnuð skrá með tveimur síðum á hverri síðu, aðskilja í sér síður og snúa síðunum 90° rangsælis
python litli_pdf_hjalpari.py -i "Downloads/scanned.pdf" -cph -rcc -o "Documents/scanned_text_searchable.pdf"
```
