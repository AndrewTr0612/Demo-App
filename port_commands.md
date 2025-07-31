# Port Management Commands

## Check what's using specific ports:
lsof -i :5000
lsof -i :5001
lsof -i :11434

## Check all listening ports:
lsof -i -P -n | grep LISTEN

## Kill process by port:
kill -9 $(lsof -ti:5001)

## Kill Python processes:
pkill -f "serverapp.py"
pkill -f "python"

## Docker cleanup:
docker stop $(docker ps -q)      # Stop all containers
docker rm $(docker ps -aq)       # Remove all containers
docker rmi $(docker images -q)   # Remove all images

## Process management:
ps aux | grep python              # Show Python processes
ps aux | grep ollama              # Show Ollama processes

## Quick port availability check:
nc -z localhost 5001 && echo "Port 5001 is in use" || echo "Port 5001 is free"
