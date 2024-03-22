# sign_pdf
Script to autosign pdf files

## How to use
```bash
pip install -r requirements.txt
python pdf_autosign.py
```
### folder structure
to use pdf_autosign follow folder structure should be created first

# Project tree
``` bash
.my_folder_with_pdfs
├── data
│   ├── main_sign
│   │   └── main_sing.png
│   └── random_signs
│       ├── random_sign1.png
│       ├── random_sign2.png
│       └── random_signN.png
├── pdf_autosign.py
├── to_sign_pdf1.pdf
├── to_sign_pdf2.pdf
└── to_sign_pdfN.pdf
```

the script will search fields with text setted in:
```main_sign_txt``` and ```sub_sign_txt``` and place main_sign.png to the main_sign text field an random sign from random_signs folder to sub_sign text field