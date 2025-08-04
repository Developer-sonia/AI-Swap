#!/bin/bash

# AI-Swap VPS Deployment Script
# This script sets up the environment for running the AI-Swap application on a VPS

set -e  # Exit on any error

echo "🚀 Starting AI-Swap VPS Setup..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.10 and pip
echo "🐍 Installing Python 3.10..."
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install system dependencies for OpenCV
echo "🔧 Installing system dependencies..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/ai-swap
sudo chown $USER:$USER /opt/ai-swap

# Navigate to application directory
cd /opt/ai-swap

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3.10 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads backend/results backend/logs

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 backend/uploads backend/results backend/logs

# Create environment file
echo "⚙️ Creating environment configuration..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

# Create systemd service file
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/ai-swap.service > /dev/null <<EOF
[Unit]
Description=AI-Swap Application
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/opt/ai-swap
Environment=PATH=/opt/ai-swap/venv/bin
ExecStart=/opt/ai-swap/venv/bin/gunicorn --config backend/gunicorn.conf.py backend.wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo "🔧 Enabling systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable ai-swap.service

# Create nginx configuration (if nginx is installed)
echo "🌐 Creating nginx configuration..."
sudo tee /etc/nginx/sites-available/ai-swap > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /opt/ai-swap/frontend/static/;
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/ai-swap /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

echo "✅ VPS Setup Complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Start the service: sudo systemctl start ai-swap"
echo "3. Check status: sudo systemctl status ai-swap"
echo "4. View logs: sudo journalctl -u ai-swap -f"
echo ""
echo "🌐 The application will be available at: http://your-server-ip"
echo ""
echo "📝 Useful commands:"
echo "  - Start service: sudo systemctl start ai-swap"
echo "  - Stop service: sudo systemctl stop ai-swap"
echo "  - Restart service: sudo systemctl restart ai-swap"
echo "  - View logs: sudo journalctl -u ai-swap -f"
echo "  - Check status: sudo systemctl status ai-swap" 