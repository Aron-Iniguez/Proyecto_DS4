UNI SEARCH – Catálogo de Revistas Académicas

Desarrollo de Sistemas 4 | Proyecto Final 
Equipo:  
- Manuel Munguía Rubio  
- Aron Iñiguez Ruiz  
- Valeria Alejandra Jiménez Figueroa  
- Benjamín Isaac Rivera Tapia  

Asistente Digital: ChatGPT (OpenAI o4-mini)
Presentacion funcional del Proyecto: https://www.canva.com/design/DAGnM7AuBpU/rCeeVbvkgVkQhVXU1Z526w/edit?utm_content=DAGnM7AuBpU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
---

📋 Resumen del Proyecto

Uni Search es un sistema en **Python + Flask + Bootstrap** que integra tres componentes:

1. **CSV → JSON**  
   Lee archivos CSV de **áreas** y **catálogos** y genera `datos/json/revistas.json`.  
2. **Scraping**  
   - **SCImago**: Obtiene sitio web, H-Index, ISSN, publisher, widget, tipo de publicación y guarda `ultima_visita` (caché 30 días).  
   - **Resurchify**: Captura rank y categoría, con `res_last_checked`.  
3. **Frontend Web**  
   Interfaz para explorar y buscar revistas por **área**, **catálogo**, **letra** o **título**, mostrar todos los datos enriquecidos y gestionar **favoritos** (login/registro).

---

🚀 Tecnologías

- **Python 3.10+**, **Flask**, **Flask-Bcrypt**  
- **Bootstrap 5**, **DataTables**  
- **Requests**, **BeautifulSoup4**  
- **JSON** (datos, scimagojr, resurchify, usuarios)  
- **Git & GitHub** (control de versiones)

---

📂 Estructura

uni-search/
├── app.py # Rutas y lógica principal Flask
├── data.py # Carga CSV, scraping y caché
├── main.py # Script parte 1: CSV→JSON
├── requirements.txt
├── README.md
├── datos/
│ ├── csv/
│ │ ├── areas/
│ │ └── catalogos/
│ └── json/
│ ├── revistas.json
│ ├── revistas_scimagojr.json
│ ├── revistas_resurchify.json
│ └── users.json
├── static/
│ ├── css/custom.css
│ └── img/
│ ├── logo_unisearch.png
│ ├── logo_unison.png
│ └── hero_revistas.svg
└── templates/
├── base.html
├── index.html
├── areas.html
├── catalogos.html
├── explorar.html
├── busqueda.html
├── revista.html
├── login.html
├── register.html
├── favorites.html
└── creditos.html

---

⚙️ Instalación y Configuración

1. **Clonar repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/uni-search.git
   cd uni-search

2. Entorno
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows


3.Dependencias
pip install -r requirements.txt

4.Inicializar JSON de usuarios
mkdir -p datos/json
echo "{}" > datos/json/users.json

5.Configurar imágenes
logos en static/img/:

logo_unisearch.png

logo_unison.png

hero_revistas.svg (optional)

▶️ Ejecución

1.Generar JSON base (Parte 1)
python main.py --build-json
— Crea datos/json/revistas.json desde los CSV.
NOTA: main.py quedó descartado para la ejecución del programa, en su lugar se utiliza app.py

2.Iniciar Flask
export FLASK_APP=app.py
export FLASK_ENV=development   # Opcional para recarga automática
flask run --port=5000

🖥️ Uso de la Aplicación
Inicio: Hero con descripción y botones de acceso.
Áreas (/areas): Lista interactiva, tabla de revistas + H-Index.
Catálogos (/catalogos): Igual que Áreas, filtrando por catálogo.
Explorar (/explorar): Abecedario → revistas por inicial.
Búsqueda (/busqueda?q=…): Filtro por texto en título.
Detalle (/revista/<nombre>): Datos base, Scimago, Resurchify, fechas, widget.
Login/Registro (/login, /register): Autenticación segura.
Favoritos (/favorites): Guarda y consulta tus revistas.
Créditos (/creditos): Tabla dinámica con fotos y nombres.

📝Adicionales:
Cache inteligente: Solo se re-scrapea lo necesario.
Seguridad: Contraseñas hasheadas con Bcrypt; sesiones seguras.
Versiones: Asegúrate de usar Python ≥ 3.10 y Flask ≥ 2.0.
Asistente: Se utilizó ChatGPT para generar y revisar código, documentación y diseño.
Presentacion de uso de la pagina: https://www.canva.com/design/DAGnM7AuBpU/rCeeVbvkgVkQhVXU1Z526w/edit?utm_content=DAGnM7AuBpU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
