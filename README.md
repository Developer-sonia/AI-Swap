# AI-Swap: Professional Face Swapping Application

## 🧠 Core Idea
AI-Swap allows users to upload their image and map their face onto pre-rendered templates of various professions (Doctor, Professor, HR, etc.) across 4 standard angles. The face stays the same, but the rest (outfit, background, body) changes to match the chosen professional style.

## 🏗️ Project Structure
```
AI-Swap/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── templates/          # Pre-rendered profession templates
│   ├── uploads/            # User uploaded images
│   ├── results/            # Generated face swaps
│   └── requirements.txt    # Python dependencies
├── frontend/               # React.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json        # Node.js dependencies
├── deploy_optimized.sh     # VPS deployment script
├── docker-compose.yml      # Docker deployment
└── README.md              # This file
```

## 🚀 Quick Start

### Local Development

#### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # For production (minimal dependencies)
   pip install -r requirements-minimal.txt
   
   # For development (all dependencies)
   pip install -r requirements-dev.txt
   
   # For full production (all features)
   pip install -r backend/requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

#### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

### VPS Deployment

#### Quick Deployment (Recommended)
```bash
# Make script executable
chmod +x deploy_optimized.sh

# Run deployment
./deploy_optimized.sh
```

#### Manual Deployment
```bash
# Run manual setup
chmod +x manual_setup.sh
./manual_setup.sh
```

#### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🧰 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn + Gunicorn
- **Image Processing**: OpenCV, MediaPipe
- **AI Models**: Face segmentation + face-preserving GAN
- **Storage**: AWS S3 / Firebase Storage
- **Database**: Firebase Firestore / MongoDB

### Frontend
- **Framework**: React.js
- **Styling**: Tailwind CSS
- **State Management**: React Context
- **HTTP Client**: Axios
- **UI Components**: Lucide React, Framer Motion

### Deployment
- **VPS**: Ubuntu/Debian with systemd
- **Web Server**: Nginx
- **Process Manager**: systemd
- **Container**: Docker (optional)

## 📋 API Endpoints

### Core Endpoints
- `POST /upload` - Upload user image
- `GET /professions` - Get available professions
- `POST /swap-face` - Perform face swapping
- `GET /templates/{profession}` - Get profession templates

### Health Check
- `GET /health` - API health status
- `GET /docs` - Interactive API documentation
- `GET /` - Root endpoint with API info

## 🖼️ Image Requirements
- Input image must match standard angles (front-facing, side, ¾ view)
- Supported formats: JPG, PNG, WebP
- Minimum resolution: 512x512 pixels
- Maximum file size: 10MB

## 🔮 Development Phases

### Phase 1: MVP (Current)
- [x] Project structure setup
- [x] Backend API foundation (FastAPI)
- [x] Face detection and segmentation
- [x] Basic face swapping
- [x] Frontend upload interface
- [x] Template selection UI
- [x] VPS deployment scripts
- [x] Docker configuration

### Phase 2: Enhancement
- [ ] Advanced AI models integration
- [ ] Multiple profession templates
- [ ] Real-time preview
- [ ] User authentication
- [ ] Result history

### Phase 3: Production
- [ ] Cloud deployment
- [ ] Performance optimization
- [ ] Advanced error handling
- [ ] Analytics and monitoring

## 🚀 Deployment Options

### VPS Deployment (Recommended)
1. **Automated**: Use `deploy_optimized.sh`
2. **Manual**: Use `manual_setup.sh`
3. **Quick**: Use `quick_deploy.sh`

### Docker Deployment
1. **Docker Compose**: `docker-compose up -d`
2. **Docker Build**: `docker build -t ai-swap .`

### Environment Configuration
```bash
# Copy example environment
cp backend/env.example backend/.env

# Edit with your settings
nano backend/.env
```

## 📊 Monitoring & Management

### Service Management
```bash
# Start service
systemctl start ai-swap

# Stop service
systemctl stop ai-swap

# Restart service
systemctl restart ai-swap

# Check status
systemctl status ai-swap

# View logs
journalctl -u ai-swap -f
```

### Health Checks
```bash
# Test API
curl http://localhost:8000/health

# Test nginx
curl http://localhost

# Check resources
free -h
df -h
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License.

## 🆘 Support
- **Documentation**: Check `/docs` endpoint for API docs
- **Issues**: Create GitHub issues for bugs
- **Deployment**: Use provided deployment scripts 