# data.py 
import os
import json
from datetime import datetime, timedelta
from functools import lru_cache
import requests
from bs4 import BeautifulSoup

# Directorio base y rutas
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
BASE_FILE = os.path.join(BASE_DIR, 'datos', 'json', 'revistas.json')
SCIMAGO_FILE = os.path.join(BASE_DIR, 'datos', 'json', 'revistas_scimagojr.json')
RESURCH_FILE = os.path.join(BASE_DIR, 'datos', 'json', 'revistas_resurchify.json')

# Caducidad de 30 días para refreshing
CADUCIDAD = timedelta(days=30)

@lru_cache()
def cargar_base(path=BASE_FILE):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def scrape_revista(titulo):
    url = f'https://www.scimagojr.com/journalsearch.php?q={requests.utils.quote(titulo)}'
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        hi = soup.select_one('.hindex')
        issn_el = soup.find(text=lambda t: 'ISSN' in t)
        issn = issn_el.find_next('td') if issn_el else None
        pub_el = soup.find(text=lambda t: 'Publisher' in t)
        publisher = pub_el.find_next('td') if pub_el else None
        type_el = soup.find(text=lambda t: 'Publication Type' in t)
        pub_type = type_el.find_next('td') if type_el else None
        website_el = soup.select_one('a[href^="http"]')
        widget_el = soup.select_one('#Widget')
        return {
            'h_index': hi.text.strip() if hi else 'N/A',
            'issn': issn.text.strip() if issn else 'N/A',
            'publisher': publisher.text.strip() if publisher else 'N/A',
            'publication_type': pub_type.text.strip() if pub_type else 'N/A',
            'website': website_el['href'] if website_el else 'N/A',
            'widget': str(widget_el) if widget_el else '',
            'ultima_visita': datetime.now().isoformat()
        }
    except Exception:
        return {
            'h_index': 'N/A',
            'issn': 'N/A',
            'publisher': 'N/A',
            'publication_type': 'N/A',
            'website': 'N/A',
            'widget': '',
            'ultima_visita': datetime.now().isoformat()
        }

def get_scimago_info(titulo):
    datos = {}
    if os.path.exists(SCIMAGO_FILE):
        with open(SCIMAGO_FILE, encoding='utf-8') as f:
            datos = json.load(f)
    entry = datos.get(titulo)
    refrescar = False
    if not entry or 'ultima_visita' not in entry:
        refrescar = True
    else:
        try:
            ult = datetime.fromisoformat(entry['ultima_visita'])
            if datetime.now() - ult > CADUCIDAD:
                refrescar = True
        except Exception:
            refrescar = True
    if refrescar:
        entry = scrape_revista(titulo)
        datos[titulo] = entry
        os.makedirs(os.path.dirname(SCIMAGO_FILE), exist_ok=True)
        with open(SCIMAGO_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    return entry or {}