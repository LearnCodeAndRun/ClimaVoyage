from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "694c6f9df89503cf8e2f3da1425cd84c"

# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def home():
    return render_template("../../frontend/templates/index.html")

# ---------------------------
# City Search (Autocomplete)
# ---------------------------
@app.route("/search-city")
def search_city():
    query = request.args.get("q")

    if not query or len(query) < 2:
        return jsonify([])

    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": query,
        "limit": 5,
        "appid": API_KEY
    }

    response = requests.get(url)
    data = response.json()

    cities = []
    for city in data:
        cities.append({
            "name": city["name"],
            "state": city.get("state", ""),
            "country": city["country"],
            "lat": city["lat"],
            "lon": city["lon"]
        })

    return jsonify(cities)

# ---------------------------
# Weather by Latitude & Longitude
# ---------------------------
@app.route("/weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude required"}), 400

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": API_KEY
    }

    response = requests.get(url)
    data = response.json()

    weather_info = {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "city": data["name"]
    }

    return jsonify(weather_info)

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
