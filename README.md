# Materiaal Uitslag Samenvatting Web App

A lightweight, secure Dockerized web application for processing woodworking CSV exports and calculating material edge lengths and widths.

---

## 🆕 What's New

- **Templates split:** The HTML is now in `templates/index.html` (not in the Python code).
- **Dutch interface:** All user-facing text is now in Dutch.
- **Headerless CSV support:** You can paste CSV data with or without headers.
- **Container security:** The GitHub Actions workflow scans the image with Trivy before pushing to GHCR.

---

## 🏗️ **Building and Running**

### Method 1: Docker Compose (Recommended)

#### Production Mode
```bash
# Pull and run the latest image from GitHub Container Registry
docker-compose up -d
```

#### Development Mode (with debug enabled)
```bash
# Run development configuration (local build, live reload)
docker-compose -f docker-compose.dev.yml up

# Or build and run with debug
docker-compose up -d
docker-compose exec materiaal-uitslag-web sh -c "DEBUG=true python app.py"
```

#### With Nginx Reverse Proxy
```bash
# Run with nginx reverse proxy
docker-compose --profile with-nginx up -d
```

### Method 2: Direct Docker/Podman

#### Production
```bash
# Build the image
podman build -t materiaal-uitslag-web .

# Run the container
podman run -d --name materiaal-uitslag-web -p 8080:8080 materiaal-uitslag-web

# Run with debug mode
podman run -d --name materiaal-uitslag-web -p 8080:8080 -e DEBUG=true materiaal-uitslag-web
```

#### Development
```bash
# Run with volume mount for development
podman run -d --name materiaal-uitslag-web-dev \
  -p 8080:8080 \
  -e DEBUG=true \
  -v $(pwd):/app \
  materiaal-uitslag-web
```

## 🌐 **Toegang tot de applicatie**

- **Webinterface**: http://localhost:8080
- **Met Nginx**: http://localhost (poort 80)

## 🎨 **Functionaliteit**

- **Donker/Licht Thema**: Moderne UI met thema-persistentie
- **Professioneel Logo**: Ingebouwd Leurs-logo
- **Debug Modus**: Debug-informatie via omgevingsvariabele
- **CSV-verwerking**: Tab-gescheiden CSV met materiaalkalculaties (met of zonder headers)
- **Responsief ontwerp**: Werkt op desktop en mobiel

## 📊 **Voorbeeldgebruik**

### Voorbeeld CSV Input
```
Materiaal	user0	Lengte	Breedte	Aantal	Onderdeel	Element	Kant_X2	Kant_X1	Kant_Y1	Kant_Y2
DECOR_01_18	1	2305.0	690.0	1	Front_Standaard_1.1	HK_Zichtzijde	X	X	X	X
U727_18	1	564.0	540.0	1	Bodem	k1 koeler		X
geen materiaal_18	1	563.0	520.0	2	Legplank	K2 OVEN		X
```

Of zonder headers:
```
DECOR_01_18	1	2305.0	690.0	1	Front_Standaard_1.1	HK_Zichtzijde	X	X	X	X
U727_18	1	564.0	540.0	1	Bodem	k1 koeler		X
geen materiaal_18	1	563.0	520.0	2	Legplank	K2 OVEN		X
```

### Verwachte Output
| Materiaal | TotaalUitslagLengte_m | TotaalUitslagBreedte_m | TotaalUitslagOpgeteld_m |
|-----------|----------------------|------------------------|-------------------------|
| DECOR_01_18 | 43.02 | 42.48 | 85.50 |
| U727_18 | 54.73 | 0.00 | 54.73 |
| geen materiaal_18 | 1.23 | 0.00 | 1.23 |

## 🚀 **Container Registry & CI**

- **Image wordt automatisch gebouwd en gescand met Trivy via GitHub Actions.**
- **Image wordt gepusht naar:** `ghcr.io/blankf/materiaal-calc:latest`
- **Pullen vanaf een andere host:**
  ```bash
  docker pull ghcr.io/blankf/materiaal-calc:latest
  ```
- Zie `.github/workflows/docker-publish.yml` voor details.

## 🔧 **Configuratie**

### Omgevingsvariabelen
- `DEBUG`: Zet op `true` om debugmodus te activeren (standaard: `false`)

### Docker Compose Profielen
- **Default**: Basis webapplicatie
- **with-nginx**: Inclusief nginx reverse proxy
- **dev**: Ontwikkelmodus met debug

### Volume Mounts
- `/app/logs`: Optionele logmap
- `/app`: Source code mount voor ontwikkeling

## 📁 **Bestandsstructuur**
```
materiaal-uitslag-web/
├── app.py                    # Flask applicatie (logica)
├── templates/index.html      # HTML template
├── leurs_logo.jpg            # Bedrijfslogo
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build instructies
├── docker-compose.yml        # Compose file (productie)
├── docker-compose.dev.yml    # Compose file (ontwikkeling)
├── nginx.conf                # Nginx configuratie
└── README.md                 # Deze file
```

## 🔒 **Security**

- Container wordt gescand met Trivy (CI)
- Applicatie draait als non-root user
- Inputvalidatie voor CSV
- Minimale attack surface (slim Python base image)

## 🛠️ **Development**

### Lokale ontwikkeling
```bash
pip install -r requirements.txt
DEBUG=true python app.py
# Open http://localhost:8080
```

### Multi-arch build
```bash
podman buildx build --platform linux/amd64,linux/arm64 -t materiaal-uitslag-web .
```

## 📝 **Changelog**

- **v1.0**: Eerste release met basis CSV-verwerking
- **v1.1**: Debugmodus en betere foutafhandeling
- **v1.2**: Donker thema, licht/donker toggle, logo
- **v1.3**: Docker Compose en uitgebreide documentatie
- **v1.4**: HTML in template, Nederlandse interface, headerloze CSV, Trivy scan in CI

## 🤝 **Bijdragen**

1. Fork de repository
2. Maak een feature branch
3. Doe je aanpassingen
4. Test
5. Maak een pull request

## 📄 **Licentie**

Dit project is voor intern gebruik bij Leurs.
