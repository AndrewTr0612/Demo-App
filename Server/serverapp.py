# Save this file as app.py
from flask import Flask, request, jsonify, send_from_directory
import requests
import json

app = Flask(__name__)

# Route to serve the main HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route to act as a proxy for the Docker Model Runner
@app.route('/api/chat', methods=['POST'])
def proxy_chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is missing"}), 400

    # --- THIS IS THE CORRECTED URL ---
    # The Docker Model Runner API requires specifying the engine in the path.
    docker_api_url = 'http://localhost:12434/engines/llama.cpp/v1/chat/completions'
    
    payload = {
        "model": "ai/deepseek-r1-distill-llama",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        print(f"\nSending POST request to the correct URL: {docker_api_url}")
        response = requests.post(docker_api_url, json=payload)
        response.raise_for_status()  # This will raise an error for 4xx or 5xx responses
        
        print("Successfully received response from model!")
        return jsonify(response.json())

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
    print("Starting Flask server with corrected API URL...")
    print("Open your browser and go to http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
