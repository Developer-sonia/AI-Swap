# AI-Swap VPS Deployment Guide

This guide provides multiple options for deploying the AI-Swap application on a VPS server.

## Prerequisites

- Ubuntu 20.04+ or Debian 11+ VPS
- Root or sudo access
- At least 2GB RAM (4GB recommended)
- At least 10GB storage

## Option 1: Automated Setup (Recommended)

### Quick Start
```bash
# Clone your repository to the VPS
git clone <your-repo-url>
cd AI-Swap

# Make the setup script executable
chmod +x setup_vps.sh

# Run the automated setup
./setup_vps.sh
```

### What the automated script does:
1. Updates system packages
2. Installs Python 3.10 and dependencies
3. Creates virtual environment
4. Installs Python packages
5. Sets up systemd service
6. Configures nginx
7. Creates necessary directories

## Option 2: Manual Setup

### Step-by-step manual installation:
```bash
# Run the manual setup script
chmod +x manual_setup.sh
./manual_setup.sh
```

### Manual steps (if you prefer full control):
```bash
# 1. Install Python 3.10
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# 2. Install system dependencies
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# 3. Create application directory
sudo mkdir -p /opt/ai-swap
sudo chown $USER:$USER /opt/ai-swap

# 4. Copy application files
cp -r backend /opt/ai-swap/
cp -r frontend /opt/ai-swap/

# 5. Create virtual environment
cd /opt/ai-swap
python3.10 -m venv venv

# 6. Install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# 7. Create directories
mkdir -p backend/uploads backend/results backend/logs
chmod 755 backend/uploads backend/results backend/logs

# 8. Setup environment
cp backend/env.example backend/.env
# Edit backend/.env with your configuration
```

## Option 3: Docker Deployment

### Using Docker Compose (Easiest)
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker directly
```bash
# Build the image
docker build -t ai-swap .

# Run the container
docker run -d \
  --name ai-swap \
  -p 8000:8000 \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/results:/app/backend/results \
  -v $(pwd)/backend/.env:/app/backend/.env \
  ai-swap
```

## Configuration

### Environment Variables
Edit `backend/.env` with your configuration:
```bash
# Copy example file
cp backend/env.example backend/.env

# Edit the file
nano backend/.env
```

### Required Environment Variables:
- Database connection strings
- API keys
- File storage paths
- Security settings

## Service Management

### Systemd Service (Option 1 & 2)
```bash
# Start the service
sudo systemctl start ai-swap

# Enable auto-start
sudo systemctl enable ai-swap

# Check status
sudo systemctl status ai-swap

# View logs
sudo journalctl -u ai-swap -f

# Restart service
sudo systemctl restart ai-swap
```

### Docker Services (Option 3)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f ai-swap

# Restart services
docker-compose restart

# Stop services
docker-compose down
```

## Nginx Configuration

### For Option 1 & 2:
The setup script automatically configures nginx. If you need to modify:

```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/ai-swap

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### For Option 3:
Nginx is included in the docker-compose setup.

## Security Considerations

### Firewall Setup
```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### SSL Certificate (Optional)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logs

### Application Logs
```bash
# Systemd service logs
sudo journalctl -u ai-swap -f

# Docker logs
docker-compose logs -f ai-swap

# Direct log files
tail -f /opt/ai-swap/backend/logs/app.log
```

### System Monitoring
```bash
# Check resource usage
htop

# Check disk usage
df -h

# Check memory usage
free -h
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   sudo netstat -tlnp | grep :8000
   sudo lsof -i :8000
   ```

2. **Permission denied**
   ```bash
   sudo chown -R $USER:$USER /opt/ai-swap
   chmod 755 /opt/ai-swap/backend/uploads
   ```

3. **Virtual environment not found**
   ```bash
   cd /opt/ai-swap
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

4. **Docker build fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker build --no-cache -t ai-swap .
   ```

### Health Check
```bash
# Test the application
curl http://localhost:8000/health

# Check if service is running
sudo systemctl is-active ai-swap
```

## Backup and Maintenance

### Backup Script
```bash
#!/bin/bash
# Backup application data
tar -czf ai-swap-backup-$(date +%Y%m%d).tar.gz \
  /opt/ai-swap/backend/uploads \
  /opt/ai-swap/backend/results \
  /opt/ai-swap/backend/.env
```

### Update Process
```bash
# Stop service
sudo systemctl stop ai-swap

# Pull latest code
cd /opt/ai-swap
git pull

# Update dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# Start service
sudo systemctl start ai-swap
```

## Performance Optimization

### Gunicorn Configuration
Edit `backend/gunicorn.conf.py` for performance tuning:
```python
# Increase workers for better performance
workers = 4
worker_class = 'sync'
worker_connections = 1000
```

### Nginx Optimization
```nginx
# Add to nginx configuration
client_max_body_size 100M;
proxy_read_timeout 300;
proxy_connect_timeout 300;
```

## Support

For issues and support:
1. Check the logs first
2. Verify environment configuration
3. Test with a simple curl request
4. Check system resources

The application should be accessible at `http://your-server-ip` once deployed successfully. 