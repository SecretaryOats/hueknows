from flask import Flask, request, jsonify
import cv2
import numpy as np
from sklearn.cluster import KMeans
import colormath.color_objects as co

app = Flask(__name__)

def extract_dominant_colors(image_bytes, num_colors=5):
    # Load image from bytes
    image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Convert to RGB and reshape
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)

    # KMeans clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)

    return dominant_colors

def classify_color(color):
    # Classify color based on RGB values
    r, g, b = color

    if 0 <= r <= 180 and 0 <= g <= 175 and 27 <= b <= 200:
        season_type = "Winter"
    elif 50 <= r <= 255 and 50 <= g <= 255 and 46 <= b <= 235:
        season_type = "Spring"
    elif 10 >= r >= 224 and 10 >= g >= 200 and 0 >= b >= 185:
        season_type = "Autumn"
    elif 0 <= r <= 255 and 0 <= g <= 237 and 0 <= b <= 255:
        season_type = "Summer"
    else:
        season_type = "Neutral"

    saturation = (np.max(color) - np.min(color)) / 255.0
    if saturation > 0.5:
        saturation_level = "Saturated"
    else:
        saturation_level = "Desaturated"

    if 180 <= r <= 225 and 0 <= g <= 175 and 50 <= b <= 150:
        temperature = "Warm"
    elif 50 <= r <= 184 and 60 <= g <= 250 and 100 <= b <= 120:
        temperature = "Cool"
    else:
        temperature = "Neutral"

    return season_type, saturation_level, temperature

def color_analysis(image_bytes):
    dominant_colors = extract_dominant_colors(image_bytes)

    classifications = []
    for color in dominant_colors:
        season_type, saturation_level, temperature = classify_color(color)
        classifications.append({
            'color': color.tolist(),  # Convert to list for JSON
            'season_type': season_type,
            'saturation_level': saturation_level,
            'temperature': temperature
        })

    return classifications

def generate_complementary_palette(classifications):
    complementary_palette = []

    for classification in classifications:
        color = classification['color']
        season_type = classification['season_type']
        saturation_level = classification['saturation_level']
        temperature = classification['temperature']

        # Generate complementary colors based on season type
        if season_type == "Winter":
            complementary_color = [255 - color[0], 255 - color[1], 255 - color[2]]
        elif season_type == "Spring":
            complementary_color = [255 - color[0], color[1], color[2]]
        elif season_type == "Autumn":
            complementary_color = [color[0], 255 - color[1], 255 - color[2]]
        elif season_type == "Summer":
            complementary_color = [color[0], color[1], 255 - color[2]]

        # Adjust complementary color based on saturation and temperature
        if saturation_level == "Desaturated":
            complementary_color = [c * 0.75 for c in complementary_color]
        if temperature == "Warm":
            complementary_color[0] = min(255
