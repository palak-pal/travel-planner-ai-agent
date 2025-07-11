from sentence_transformers import SentenceTransformer
import faiss
import json
import os

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Enhanced RAG KB from dynamic data ---
def load_knowledge_base():
    data_file = "travel_data/traveldata.json"
    if not os.path.exists(data_file):
        print(f"⚠️  Dynamic data file not found: {data_file}")
        print("📝 Using fallback data from destinations.json")
        data_file = "data/destinations.json"
    
    with open(data_file, encoding="utf-8") as f:
        destinations = json.load(f)
    
    knowledge_base = []
    city_data_map = {}
    
    if data_file == "travel_data/traveldata.json":
        # Process dynamic data structure
        for dest in destinations:
            name = dest.get("name", "")
            desc = dest.get("description", "")
            
            # Create comprehensive knowledge entry
            knowledge_entry = f"{name}: {desc}"
            
            # Add attractions if available
            if dest.get("attractions"):
                attractions = [a.get("name", "") for a in dest["attractions"][:5]]
                knowledge_entry += f" Top attractions: {', '.join(attractions)}."
            
            # Add restaurants if available
            if dest.get("restaurants"):
                restaurants = [r.get("name", "") for r in dest["restaurants"][:3]]
                knowledge_entry += f" Popular restaurants: {', '.join(restaurants)}."
            
            # Add accommodations if available
            if dest.get("accommodations"):
                hotels = [h.get("name", "") for h in dest["accommodations"][:3]]
                knowledge_entry += f" Accommodation options: {', '.join(hotels)}."
            
            knowledge_base.append(knowledge_entry)
            city_data_map[name] = dest
    else:
        # Fallback to original structure
        for dest in destinations:
            knowledge_entry = f"{dest['name']}: {dest['description']}"
            knowledge_base.append(knowledge_entry)
            city_data_map[dest['name']] = dest
    
    return knowledge_base, city_data_map

knowledge_base, city_data_map = load_knowledge_base()

kb_embeddings = embedding_model.encode(knowledge_base)
kb_index = faiss.IndexFlatL2(kb_embeddings.shape[1])
kb_index.add(kb_embeddings)

def rag_follow_up(state):
    selected_city = state["selected_city"]
    query_vec = embedding_model.encode([selected_city])
    D, I = kb_index.search(query_vec, k=1)
    
    print(f"\n📚 Enhanced Information for {selected_city}:")
    print(f"📖 {knowledge_base[I[0][0]]}")
    
    # Provide additional structured information if available
    if selected_city in city_data_map:
        city_data = city_data_map[selected_city]
        
        if city_data.get("attractions"):
            print(f"\n🏛️  Top Attractions:")
            for i, attraction in enumerate(city_data["attractions"][:5], 1):
                rating = attraction.get("rating", "N/A")
                vicinity = attraction.get("vicinity", "")
                print(f"  {i}. {attraction['name']} (Rating: {rating}) - {vicinity}")
        
        if city_data.get("restaurants"):
            print(f"\n🍽️  Popular Restaurants:")
            for i, restaurant in enumerate(city_data["restaurants"][:3], 1):
                rating = restaurant.get("rating", "N/A")
                cuisine = restaurant.get("cuisine", "")
                print(f"  {i}. {restaurant['name']} (Rating: {rating}) - {cuisine}")
        
        if city_data.get("accommodations"):
            print(f"\n🏨 Accommodation Options:")
            for i, hotel in enumerate(city_data["accommodations"][:3], 1):
                rating = hotel.get("rating", "N/A")
                hotel_type = hotel.get("type", "")
                print(f"  {i}. {hotel['name']} (Rating: {rating}) - {hotel_type}")
    
    return state