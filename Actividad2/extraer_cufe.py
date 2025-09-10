import os
import re
import sqlite3
from PyPDF2 import PdfReader

# Configuración
PDF_DIR = 'pdfs'
DB_FILE = 'facturas.db'
# CUFE: 32 hex + 32 hex + 32 hex + 1 hex = 97 hex (sin saltos de línea)
CUFE_REGEX = r'([0-9a-fA-F]{95,100})'

# Crear/conectar base de datos
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT,
    numero_paginas INTEGER,
    cufe TEXT,
    peso_archivo INTEGER
)''')

# Procesar PDFs
def extraer_info_pdf(pdf_path):
    nombre_archivo = os.path.basename(pdf_path)
    peso_archivo = os.path.getsize(pdf_path)
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        numero_paginas = len(reader.pages)
        texto = ''
        for page in reader.pages:
            texto += page.extract_text() or ''
        # Limpiar texto: quitar saltos de línea y espacios
        texto_limpio = texto.replace('\n', '').replace(' ', '')
        match = re.search(CUFE_REGEX, texto_limpio)
        cufe = match.group(0) if match else None
    return nombre_archivo, numero_paginas, cufe, peso_archivo

for filename in os.listdir(PDF_DIR):
    if filename.lower().endswith('.pdf'):
        ruta = os.path.join(PDF_DIR, filename)
        nombre_archivo, numero_paginas, cufe, peso_archivo = extraer_info_pdf(ruta)
        c.execute('INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo) VALUES (?, ?, ?, ?)',
                  (nombre_archivo, numero_paginas, cufe, peso_archivo))
        print(f'Procesado: {nombre_archivo} | Páginas: {numero_paginas} | CUFE: {cufe} | Peso: {peso_archivo}')

conn.commit()
conn.close()
print('Extracción completada. Datos guardados en facturas.db')
