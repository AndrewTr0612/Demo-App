# Save this file as app.py
from flask import Flask, request, jsonify, send_from_directory
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Health check endpoint to test Ollama connection
@app.route('/api/health', methods=['GET'])
def health_check():
    api_endpoints = [
        'http://localhost:11434/api/tags'  # Ollama models endpoint
    ]
    
    status = {}
    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                status[endpoint] = "Available"
                models = response.json().get('models', [])
                status['available_models'] = [model.get('name', 'unknown') for model in models]
            else:
                status[endpoint] = f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            status[endpoint] = f"Connection failed: {str(e)}"
    
    return jsonify({"api_status": status})

# Route to act as a proxy for the Ollama API
@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is missing"}), 400

    # Ollama API endpoint for DeepSeek R1
    api_endpoints = [
        'http://localhost:11434/api/generate',  # Ollama API endpoint
    ]
    
    # Use DeepSeek R1 model
    payload = {
        "model": "deepseek-r1",
        "prompt": prompt,
        "stream": False
    }

    try:
        # Try the Ollama API endpoint
        api_url = api_endpoints[0]
        print(f"\nTrying Ollama API endpoint: {api_url}")
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("Successfully received response from DeepSeek R1!")
            ollama_response = response.json()
            
            # Convert Ollama response format to match frontend expectations
            chat_response = {
                "choices": [
                    {
                        "message": {
                            "content": ollama_response.get("response", "No response generated")
                        },
                        "finish_reason": "stop"
                    }
                ],
                "model": "deepseek-r1"
            }
            return jsonify(chat_response)
        else:
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Docker Model Runner: {e}")
        # Try to get more details from the response if available
        error_details = "No additional details."
        if e.response is not None:
            try:
                error_details = e.response.json()
            except json.JSONDecodeError:
                error_details = e.response.text
        
        return jsonify({
            "error": "Could not connect to the model runner API.", 
            "details": str(e),
            "response_from_server": error_details
        }), 502

# Main entry point to run the app
if __name__ == '__main__':
    print("Starting Flask server with DeepSeek R1...")
    print("Local access: http://127.0.0.1:5001")
    print("Network access: http://0.0.0.0:5001")
    print("Other devices can connect using your IP address on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
