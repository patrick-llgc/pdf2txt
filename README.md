# pdf2txt
This records multiple ways to convert a pdf to plain txt file.

- pdfminer
- pypdfocr
- pdf to png with imagemagick and then OCR using tesseract

### Iteration 1: [pdfminer](https://github.com/euske/pdfminer)
- install pdfminer (works with python 2 only!)
- create virtualenv env with python 2
- some files are encrypted with an empty password. install [	qpdf](https://stackoverflow.com/questions/16956875/how-can-i-install-qpdf-on-mac-10-8-3) to convert files
- Issues: some encrypted fields (or embedded pictures) cannot be extracted directly with pdfminer
- Solution: OCR

### Iteration 2: [pypdfocr](https://pypi.python.org/pypi/pypdfocr)
- install prerequisites
```
brew install tesseract
brew install ghostscript
brew install poppler
brew install imagemagick
```
- Issues: can only convert from pdf to pdf. Some word-only paragraphs in pdf files do not preserve prior word order after ocr.
`qpdf --password='' --decrypt encrypted decrypted`
- Solution: use tesseract direclty

### Iteration 3: [tesseract](https://github.com/tesseract-ocr/tesseract)
- convert pdf to png images
- ocr with tesseract
```
convert -density 300 -alpha off image.pdf[1] -resize 80% image-02.png
tesseract image-02.png outputtxt
```
- Issue: some words are not OCR'ed correctly. Need manual proofreading.

<!--
The necessary information is scattered in two places
- attachment on Page 11
- H11 item on Page 3

Thus a second round of text mining was performed and the two versions of json files are combined.
-->