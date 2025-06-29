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
│   └── requirements.txt    # Python dependencies
├── frontend/               # React.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json        # Node.js dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Backend Setup
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
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup
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

## 🧰 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Image Processing**: OpenCV, MediaPipe
- **AI Models**: Face segmentation + face-preserving GAN
- **Storage**: AWS S3 / Firebase Storage
- **Database**: Firebase Firestore / MongoDB

### Frontend
- **Framework**: React.js
- **Styling**: Tailwind CSS
- **State Management**: React Context / Redux
- **HTTP Client**: Axios

## 📋 API Endpoints

### Core Endpoints
- `POST /upload` - Upload user image
- `GET /professions` - Get available professions
- `POST /swap-face` - Perform face swapping
- `GET /templates/{profession}` - Get profession templates

### Health Check
- `GET /health` - API health status
- `GET /docs` - Interactive API documentation

## 🖼️ Image Requirements
- Input image must match standard angles (front-facing, side, ¾ view)
- Supported formats: JPG, PNG, WebP
- Minimum resolution: 512x512 pixels
- Maximum file size: 10MB

## 🔮 Development Phases

### Phase 1: MVP (Current)
- [x] Project structure setup
- [ ] Backend API foundation
- [ ] Face detection and segmentation
- [ ] Basic face swapping
- [ ] Frontend upload interface
- [ ] Template selection UI

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

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License. 