
# litli-pdf-hjalpari

![Litli PDF Hjálpari](/pic-litli-pdf-hjalpari.png?raw=true "Litli PDF Hjálpari")

> "Ég er með þessar pdf skrár sem virkar ekki að leita að texta í, gætirðu litið á þær fyrir mig Litli PDF Hjálpari?"

Python skripta sem notar [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) til að textavæða pdf skrár sem eru án textaleitar.

# Forkröfur

## Python 3 og pip

[Python (3.6.8 eða nýrra) og pip pakkastjórnunartólið](https://www.python.org/downloads/) og python pakkar sem tilgreindir eru í `requirements.txt`:

```bash
pip install -Ur requirements.txt
```

## Tesseract skipanalínutólið (CLI)

### Arch

```bash
sudo pacman -Syu
sudo pacman -S tesseract tesseract-data-eng tesseract-data-isl
```

Ath: Við sækjum ensku og íslensku fyrir tesseract hér fyrir ofan, til að sjá fleiri tungumál í boði sem tilbúnir pakkar er hægt að keyra t.d. `pacman -Ss tesseract`.

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-isl
```

Ath: Við sækjum ensku og íslensku fyrir tesseract hér fyrir ofan, til að sjá fleiri tungumál í boði sem tilbúnir pakkar er hægt að keyra t.d. `apt-cache search tesseract | grep language`.

### MacOS

[Homebrew?](https://formulae.brew.sh/formula/tesseract)

```bash
brew update
brew install tesseract --with-all-languages
```

### Windows

[Finna, sækja og keyra EXE uppsetningarskrá?](https://medium.com/quantrium-tech/installing-and-using-tesseract-4-on-windows-10-4f7930313f82) Eflaust er líka hægt að smíða tesseract frá kóða .. hef ekki sett mig inn í hvernig það er gert. Veit ekki um pakkatól fyrir windows sem býður upp á að sækja og setja upp tesseract, endilega sendu mér línu kæri lesandi ef þú veist um eitthvað slíkt. Þarf líklega að [bæta tesseract í PATH](https://medium.com/@kevinmarkvi/how-to-add-executables-to-your-path-in-windows-5ffa4ce61a53) að uppsetningu lokinni.

Ath: Ef þú sækir og keyrir einhverja EXE uppsetningarskrá gæti þig langað að velja einhver auka tungumál til að hafa með í tesseract uppsetningunni.

Hægt er að sjá hvaða tungumál hafa verið sett upp fyrir tesseract með að keyra `tesseract --list-langs`.

# Notkun

Opna skipanalínu, vera í viðeigandi möppu og keyra:

```bash
python litli-pdf-hjalpari.py -h
```

```bash
usage: litli-pdf-hjalpari [-h] -i INPUT_FILE -o OUTPUT_FILE [-ow] [-del] [-lang LANGUAGE] [-cph]
                          [-cphr] [-rc] [-rcc] [-flip] [-ln LOGGER_NAME] [-ldir LOG_DIRECTORY]
                          [-r ROLE]

Litli PDF Hjálpari

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input PDF file.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output PDF file.
  -ow, --overwrite      Overwrite output file if exists.
  -del, --delete-page-files
                        Delete individual page files which are generated when textifying PDF files.
  -lang LANGUAGE, --language LANGUAGE
                        Language code for Tesseract to use.
  -cph, --cut-pages-horizontally
                        Separate each page horizontally into two pages, top half first.
  -cphr, --cut-pages-horizontally-reverse
                        Separate each page horizontally into two pages, bottom half first.
  -rc, --rotate-clockwise
                        Rotate each page clockwise.
  -rcc, --rotate-counter-clockwise
                        Rotate each page counterclockwise.
  -flip, --rotate-flip  Rotate each page 180 degrees.
  -ln LOGGER_NAME, --logger-name LOGGER_NAME
                        Define logger name (Default: "hjalpari").
  -ldir LOG_DIRECTORY, --log-directory LOG_DIRECTORY
                        Directory to write logs in. Default: "./logs/".
  -r ROLE, --role ROLE  Define runner role. (Default: "cli")
                        Available options: "cli", "api", "cron", "hook".
```

## Nota sem CLI tól, hvar sem er

Viljirðu frekar geta skrifað til dæmis `litli-pdf-hjalpari` hvar sem er í stað þess að þurfa að vera í réttri möppu og keyra `python litli-pdf-hjalpari.py` geturðu einfaldlega bætt viðeigandi symlink í einhverja af bin/PATH möppunum þínum, til dæmis:

### Linux/UNIX (bash)

```bash
ln -s /path/to/litli-pdf-hjalpari/bin/litli-pdf-hjalpari ~/.local/bin/litli-pdf-hjalpari
```

Ath: Breyta `/path/to/` í slóð að repo möppunni `litli-pdf-hjalpari`.

### Windows (powershell)

```powershell
todo: skrifa bat skrá í stíl við bash skrána?
```

## Nokkur einföld skipanadæmi

```bash
# bara skrá inn skrá út bing bang bæng
litli-pdf-hjalpari -i "Downloads/scanned.pdf" -o "Documents/scanned_text_searchable.pdf"
# yfirskrifa output skrá sem er nú þegar til
litli-pdf-hjalpari -i "Downloads/scanned.pdf" -o "Documents/scanned_text_searchable.pdf" -ow
# skrá þar sem síður snúa ekki rétt, snúa síðunum 90° réttsælis
litli-pdf-hjalpari -i "Downloads/scanned.pdf" -rc -o "Documents/scanned_text_searchable.pdf"
# skönnuð skrá með tveimur síðum á hverri síðu, aðskilja í sér síður og snúa síðunum 90° rangsælis
litli-pdf-hjalpari -i "Downloads/scanned.pdf" -cph -rcc -o "Documents/scanned_text_searchable.pdf"
```
