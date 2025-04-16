from dotenv import load_dotenv
from flask import Flask, jsonify, request
import json
import os
import requests


# Nominatim OSM API
OSM = "https://nominatim.openstreetmap.org/search"
# OpenRouteServices API
ORS = "https://api.openrouteservice.org/v2/matrix/driving-car"


app = Flask(__name__)


@app.route("/get_coord/<q>")
def get_coordinates(q:str) -> tuple[float, float]:
    """
    Use the Nominatim OSM API to get the coordinates (lat & long)
    of a particular address

    Args:
        q: str
            The full address of a point

    Returns:
        (lat, long) of a point
    """

    user_agent = {"User-Agent": "My User Agent 1.0"} # Nominatim usage policy
    params = {"q": q, "format": "geocodejson",
              "addressdetails": 1, "limit": 1}

    # Make the request
    request = requests.get(OSM, params=params, headers=user_agent)

    output = request.json()

    # Get the coordinates
    coord = tuple( output["features"][0]["geometry"]["coordinates"] )

    return f"{coord}"


@app.route("/get_dist/", methods=["POST"])
def get_distance() -> float:
    """
    Calculate the distances from an origin and destination 
    coordinates by using the OpenRouteServices API.

    Returns:
        float
            Distance
    """
    # Parse the sent JSON.
    coordinates = request.get_json(force=True, silent=True)
    if not coordinates:
        return jsonify({
            "status": 400,
            "message": "Invalid json in request body"
        })
    
    # Get the coordinates of origin and destination
    coord_1, coord_2 = coordinates.get("origin"), coordinates.get("destination")

    # Build the query
    load_dotenv()
    
    body = {"locations":[coord_1,coord_2],"metrics":["distance"]}

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": os.getenv("API_KEY"),
        "Content-Type": "application/json; charset=utf-8"
    }
    call = requests.post(ORS, json=body, headers=headers)

    # Get the distance
    response = json.loads(call.text)
    distance = response["distances"][0][1] # from 1 to 2

    return f"{distance}"