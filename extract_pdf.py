from pathlib import Path
from PyPDF2 import PdfReader
p = Path(r'c:\projetos\kalawenda AI\Refatoração da LOTADORi (1).pdf')
r = PdfReader(p)
import sys
sys.stdout.reconfigure(encoding='utf-8')
for i, page in enumerate(r.pages):
    print('--- PAGE {} ---'.format(i+1))
    text = page.extract_text()
    print(text[:2000] if text else '')
