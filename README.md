# Materiaal Uitslag Samenvatting Web App

A lightweight, secure Dockerized web application for processing woodworking CSV exports and calculating material edge lengths and widths.

## 🏗️ **Building and Running**

### Method 1: Docker Compose (Recommended)

#### Production Mode
```bash
# Build and run with docker-compose
docker-compose up -d

# Or with Podman
podman-compose up -d
```

#### Development Mode (with debug enabled)
```bash
# Run development configuration
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

## 🌐 **Accessing the Application**

- **Web Interface**: http://localhost:8080
- **With Nginx**: http://localhost (port 80)

## 🎨 **Features**

- **Dark/Light Theme Toggle**: Modern UI with theme persistence
- **Professional Logo**: Embedded Leurs logo
- **Debug Mode**: Toggle debug information via environment variable
- **CSV Processing**: Handles tab-separated CSV with material calculations
- **Responsive Design**: Works on desktop and mobile devices

## 📊 **Usage Examples**

### Example CSV Input
```
Materiaal	user0	Lengte	Breedte	Aantal	Onderdeel	Element	Kant_X2	Kant_X1	Kant_Y1	Kant_Y2
DECOR_01_18	1	2305.0	690.0	1	Front_Standaard_1.1	HK_Zichtzijde	X	X	X	X
U727_18	1	564.0	540.0	1	Bodem	k1 koeler		X
geen materiaal_18	1	563.0	520.0	2	Legplank	K2 OVEN		X
```

### Expected Output
| Materiaal | TotaalUitslagLengte_m | TotaalUitslagBreedte_m | TotaalUitslagOpgeteld_m |
|-----------|----------------------|------------------------|-------------------------|
| DECOR_01_18 | 43.02 | 42.48 | 85.50 |
| U727_18 | 54.73 | 0.00 | 54.73 |
| geen materiaal_18 | 1.23 | 0.00 | 1.23 |

## 🚀 **Container Registry Options**

### 1. Docker Hub
```bash
# Tag your image
podman tag materiaal-uitslag-web yourusername/materiaal-uitslag-web:latest

# Login and push
podman login docker.io
podman push yourusername/materiaal-uitslag-web:latest

# Others can pull with:
podman pull yourusername/materiaal-uitslag-web:latest
```

### 2. Quay.io (Red Hat's registry)
```bash
# Tag for Quay.io
podman tag materiaal-uitslag-web quay.io/yourusername/materiaal-uitslag-web:latest

# Login and push
podman login quay.io
podman push quay.io/yourusername/materiaal-uitslag-web:latest

# Pull command for others:
podman pull quay.io/yourusername/materiaal-uitslag-web:latest
```

### 3. GitHub Container Registry (ghcr.io)
```bash
# Tag for GitHub Container Registry
podman tag materiaal-uitslag-web ghcr.io/yourusername/materiaal-uitslag-web:latest

# Login with GitHub Personal Access Token
echo $GITHUB_TOKEN | podman login ghcr.io -u yourusername --password-stdin

# Push
podman push ghcr.io/yourusername/materiaal-uitslag-web:latest

# Pull command for others:
podman pull ghcr.io/yourusername/materiaal-uitslag-web:latest
```

### 4. Azure Container Registry (ACR)
```bash
# Tag for ACR
podman tag materiaal-uitslag-web yourregistry.azurecr.io/materiaal-uitslag-web:latest

# Login to ACR
az acr login --name yourregistry
# Or with podman directly
podman login yourregistry.azurecr.io

# Push
podman push yourregistry.azurecr.io/materiaal-uitslag-web:latest
```

### 5. Google Container Registry (GCR)
```bash
# Tag for GCR
podman tag materiaal-uitslag-web gcr.io/your-project-id/materiaal-uitslag-web:latest

# Configure authentication
gcloud auth configure-docker

# Push
podman push gcr.io/your-project-id/materiaal-uitslag-web:latest
```

### 6. Private Registry
```bash
# For a private registry
podman tag materiaal-uitslag-web your-registry.com/materiaal-uitslag-web:latest
podman login your-registry.com
podman push your-registry.com/materiaal-uitslag-web:latest
```

## 🔧 **Configuration**

### Environment Variables
- `DEBUG`: Set to `true` to enable debug mode (default: `false`)

### Docker Compose Profiles
- **Default**: Basic web application
- **with-nginx**: Includes nginx reverse proxy
- **dev**: Development mode with debug enabled

### Volume Mounts
- `/app/logs`: Optional log directory
- `/app`: Development source code mount

## 📁 **File Structure**
```
materiaal-uitslag-web/
├── app.py                    # Main Flask application
├── leurs_logo.jpg           # Company logo
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container build instructions
├── docker-compose.yml      # Production compose file
├── docker-compose.dev.yml  # Development compose file
├── nginx.conf              # Nginx configuration
└── README.md               # This file
```

## 🔒 **Security Notes**

- The application runs as a non-root user inside the container
- No external dependencies beyond Flask
- Input validation for CSV processing
- Minimal attack surface with lightweight Alpine Linux base

## 🛠️ **Development**

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run with debug
DEBUG=true python app.py

# Access at http://localhost:8080
```

### Building for Different Architectures
```bash
# Build for multiple architectures
podman buildx build --platform linux/amd64,linux/arm64 -t materiaal-uitslag-web .

# Or build specifically for ARM64 (Apple Silicon, Raspberry Pi)
podman build --platform linux/arm64 -t materiaal-uitslag-web:arm64 .
```

## 📝 **Changelog**

- **v1.0**: Initial release with basic CSV processing
- **v1.1**: Added debug mode and enhanced error handling
- **v1.2**: Dark theme with light mode toggle and logo integration
- **v1.3**: Docker Compose support and comprehensive documentation

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both Docker and Podman
5. Submit a pull request

## 📄 **License**

This project is for internal use at Leurs.
