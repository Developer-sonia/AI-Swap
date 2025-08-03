#!/bin/bash

# Fix Swap Space Script
# This script increases swap space for better performance

echo "🔧 Fixing Swap Space for AI-Swap VPS"
echo "====================================="

# Check current swap
echo "📊 Current swap usage:"
free -h

# Create 4GB swap file
echo "💾 Creating 4GB swap file..."
sudo fallocate -l 4G /swapfile

# Set proper permissions
echo "🔐 Setting swap file permissions..."
sudo chmod 600 /swapfile

# Make it swap
echo "🔄 Setting up swap..."
sudo mkswap /swapfile

# Enable swap
echo "✅ Enabling swap..."
sudo swapon /swapfile

# Make swap permanent
echo "📝 Making swap permanent..."
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Set swappiness to 10 (prefer RAM over swap)
echo "⚙️ Optimizing swappiness..."
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl vm.swappiness=10

# Verify new swap
echo "📊 New swap configuration:"
free -h

echo ""
echo "✅ Swap space increased to 4GB!"
echo "🔄 You may need to reboot for all changes to take effect"
echo "💡 Run: sudo reboot" 