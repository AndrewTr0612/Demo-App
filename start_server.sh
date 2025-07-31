#!/bin/bash

echo "🚀 Starting DeepSeek R1 LLM Server..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Ollama container exists
if docker ps -a --format '{{.Names}}' | grep -q "^deepseek-server$"; then
    echo "📦 Starting existing Ollama container..."
    docker start deepseek-server
else
    echo "📦 Creating new Ollama container with DeepSeek R1..."
    docker run -d -v ~/.ollama:/root/.ollama -p 11434:11434 --name deepseek-server ollama/ollama
fi

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "❌ Ollama failed to start within 30 seconds"
        exit 1
    fi
done

# Start Flask server
echo "🌐 Starting Flask web server with network access..."
echo "📱 Other devices can connect using your IP address on port 5001"
cd Server
python3 serverapp.py

echo "🎉 Setup complete!"
echo "🖥️  Local access: http://127.0.0.1:5001"
echo "📱 Network access: http://YOUR_IP:5001"
