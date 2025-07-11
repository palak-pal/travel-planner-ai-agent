import requests
import os
import json

class WeatherTool:
    def call(self, location: str, month: str = None) -> str:
        # Use Open-Meteo geocoding and weather API (no API key required)
        try:
            geo = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
            ).json()
            if not geo.get("results"):
                return f"Could not find weather for {location}."
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            
            # Get current weather
            weather = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            ).json()
            temp = weather['current_weather']['temperature']
            wind = weather['current_weather']['windspeed']
            
            result = f"Current temperature: {temp}°C, wind speed: {wind} km/h."
            
            # If month is specified, get seasonal information
            if month:
                month_num = {
                    "january": 1, "february": 2, "march": 3, "april": 4,
                    "may": 5, "june": 6, "july": 7, "august": 8,
                    "september": 9, "october": 10, "november": 11, "december": 12
                }.get(month.lower())
                
                if month_num:
                    # Get historical data for the specified month
                    historical = requests.get(
                        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=2023-{month_num:02d}-01&end_date=2023-{month_num:02d}-28&daily=temperature_2m_mean,precipitation_sum"
                    ).json()
                    
                    if historical.get("daily"):
                        avg_temp = sum(historical["daily"]["temperature_2m_mean"]) / len(historical["daily"]["temperature_2m_mean"])
                        avg_precip = sum(historical["daily"]["precipitation_sum"]) / len(historical["daily"]["precipitation_sum"])
                        
                        result += f"\n{month.title()} average: {avg_temp:.1f}°C, {avg_precip:.1f}mm precipitation."
                        
                        # Add seasonal advice
                        if avg_temp < 10:
                            result += " ❄️ Cold weather - pack warm clothes!"
                        elif avg_temp > 25:
                            result += " ☀️ Hot weather - pack light clothes and stay hydrated!"
                        elif avg_precip > 100:
                            result += " 🌧️ Rainy season - bring umbrella and rain gear!"
                        else:
                            result += " 🌤️ Pleasant weather - perfect for sightseeing!"
            
            return result
        except Exception as e:
            return f"Weather unavailable for {location}."

class AttractionsTool:
    def call(self, location: str) -> str:
        # First try to get data from our dynamic dataset
        try:
            with open("travel_data/traveldata.json", "r", encoding="utf-8") as f:
                city_data = json.load(f)
            
            for city in city_data:
                if city["name"].lower() == location.lower():
                    attractions = city.get("attractions", [])
                    if attractions:
                        result = f"Top attractions in {location}:\n"
                        for i, attraction in enumerate(attractions[:5], 1):
                            rating = attraction.get("rating", "N/A")
                            vicinity = attraction.get("vicinity", "")
                            result += f"  {i}. {attraction['name']} (Rating: {rating}) - {vicinity}\n"
                        return result
        except Exception as e:
            pass
        
        # Fallback to API if not found in dataset
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            # Try to get from Streamlit secrets
            try:
                import streamlit as st
                api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
            except:
                return f"[Demo] Top attractions in {location}: Museum, Park, Historic Site. (Set GOOGLE_MAPS_API_KEY for real data)"
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {"query": f"tourist attractions in {location}", "key": api_key}
            resp = requests.get(url, params=params)
            data = resp.json()
            if not data.get("results"):
                return f"No attractions found for {location}."
            names = [place["name"] for place in data["results"][:5]]
            return f"Top attractions in {location}: {', '.join(names)}."
        except Exception as e:
            return f"Attractions unavailable for {location}."

class TransportationTool:
    def call(self, location: str) -> str:
        # Use Google Maps Places API (requires API key)
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            # Try to get from Streamlit secrets
            try:
                import streamlit as st
                api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
            except:
                return f"[Demo] Transportation options in {location}: Metro, Bus, Taxi, Bike rental. (Set GOOGLE_MAPS_API_KEY for real data)"
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {"query": f"public transport in {location}", "key": api_key}
            resp = requests.get(url, params=params)
            data = resp.json()
            if not data.get("results"):
                return f"No transportation info found for {location}."
            names = [place["name"] for place in data["results"][:3]]
            return f"Transportation options in {location}: {', '.join(names)}."
        except Exception as e:
            return f"Transportation info unavailable for {location}."

class RestaurantTool:
    def call(self, location: str) -> str:
        # First try to get data from our dynamic dataset
        try:
            with open("travel_data/traveldata.json", "r", encoding="utf-8") as f:
                city_data = json.load(f)
            
            for city in city_data:
                if city["name"].lower() == location.lower():
                    restaurants = city.get("restaurants", [])
                    if restaurants:
                        result = f"Popular restaurants in {location}:\n"
                        for i, restaurant in enumerate(restaurants[:5], 1):
                            rating = restaurant.get("rating", "N/A")
                            cuisine = restaurant.get("cuisine", "")
                            result += f"  {i}. {restaurant['name']} (Rating: {rating}) - {cuisine}\n"
                        return result
        except Exception as e:
            pass
        
        # Fallback to API if not found in dataset
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            # Try to get from Streamlit secrets
            try:
                import streamlit as st
                api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
            except:
                return f"[Demo] Popular restaurants in {location}: Local cuisine, International dining. (Set GOOGLE_MAPS_API_KEY for real data)"
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {"query": f"restaurants in {location}", "key": api_key}
            resp = requests.get(url, params=params)
            data = resp.json()
            if not data.get("results"):
                return f"No restaurants found for {location}."
            names = [place["name"] for place in data["results"][:5]]
            return f"Popular restaurants in {location}: {', '.join(names)}."
        except Exception as e:
            return f"Restaurant info unavailable for {location}."

class AccommodationTool:
    def call(self, location: str) -> str:
        # First try to get data from our dynamic dataset
        try:
            with open("travel_data/traveldata.json", "r", encoding="utf-8") as f:
                city_data = json.load(f)
            
            for city in city_data:
                if city["name"].lower() == location.lower():
                    accommodations = city.get("accommodations", [])
                    if accommodations:
                        result = f"Accommodation options in {location}:\n"
                        for i, hotel in enumerate(accommodations[:5], 1):
                            rating = hotel.get("rating", "N/A")
                            hotel_type = hotel.get("type", "")
                            result += f"  {i}. {hotel['name']} (Rating: {rating}) - {hotel_type}\n"
                        return result
        except Exception as e:
            pass
        
        # Fallback to API if not found in dataset
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            # Try to get from Streamlit secrets
            try:
                import streamlit as st
                api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
            except:
                return f"[Demo] Accommodation options in {location}: Hotels, Hostels, Guesthouses. (Set GOOGLE_MAPS_API_KEY for real data)"
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {"query": f"hotels in {location}", "key": api_key}
            resp = requests.get(url, params=params)
            data = resp.json()
            if not data.get("results"):
                return f"No accommodation found for {location}."
            names = [place["name"] for place in data["results"][:5]]
            return f"Accommodation options in {location}: {', '.join(names)}."
        except Exception as e:
            return f"Accommodation info unavailable for {location}."

weather_tool = WeatherTool()
attractions_tool = AttractionsTool()
transportation_tool = TransportationTool()
restaurant_tool = RestaurantTool()
accommodation_tool = AccommodationTool()