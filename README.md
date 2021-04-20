
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

## Tesseract CLI

### Arch

```zsh
sudo pacman -Syu
sudo pacman -S tesseract
```

### Debian/Ubuntu

```zsh
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev
```

### Windows

[Find, download and execute some EXE file?](https://medium.com/quantrium-tech/installing-and-using-tesseract-4-on-windows-10-4f7930313f82)

# Notkun

```zsh
python litli_pdf_hjalpari.py -h
```
