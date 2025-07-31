#!/bin/bash

echo "🧹 Starting Port Cleanup..."

# Kill all Python Flask servers
echo "1️⃣ Stopping Python/Flask servers..."
pkill -f "serverapp.py"
pkill -f "flask"

# Stop Ollama processes
echo "2️⃣ Stopping Ollama processes..."
pkill -f "ollama" 2>/dev/null || echo "No Ollama processes found"

# Stop all Docker containers
echo "3️⃣ Stopping Docker containers..."
docker stop $(docker ps -q) 2>/dev/null || echo "No running containers to stop"

# Remove all Docker containers
echo "4️⃣ Removing Docker containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

# Optional: Remove Docker images (uncomment if you want to clean everything)
# echo "5️⃣ Removing Docker images..."
# docker rmi $(docker images -q) 2>/dev/null || echo "No images to remove"

# Kill specific processes on common ports
echo "6️⃣ Checking for processes on common ports..."

# Port 5001 (your Flask server)
PID_5001=$(lsof -ti:5001 2>/dev/null)
if [ ! -z "$PID_5001" ]; then
    echo "Killing process on port 5001: $PID_5001"
    kill -9 $PID_5001
fi

# Port 11434 (Ollama)
PID_11434=$(lsof -ti:11434 2>/dev/null)
if [ ! -z "$PID_11434" ]; then
    echo "Killing process on port 11434: $PID_11434"
    kill -9 $PID_11434
fi

# Port 12434 (Docker)
PID_12434=$(lsof -ti:12434 2>/dev/null)
if [ ! -z "$PID_12434" ]; then
    echo "Killing process on port 12434: $PID_12434"
    kill -9 $PID_12434
fi

echo "7️⃣ Final port check..."
echo "Checking ports 5000, 5001, 11434:"
lsof -i :5000 -i :5001 -i :11434 2>/dev/null || echo "✅ All target ports are clean!"

echo "🎉 Cleanup complete!"
echo ""
echo "📋 Summary of what was cleaned:"
echo "   - Python/Flask servers (serverapp.py)"
echo "   - Ollama processes"
echo "   - Docker containers"
echo "   - Processes on ports 5001, 11434, 12434"
echo ""
echo "Note: Port 5000 may still show ControlCenter (macOS system service) - this is normal."
