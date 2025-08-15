# app.py

# 1. Import necessary libraries
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# 2. Load environment variables from .env file
load_dotenv()

# 3. Initialize the Flask app
app = Flask(__name__)

# 4. Middleware setup
# Enable Cross-Origin Resource Sharing (CORS) for all routes
# This allows your frontend to make requests to this server
CORS(app)

# 5. Define the API endpoint for weather
@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        # 6. Get the API key from environment variables (the secure part)
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            # If the API key is missing on the server, return an error
            return jsonify({"message": "Server configuration error: API key is missing."}), 500

        # 7. Construct the OpenWeatherMap API URL with query params from the frontend
        # The request arguments (like 'q', 'lat', 'lon') are in request.args
        params = {**request.args, 'appid': api_key}
        
        # 8. Make the request to the OpenWeatherMap API
        url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params=params)
        
        # This will raise an exception for bad responses (4xx or 5xx)
        response.raise_for_status() 

        # 9. Send the data from OpenWeatherMap back to our frontend
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        # 10. Error handling for failed API calls
        # Extract error message from OpenWeatherMap's response if possible
        error_data = http_err.response.json()
        message = error_data.get("message", "An error occurred fetching weather data.")
        return jsonify({"message": message}), http_err.response.status_code
        
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"message": f"An internal server error occurred: {e}"}), 500

# 11. Run the server
if __name__ == '__main__':
    # Use port from environment or default to 3001
    port = int(os.getenv('PORT', 3001))
    app.run(host='0.0.0.0', port=port, debug=True)

