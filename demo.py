import requests
import json
import os
import time
from datetime import datetime

# --- Configuration ---
# WARNING: NEVER HARDCODE API KEYS IN PRODUCTION CODE.
# Use environment variables (e.g., os.getenv("GOOGLE_PLACES_API_KEY"))
# For demonstration purposes, we're using the provided key.
GOOGLE_MAPS_API_KEY = "AIzaSyBUHqCpupMaG_qPwayW35nfTjMnWQi1bF8"
# You'd also need an API key for a weather service, e.g., OpenWeatherMap
OPENWEATHER_API_KEY = "c7dde16d4a66ba53f9014d43d888faca" # Replace with your actual key if using

# --- Helper Functions (Simulated External API Calls/Data Fetching) ---
# In a real system, these would make actual HTTP requests to APIs.
# For this demonstration, they return sample/dummy data.

def fetch_city_overview_from_source(city_name, country_name):
    """
    Simulates fetching a general overview of a city from a source like Wikipedia or a travel guide API.
    In a real scenario, this would involve parsing API responses from an authoritative source.
    """
    print(f"  > Simulating fetch of overview for {city_name}, {country_name}...")
    # Example: You might use Wikipedia API or a dedicated travel content API here.
    # For demonstration, returning a hardcoded sample.
    sample_data = {
        "Kyoto, Japan": {
            "description": "Kyoto, Japan's ancient capital, is renowned for its serene temples and traditional gardens. The iconic Kinkaku-ji (Golden Pavilion) gleams on a pond, offering a breathtaking sight. The city boasts exquisite geisha districts, preserving a unique cultural heritage. Traditional tea ceremonies and kaiseki cuisine provide enriching cultural experiences. From bamboo forests to meticulously crafted gardens, Kyoto offers a tranquil escape into Japan's rich past.",
            "major_landmarks_raw": ["Kinkaku-ji", "Fushimi Inari-taisha", "Kiyomizu-dera", "Arashiyama Bamboo Grove", "Gion District", "Nijo Castle"],
            "known_cuisine_raw": ["Kaiseki", "Matcha", "Yuba (Tofu Skin)", "Kyoto Vegetables", "Sake"],
            "location_coords": {"lat": 35.0116, "lng": 135.7681},
            "continent": "Asia"
        },
        "Paris, France": {
            "description": "Paris, the City of Lights, is a global center for art, fashion, and gastronomy. The Eiffel Tower, an iconic symbol of France, offers panoramic views of the city. The Louvre Museum houses masterpieces of Western art, including the Mona Lisa. Charming cafes and bistros line the streets, offering delicious pastries and coffee. The Seine River winds its way through the city, offering picturesque boat rides. Paris's rich history and vibrant culture make it an unforgettable destination.",
            "major_landmarks_raw": ["Eiffel Tower", "Louvre Museum", "Notre Dame Cathedral", "Arc de Triomphe", "Champs-Élysées", "Montmartre"],
            "known_cuisine_raw": ["Croissants", "Baguettes", "Macarons", "Steak Frites", "French Cheese", "Escargots"],
            "location_coords": {"lat": 48.8566, "lng": 2.3522},
            "continent": "Europe"
        },
        "New York City, USA": {
            "description": "New York City, a global hub of finance, culture, and entertainment, is known for its iconic skyline. Times Square, a dazzling display of lights and billboards, is a must-see. Central Park offers a tranquil escape in the middle of the bustling city. The city's diverse culinary scene offers a wide range of cuisines from around the world. From Broadway shows to world-class museums, NYC offers endless entertainment options. The city's energy and diversity are truly captivating.",
            "major_landmarks_raw": ["Statue of Liberty", "Empire State Building", "Times Square", "Central Park", "Broadway", "Metropolitan Museum of Art"],
            "known_cuisine_raw": ["New York-style Pizza", "Bagels", "Cheesecake", "Hot Dogs", "Diverse International Cuisine"],
            "location_coords": {"lat": 40.7128, "lng": -74.0060},
            "continent": "North America"
        }
    }
    return sample_data.get(f"{city_name}, {country_name}", None)

def fetch_weather_climate_data(city_coords):
    """
    Simulates fetching current and historical weather data.
    In a real scenario, this would use a weather API like OpenWeatherMap.
    """
    print(f"  > Simulating fetch of weather for coords {city_coords['lat']},{city_coords['lng']}...")
    # Example API call (commented out for simulation):
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={city_coords['lat']}&lon={city_coords['lng']}&appid={OPENWEATHER_API_KEY}&units=metric"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     print(f"    ! Weather API error: {response.status_code}")
    #     return None

    # Simulated data based on July 2025 context
    return {
        "current_temp_c": 32,
        "current_condition": "Rainy",
        "feels_like_c": 33,
        "uv_index": "low",
        "avg_temp_july_c": 28,
        "avg_rain_days_july": 15,
        "season_notes_july": "Hot and humid with frequent rain showers. Typhoon season risk.",
        "sunrise_july": "05:00 AM",
        "sunset_july": "07:00 PM"
    }

# --- Real Google Places API Fetch ---
def fetch_pois_from_google_places(city_name, country_name, poi_type, api_key, max_results=10):
    results = []
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={poi_type}+in+{city_name}+{country_name}&key={api_key}"
    )
    while url and len(results) < max_results:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results.extend(data.get('results', []))
            next_page_token = data.get('next_page_token')
            if next_page_token:
                time.sleep(2)
                url = (
                    f"https://maps.googleapis.com/maps/api/place/textsearch/json"
                    f"?pagetoken={next_page_token}&key={api_key}"
                )
            else:
                break
        else:
            print(f"API error: {response.status_code}")
            break
    return results[:max_results]

# --- Data Processing and Tagging Logic ---

def map_google_price_level_to_budget_tier(price_level_int):
    """Maps Google Places API integer price levels to our budget tiers."""
    if price_level_int == 4: # Very Expensive
        return ["high"]
    elif price_level_int == 3: # Expensive
        return ["medium", "high"]
    elif price_level_int == 2: # Moderate
        return ["low", "medium"]
    elif price_level_int == 1: # Inexpensive
        return ["low"]
    return ["low", "medium", "high"] # Default if no price level or unknown

def map_poi_types_to_interests(poi_types, name=""):
    """
    Maps Google Places API 'types' to our standardized interest categories.
    This is a simplification; a real system would have a more extensive and nuanced mapping.
    """
    interests = set()
    type_map = {
        "museum": "art", "art_gallery": "art", "gallery": "art",
        "historical_landmark": "history", "church": "history", "hindu_temple": "history", "mosque": "history", "synagogue": "history", "temple": "history", "shrine": "history", "castle": "history",
        "park": "nature", "garden": "nature", "zoo": "nature", "aquarium": "nature", "natural_feature": "nature", "tourist_attraction": "nature", # Broad for nature if it's a natural attraction
        "restaurant": "food", "cafe": "food", "bakery": "food", "bar": "food", "food": "food",
        "shopping_mall": "shopping", "store": "shopping", "market": "shopping", "boutique": "shopping",
        "night_club": "nightlife", "bar": "nightlife", # Can be both food and nightlife
        "spa": "relaxation", "lodging": "relaxation", # Lodging implies relaxation
        "university": "education", "library": "education"
    }
    for t in poi_types:
        if t in type_map:
            interests.add(type_map[t])
    
    # Add some manual rules for common cases or to refine based on name
    if "bamboo" in name.lower() or "forest" in name.lower() or "mountain" in name.lower():
        interests.add("nature")
        interests.add("outdoor")
    if "kaiseki" in name.lower() or "fine dining" in name.lower():
        interests.add("fine_dining")
        interests.add("food") # Ensure 'food' is also added
        interests.add("culture")
    if "traditional" in name.lower() or "craft" in name.lower():
        interests.add("traditional_crafts")
        interests.add("culture")
    if "river" in name.lower() or "boat" in name.lower():
        interests.add("nature")
        interests.add("scenic_views")
    if "walking" in name.lower() or "stroll" in name.lower():
        interests.add("walking")
        interests.add("outdoor")
    if "museum" in name.lower() and "interactive" in name.lower():
        interests.add("family") # Example for family-friendly interest
    if "on-sen" in name.lower() or "onsen" in name.lower():
        interests.add("relaxation")

    # Add broad categories if specific ones are missing but implied
    if any(i in ["history", "art", "religious_sites", "traditional_crafts"] for i in interests):
        interests.add("culture")
    if any(i in ["hiking", "cycling", "water_sports"] for i in interests):
        interests.add("adventure")

    return list(interests)

def generate_city_data(city_name, country_name, country_code):
    """
    Generates a structured data entry for a single city by combining various data sources.
    This is the core function for building one entry of your 1000-city database.
    """
    print(f"Generating data for {city_name}, {country_name}...")
    city_data = {
        "name": f"{city_name}, {country_name}",
        "country": country_name,
        "country_code": country_code,
        "continent": "", # Will be populated from overview_data
        "description": "",
        "keywords": [], # General keywords derived from content
        "iconic_landmarks": [], # Key landmarks with brief descriptions
        "culinary_highlights": [], # Specific dishes/cuisine types
        "unique_experiences": [], # Experiences not easily categorized as standard POIs
        "best_time_to_visit": {}, # Climate and seasonal notes
        "average_budget_tiers": { # General cost estimates for each tier
            "low": "",
            "medium": "",
            "high": ""
        },
        "travel_tips": [], # General advice for the city
        "airport_codes": [], # Relevant airport codes
        "attractions": [], # List of detailed attractions
        "restaurants": [], # List of detailed restaurants
        "accommodations": [], # List of detailed accommodations
        "last_updated": datetime.now().isoformat()
    }

    # 1. Fetch general overview (e.g., from Wikipedia/travel guide)
    overview_data = fetch_city_overview_from_source(city_name, country_name)
    if overview_data:
        city_data["description"] = overview_data.get("description", "")
        city_data["continent"] = overview_data.get("continent", "Unknown")
        city_data["location_coords"] = overview_data.get("location_coords")
        
        # Initial population of iconic landmarks from raw data
        for landmark_name in overview_data.get("major_landmarks_raw", []):
            city_data["iconic_landmarks"].append({
                "name": landmark_name,
                "description": f"An iconic landmark in {city_name}.", # Placeholder, would be refined by LLM/human
                "interests": map_poi_types_to_interests(["tourist_attraction"], landmark_name) # Basic tagging
            })
        city_data["culinary_highlights"] = overview_data.get("known_cuisine_raw", [])
        # Generate initial keywords from raw data
        city_data["keywords"].extend([k.lower() for k in overview_data.get("major_landmarks_raw", [])])
        city_data["keywords"].extend([k.lower() for k in overview_data.get("known_cuisine_raw", [])])
        city_data["keywords"] = list(set(city_data["keywords"])) # Remove duplicates

    # 2. Fetch weather/climate data
    if city_data.get("location_coords"):
        weather_info = fetch_weather_climate_data(city_data["location_coords"])
        if weather_info:
            city_data["best_time_to_visit"] = {
                "season_notes": weather_info.get("season_notes_july", "Varies by season."),
                "avg_temp_c_july": weather_info.get("avg_temp_july_c"),
                "avg_rain_days_july": weather_info.get("avg_rain_days_july"),
                "sunrise_july": weather_info.get("sunrise_july"),
                "sunset_july": weather_info.get("sunset_july")
            }

    # 3. Fetch POIs (Attractions, Restaurants, Accommodations) from Places API
    # --- Attractions ---
    attraction_results = fetch_pois_from_google_places(city_name, country_name, "tourist attraction", GOOGLE_MAPS_API_KEY)
    for item in attraction_results:
        city_data["attractions"].append({
            "name": item.get("name"),
            "place_id": item.get("place_id"),
            "description": "", # To be enriched later
            "rating": item.get("rating"),
            "price_level_google": item.get("price_level"), # Keep raw Google price level
            "budget_suitability": map_google_price_level_to_budget_tier(item.get("price_level", 2)), # Default to moderate
            "interests": map_poi_types_to_interests(item.get("types", []), item.get("name")),
            "type": "attraction",
            "vicinity": item.get("vicinity"),
            "opening_hours_info": item.get("opening_hours", {}) # Store raw opening hours data
        })

    # --- Restaurants ---
    restaurant_results = fetch_pois_from_google_places(city_name, country_name, "restaurant", GOOGLE_MAPS_API_KEY)
    for item in restaurant_results:
        city_data["restaurants"].append({
            "name": item.get("name"),
            "place_id": item.get("place_id"),
            "cuisine": ", ".join([t for t in item.get("types", []) if t != "restaurant" and t != "point_of_interest" and t != "establishment"]), # Extract specific cuisine types
            "rating": item.get("rating"),
            "price_level_google": item.get("price_level"),
            "budget_suitability": map_google_price_level_to_budget_tier(item.get("price_level", 2)),
            "interests": map_poi_types_to_interests(item.get("types", []), item.get("name")),
            "type": "dining",
            "vicinity": item.get("vicinity"),
            "opening_hours_info": item.get("opening_hours", {})
        })

    # --- Accommodations ---
    lodging_results = fetch_pois_from_google_places(city_name, country_name, "hotel", GOOGLE_MAPS_API_KEY)
    for item in lodging_results:
        city_data["accommodations"].append({
            "name": item.get("name"),
            "place_id": item.get("place_id"),
            "type": ", ".join([t for t in item.get("types", []) if t != "lodging" and t != "point_of_interest" and t != "establishment"]),
            "rating": item.get("rating"),
            "price_level_google": item.get("price_level"),
            "budget_suitability": map_google_price_level_to_budget_tier(item.get("price_level", 2)),
            "interests": map_poi_types_to_interests(item.get("types", []), item.get("name")), # Will include "relaxation" etc.
            "vicinity": item.get("vicinity"),
            "opening_hours_info": item.get("opening_hours", {})
        })

    # 4. Human-in-the-loop / LLM Enrichment (Post-processing on fetched data)
    # This is the critical step for adding the "high-quality", "non-dummy" details
    # that automated API fetches alone might miss or provide generically.
    # In a real system, this would be a separate process, potentially involving:
    # - More detailed API calls (e.g., Google Places Details API for full descriptions)
    # - LLM calls to generate engaging descriptions based on raw data
    # - Human editors to review, refine, add unique insights, and verify.

    # Example of specific enrichment for Kyoto (based on previous detailed output)
    if city_name == "Kyoto":
        city_data["unique_experiences"].extend([
            {"name": "Private Tea Ceremony with Master", "budget_suitability": ["high"], "interests": ["culture", "traditional_crafts", "relaxation"], "notes": "An intimate, authentic experience."},
            {"name": "Maiko/Geiko Dinner Experience", "budget_suitability": ["high"], "interests": ["culture", "performing_arts", "food", "nightlife"], "notes": "Exclusive dinner with traditional entertainment."},
            {"name": "Kyo-yuzen Dyeing Workshop", "budget_suitability": ["medium", "high"], "interests": ["culture", "traditional_crafts", "art"], "notes": "Hands-on experience with traditional silk dyeing."},
            {"name": "Hozugawa River Boat Ride", "budget_suitability": ["medium", "high"], "interests": ["nature", "adventure", "scenic_views"], "notes": "Scenic river journey from Kameoka to Arashiyama (seasonal)."}
        ])
        city_data["average_budget_tiers"] = {
            "low": "¥5,000 - ¥10,000 per day (hostel/guesthouse, street food/convenience, public transport)",
            "medium": "¥15,000 - ¥30,000 per day (3-4 star hotel, mid-range restaurants, mix of public/taxi)",
            "high": "¥40,000 - ¥100,000+ per day (luxury hotel/ryokan, fine dining, private transport)"
        }
        city_data["travel_tips"].extend([
            "Purchase an ICOCA card for easy public transport.",
            "Book accommodation and popular restaurants well in advance, especially during peak season.",
            "Respect local customs and dress codes at temples and shrines.",
            "Carry some cash for smaller shops and eateries.",
            "Be mindful of noise levels in residential areas, especially in Gion.",
            "Consider a private car for convenience if on a high budget."
        ])
        city_data["airport_codes"].append("KIX")
    elif city_name == "Paris":
         city_data["unique_experiences"].extend([
            {"name": "Private Seine River Dinner Cruise", "budget_suitability": ["high"], "interests": ["food", "relaxation", "romance", "scenic_views"], "notes": "Gourmet dining with iconic landmark views."},
            {"name": "Macaron Baking Class", "budget_suitability": ["medium", "high"], "interests": ["food", "traditional_crafts"], "notes": "Learn to make classic French pastries."},
            {"name": "Montmartre Walking Tour (Art & History)", "budget_suitability": ["low", "medium"], "interests": ["art", "history", "culture", "walking"], "notes": "Explore the artistic heart of Paris."}
        ])
         city_data["average_budget_tiers"] = {
            "low": "€50 - €100 per day (hostel/budget hotel, street food/bakeries, metro)",
            "medium": "€150 - €300 per day (3-4 star hotel, bistros, mix of metro/taxi)",
            "high": "€400 - €1000+ per day (luxury hotel, Michelin dining, private car)"
        }
         city_data["travel_tips"].extend([
            "Utilize the extensive Metro system for efficient travel.",
            "Book popular attractions (Louvre, Eiffel Tower) tickets online in advance to save time.",
            "Be aware of pickpockets in crowded tourist areas.",
            "Learn a few basic French phrases (Bonjour, Merci, S'il vous plaît).",
            "Many museums offer free entry on the first Sunday of the month (check specific dates)."
        ])
         city_data["airport_codes"].extend(["CDG", "ORY"])


    print(f"Data generation for {city_name} complete.")
    return city_data

# --- Main Execution Loop (for all cities in destinations.json) ---
def main():
    with open('data/destinations.json', encoding='utf-8') as f:
        destinations = json.load(f)
    all_cities_data = []
    for i, dest in enumerate(destinations):
        # Split city and country
        if ',' in dest['name']:
            city, country = [x.strip() for x in dest['name'].split(',', 1)]
        else:
            city = dest['name'].strip()
            country = ''
        print(f"Processing {i+1}/{len(destinations)}: {city}, {country}")
        city_data = {
            "name": dest['name'],
            "country": country,
            "description": dest.get('description', ''),
            "attractions": [],
            "restaurants": [],
            "accommodations": []
        }
        # Fetch real data
        city_data["attractions"] = fetch_pois_from_google_places(city, country, "tourist attraction", GOOGLE_MAPS_API_KEY)
        city_data["restaurants"] = fetch_pois_from_google_places(city, country, "restaurant", GOOGLE_MAPS_API_KEY)
        city_data["accommodations"] = fetch_pois_from_google_places(city, country, "hotel", GOOGLE_MAPS_API_KEY)
        all_cities_data.append(city_data)
        # Save progress every 10 cities
        if (i+1) % 10 == 0:
            with open('travel_data/traveldata.json', 'w', encoding='utf-8') as f:
                json.dump(all_cities_data, f, ensure_ascii=False, indent=2)
        time.sleep(1)  # Respect API quota
    # Final save
    with open('travel_data/traveldata.json', 'w', encoding='utf-8') as f:
        json.dump(all_cities_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

