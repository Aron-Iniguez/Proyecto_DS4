import os
import csv
import json
import time
import re
import difflib
import chardet
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#Este main ya no se usa se dividio en app.py y data.py para mejor funcionamiento
# Rutas de las carpetas
base_path = 'datos'
areas_path = os.path.join(base_path, 'csv', 'areas')
catalogos_path = os.path.join(base_path, 'csv', 'catalogos')
json_path = os.path.join(base_path, 'json')
output_file = os.path.join(json_path, 'revistas.json')

entrada_json = "datos/json/revistas.json" # entrada para el scrapper
salida_json = "datos/json/revistas_scimagojr.json"

#headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
revistas = {}


if os.path.isfile(salida_json):
    with open(salida_json, 'r', encoding='utf-8') as f:
        catalogo_existente = json.load(f)
else:
    catalogo_existente = {}

with open(entrada_json, 'r', encoding='utf-8') as f:
    revistas = json.load(f)

def buscar_en_scimago(nombre_revista):
    try:
        query = nombre_revista.replace(' ', '+')
        url = f"https://www.scimagojr.com/journalsearch.php?q={query}"

        #print(f"Buscando: {url}")
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Buscar todos los <a> dentro del div de resultados
        resultados = soup.select("div.search_results a")
        revistas = []

        for res in resultados:
            span = res.find("span", class_="jrnlname")
            if span:
                titulo = span.get_text(strip=True)
                href = res.get("href")
                revistas.append({"titulo": titulo, "href": href})

        if not revistas:
            print("No se encontraron resultados.")
            return None

        # Usar difflib para encontrar coincidencia más cercana
        titulos = [rev["titulo"] for rev in revistas]
        coincidencia = difflib.get_close_matches(nombre_revista.strip(), titulos, n=1, cutoff=0.6)

        if not coincidencia:
            print("No hay coincidencia cercana para:", nombre_revista)
            return None

        # Obtener href correspondiente
        revista_match = next((rev for rev in revistas if rev["titulo"] == coincidencia[0]), None)
        if not revista_match:
            print("No se encontró el enlace asociado.")
            return None

        url_revista = "https://www.scimagojr.com/" + revista_match["href"]
        #print(f"Enlace a revista: {url_revista}")
        r = requests.get(url_revista, headers=headers, timeout=1)
        soup_detalle = BeautifulSoup(r.text, "html.parser")

        def extraer_info(label):
            tag = soup_detalle.find(string=re.compile(label, re.IGNORECASE))
            return tag.find_next().text.strip() if tag else None

        info = {
            "titulo": revista_match["titulo"],
            "url": url_revista,
            "fecha_consulta": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "H-Index": extraer_info("H index"),
            "Subject Area and Category": extraer_info("Subject Area and Category"),
            "Publisher": extraer_info("Publisher"),
            "ISSN": extraer_info("ISSN"),
            "Publication Type": extraer_info("Type"),
            "Widget": None
        }

        iframe = soup_detalle.find("iframe")
        if iframe and 'src' in iframe.attrs:
            info["Widget"] = iframe['src']

        return info

    except Exception as e:
        print("Error al buscar revista:", nombre_revista)
        print(e)
        return None

for titulo in revistas:
    if titulo in catalogo_existente:
        print(f"{titulo} ya existe")
        continue

    datos = buscar_en_scimago(titulo)
    if datos:
        catalogo_existente[titulo] = datos
        with open(salida_json, 'w', encoding='utf-8') as f:
            json.dump(catalogo_existente, f, indent=4, ensure_ascii=False)
    time.sleep(1)