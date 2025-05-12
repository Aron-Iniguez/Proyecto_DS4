import os
import csv
import json

# Rutas de las carpetas
base_path = 'datos'
areas_path = os.path.join(base_path, 'csv', 'areas')
catalogos_path = os.path.join(base_path, 'csv', 'catalogos')
json_path = os.path.join(base_path, 'json')
output_file = os.path.join(json_path, 'revistas.json')

revistas = {}

def procesar_csv(ruta, tipo):
    for archivo in os.listdir(ruta):
        if archivo.endswith(".csv"):
            ruta_archivo = os.path.join(ruta, archivo)

            # Obtener nombre de categoría limpio
            nombre_archivo = os.path.splitext(archivo)[0].upper()
            nombre_archivo = nombre_archivo.replace("RADGRIDEXPORT", "")
            nombre_archivo = nombre_archivo.replace("_", " ").strip()
            categoria = nombre_archivo.replace(" ", "_")

            # Leer archivo
            with open(ruta_archivo, encoding="latin1") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    titulo = row.get("TITULO:") or row.get("TÍTULO:")
                    if not titulo:
                        continue
                    titulo = titulo.strip().lower()

                    if titulo not in revistas:
                        revistas[titulo] = {"areas": [], "catalogos": []}

                    if tipo == "areas" and categoria not in revistas[titulo]["areas"]:
                        revistas[titulo]["areas"].append(categoria)
                    elif tipo == "catalogos" and categoria not in revistas[titulo]["catalogos"]:
                        revistas[titulo]["catalogos"].append(categoria)

procesar_csv(areas_path, "areas")
procesar_csv(catalogos_path, "catalogos")
os.makedirs(json_path, exist_ok=True)
# guardamos el trip como json
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(revistas, f, indent=4, ensure_ascii=False)

# Verificar que puede ser leído
with open(output_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    print("Archivo JSON leído correctamente. Número de revistas:", len(data))