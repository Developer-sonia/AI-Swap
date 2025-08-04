#!/bin/bash

# Optimized VPS Deployment for AI-Swap
# Optimized for: 2GB RAM, 40GB Disk, 1000GB Bandwidth

set -e

echo "🚀 Optimized AI-Swap Deployment for 2GB RAM VPS"
echo "================================================"

# Step 1: Fix swap space first
echo "💾 Step 1: Optimizing swap space..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
    sudo sysctl vm.swappiness=10
    echo "✅ Swap space increased to 4GB"
else
    echo "✅ Swap file already exists"
fi

# Step 2: Update system
echo "📦 Step 2: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 3: Install Python 3.10 with minimal dependencies
echo "🐍 Step 3: Installing Python 3.10..."
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Step 4: Install only essential OpenCV dependencies
echo "🔧 Step 4: Installing essential dependencies..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6

# Step 5: Create application directory
echo "📁 Step 5: Setting up application directory..."
sudo mkdir -p /opt/ai-swap
sudo chown $USER:$USER /opt/ai-swap

# Step 6: Copy application files
echo "📋 Step 6: Copying application files..."
cp -r backend /opt/ai-swap/
cp -r frontend /opt/ai-swap/

# Step 7: Create virtual environment
echo "🔧 Step 7: Creating Python virtual environment..."
cd /opt/ai-swap
python3.10 -m venv venv

# Step 8: Install dependencies with memory optimization
echo "📦 Step 8: Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Step 9: Create directories
echo "📁 Step 9: Creating necessary directories..."
mkdir -p backend/uploads backend/results backend/logs
chmod 755 backend/uploads backend/results backend/logs

# Step 10: Setup environment
echo "⚙️ Step 10: Setting up environment configuration..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

# Step 11: Create optimized gunicorn config for 2GB RAM
echo "🔧 Step 11: Creating optimized gunicorn configuration..."
cat > backend/gunicorn_optimized.conf.py << 'EOF'
# Optimized gunicorn config for 2GB RAM VPS
bind = "127.0.0.1:8000"
workers = 2  # Reduced for 2GB RAM
worker_class = "sync"
worker_connections = 500
max_requests = 1000
max_requests_jitter = 100
timeout = 300
keepalive = 2
preload_app = True
EOF

# Step 12: Create systemd service with memory limits
echo "🔧 Step 12: Creating systemd service..."
sudo tee /etc/systemd/system/ai-swap.service > /dev/null <<EOF
[Unit]
Description=AI-Swap Application (Optimized for 2GB RAM)
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/opt/ai-swap
Environment=PATH=/opt/ai-swap/venv/bin
ExecStart=/opt/ai-swap/venv/bin/gunicorn --config backend/gunicorn_optimized.conf.py backend.wsgi:app
Restart=always
RestartSec=10
MemoryMax=1.5G
MemoryHigh=1.2G

[Install]
WantedBy=multi-user.target
EOF

# Step 13: Enable and start service
echo "🔧 Step 13: Enabling systemd service..."
sudo systemctl daemon-reload
sudo systemctl enable ai-swap.service

# Step 14: Create simple nginx config
echo "🌐 Step 14: Setting up nginx..."
sudo apt install -y nginx
sudo tee /etc/nginx/sites-available/ai-swap > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 50M;
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static/ {
        alias /opt/ai-swap/frontend/static/;
        expires 1y;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ai-swap /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo ""
echo "✅ Optimized deployment complete!"
echo ""
echo "📊 System Status:"
free -h
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Start the service: sudo systemctl start ai-swap"
echo "3. Check status: sudo systemctl status ai-swap"
echo "4. View logs: sudo journalctl -u ai-swap -f"
echo ""
echo "🌐 The application will be available at: http://your-server-ip"
echo ""
echo "💡 Memory optimizations applied:"
echo "  - 4GB swap space created"
echo "  - Gunicorn workers reduced to 2"
echo "  - Memory limits set in systemd"
echo "  - Optimized nginx configuration" 