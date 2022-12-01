import os
import re
import json
from pathlib import Path
from subprocess import check_call, DEVNULL
from tempfile import TemporaryDirectory
from datetime import datetime

import PyPDF3


def extract_text(pdf):
    """Extract and return text in the pdf that is not in raster images"""
    with open(pdf, 'rb') as f:
        p = PyPDF3.PdfFileReader(f)
        page = p.getPage(0)
        return page.extractText().replace('\n', '')


def extract_image_text(pdf, rasterise=False):
    """Extract and return text in the pdf that is in the first raster image"""
    with TemporaryDirectory() as tempdir:
        if rasterise:
            check_call(
                [
                    'convert',
                    '-density',
                    '150',
                    pdf.absolute(),
                    '-quality',
                    '100',
                    'output.png',
                ],
                cwd=tempdir,
            )
        else:
            check_call(['pdfimages', '-all', pdf.absolute(), 'image'], cwd=tempdir)
            check_call(
                [
                    'convert',
                    'image-000.png',
                    'image-001.png',
                    '-alpha',
                    'Off',
                    '-compose',
                    'CopyOpacity',
                    '-composite',
                    'output.png',
                ],
                cwd=tempdir,
            )
        check_call(
            ['tesseract', 'output.png', 'tesseract'],
            cwd=tempdir,
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
        s = Path(tempdir, 'tesseract.txt').read_text('utf8')

        OCR_replacements = {
            'Ocl': 'Oct',
            'JuI': 'Jul'
        }

        for orig, replacement in OCR_replacements.items():
            s = s.replace(orig, replacement)
        return s


DATAFILE = Path('pdfdata.json')
try:
    pdfdata = json.loads(DATAFILE.read_text())
except FileNotFoundError:
    pdfdata = {}

for f in sorted(Path('pdfs').iterdir(), key=lambda s: -os.stat(s).st_mtime):
    s = extract_text(f)
    date = re.search(r'(\d{1,2})(?:|st|nd|rd|th) ([A-Z][a-z]+) (\d{4})', s).groups()
    date = datetime.strptime('-'.join(date), '%d-%B-%Y').strftime('%Y-%m-%d')
    print(f'{f.name}')
    if date not in pdfdata:
        print(f'{f.name} → {date}')
        # On Oct 4 they switched to vector-based images. For now we just rasterise and
        # do OCR as normal. But in principle the text should be extractable now without
        # OCR
        s = extract_image_text(f, rasterise=True)
        rates = [float(a) for a in re.findall(r'\d\.\d{3}', s)]
        months = re.findall(r'([A-Z][a-z]{2})[^A-Za-z0-9]*(\d{2})[^\d]', s)
        assert months and len(months) == len(rates)
        pdfdata[date] = {f'{mmm}-{y}': r for (mmm, y), r in zip(months, rates)}
    else:
        break

# hard-code July 8th 2022 data, and Oct 3rd 2022, ASX didn't release a PDF then so we
# use the numbers from the asx short-term-derivatives page after close of market that
# day:
pdfdata['2022-07-08'] = {
    "Jul-22": 100 - 98.775,
    "Aug-22": 100 - 98.285,
    "Sep-22": 100 - 97.960,
    "Oct-22": 100 - 97.585,
    "Nov-22": 100 - 97.200,
    "Dec-22": 100 - 96.920,
    "Jan-23": 100 - 96.850,
    "Feb-23": 100 - 96.640,
    "Mar-23": 100 - 96.520,
    "Apr-23": 100 - 96.485,
    "May-23": 100 - 96.475,
    "Jun-23": 100 - 96.485,
    "Jul-23": 100 - 96.510,
    "Aug-23": 100 - 96.535,
    "Sep-23": 100 - 96.555,
    "Oct-23": 100 - 96.580,
    "Nov-23": 100 - 96.595,
}
pdfdata['2022-10-03'] = {
    "Oct-22": 100 - 97.300,
    "Nov-22": 100 - 96.9150,
    "Dec-22": 100 - 96.6900,
    "Jan-23": 100 - 96.6250,
    "Feb-23": 100 - 96.4600,
    "Mar-23": 100 - 96.2300,
    "Apr-23": 100 - 96.0050,
    "May-23": 100 - 95.8750,
    "Jun-23": 100 - 95.8700,
    "Jul-23": 100 - 95.8600,
    "Aug-23": 100 - 95.8650,
    "Sep-23": 100 - 95.8800,
    "Oct-23": 100 - 95.9000,
    "Nov-23": 100 - 95.9150,
    "Dec-23": 100 - 95.9450,
    "Jan-24": 100 - 95.9500,
    "Feb-24": 100 - 95.9600,
    "Mar-24": 100 - 95.9800,
}
pdfdata['2022-10-27'] = {
    "Oct-22": 100 - 97.4750,
    "Nov-22": 100 - 97.1400,
    "Dec-22": 100 - 96.9300,
    "Jan-23": 100 - 96.8850,
    "Feb-23": 100 - 96.7100,
    "Mar-23": 100 - 96.4900,
    "Apr-23": 100 - 96.2800,
    "May-23": 100 - 96.1100,
    "Jun-23": 100 - 96.0300,
    "Jul-23": 100 - 95.9650,
    "Aug-23": 100 - 95.9600,
    "Sep-23": 100 - 95.9550,
    "Oct-23": 100 - 95.9600,
    "Nov-23": 100 - 95.9600,
    "Dec-23": 100 - 95.9900,
    "Jan-24": 100 - 95.9950,
    "Feb-24": 100 - 96.0150,
    "Mar-24": 100 - 96.0500,
}


pdfdata['2022-07-08'] = {k: float(f"{v:.3f}") for k, v in pdfdata['2022-07-08'].items()}
pdfdata['2022-10-03'] = {k: float(f"{v:.3f}") for k, v in pdfdata['2022-10-03'].items()}
pdfdata['2022-10-27'] = {k: float(f"{v:.3f}") for k, v in pdfdata['2022-10-27'].items()}
pdfdata = {k: v for k, v in sorted(pdfdata.items())}

DATAFILE.write_text(json.dumps(pdfdata, indent=4))
