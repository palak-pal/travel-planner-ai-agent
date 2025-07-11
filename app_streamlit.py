# Import warnings configuration first
import warnings_config

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os

from planner.tools import weather_tool, attractions_tool, transportation_tool, restaurant_tool, accommodation_tool

st.set_page_config(page_title="AI Travel Planner", page_icon="🌟", layout="centered")

# Initialize LLM with caching
@st.cache_resource
def get_llm():
    # Get API key from environment or Streamlit secrets
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        # Try to get from Streamlit secrets
        try:
            api_key = st.secrets["GOOGLE_GEMINI_API_KEY"]
        except:
            st.error("❌ Google Gemini API key not found! Please set GOOGLE_GEMINI_API_KEY in environment variables or Streamlit secrets.")
            st.stop()
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=api_key,
        temperature=0.5
    )

# Helper to check data availability
def check_data_availability():
    dynamic_data_file = "travel_data/traveldata.json"
    fallback_data_file = "data/destinations.json"
    if os.path.exists(dynamic_data_file):
        return True, dynamic_data_file
    elif os.path.exists(fallback_data_file):
        return True, fallback_data_file
    else:
        return False, None

# Optimized destination loading with better caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_destination_data():
    """Load destination data without embeddings - much faster"""
    data_ok, data_file = check_data_availability()
    if not data_ok:
        return None, None
    
    # Load data
    with open(data_file, encoding="utf-8") as f:
        destinations = json.load(f)
    
    # Process data based on structure
    if data_file == "travel_data/traveldata.json":
        # Dynamic data structure
        names = [dest.get("name", "") for dest in destinations]
        descriptions = []
        for dest in destinations:
            desc = dest.get("description", "")
            
            # Enhance description with additional data if available
            if dest.get("attractions"):
                attractions = [a.get("name", "") for a in dest["attractions"][:3]]
                desc += f" Popular attractions: {', '.join(attractions)}."
            
            if dest.get("restaurants"):
                restaurants = [r.get("name", "") for r in dest["restaurants"][:2]]
                desc += f" Notable dining: {', '.join(restaurants)}."
            
            if dest.get("accommodations"):
                hotels = [h.get("name", "") for h in dest["accommodations"][:2]]
                desc += f" Accommodation options: {', '.join(hotels)}."
            
            descriptions.append(desc)
    else:
        # Fallback structure
        descriptions = [d["description"] for d in destinations]
        names = [d["name"] for d in destinations]
    
    return names, descriptions

# Lazy loading of embeddings - only when needed
@st.cache_resource
def get_embedding_model():
    """Get embedding model only when needed"""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

@st.cache_data(ttl=3600)
def create_embeddings(descriptions):
    """Create embeddings with caching"""
    embedding_model = get_embedding_model()
    return embedding_model.encode(descriptions)

@st.cache_data(ttl=3600)
def create_faiss_index(embeddings):
    """Create FAISS index with caching"""
    import faiss
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def suggest_destinations_streamlit(interests, budget, destination_names, descriptions):
    """Streamlit-compatible destination suggestion with lazy loading"""
    # Only load embeddings when needed
    embeddings = create_embeddings(descriptions)
    index = create_faiss_index(embeddings)
    
    query = ' '.join(interests)
    embedding_model = get_embedding_model()
    query_vec = embedding_model.encode([query])
    D, I = index.search(query_vec, k=8)
    
    # Filter by budget
    if budget == "low":
        idxs = I[0][:3]
    elif budget == "high":
        idxs = I[0][-3:]
    else:
        idxs = I[0][2:5]
    
    suggestions = [destination_names[i] for i in idxs]
    return suggestions

def create_itinerary_streamlit(city, interests, duration, budget, travel_month=None):
    """Streamlit-compatible itinerary generation"""
    llm = get_llm()
    
    itinerary_prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are an ultra-premium luxury travel assistant, specializing in crafting immersive, tailor-made itineraries.

**Client Profile:**
- Destination: {city}
- Number of days: {duration}
- Budget: {budget} (low, medium, high)
- Interests: {interests}
- Season/Starting month: {starting_month}

**Your mission:**
Develop a meticulously detailed, hour-by-hour, {duration}-day itinerary covering:
- Morning, lunch, afternoon, and evening plans for each day
- Curated mix of history, fun, food, and adventure activities
- Exclusive recommendations: luxury hotels, signature dining, private tours, unique local experiences
- Add seasonal context: typical weather and festivals during {starting_month}

**Additionally, provide:**
- 📍 2–3 hotel suggestions (with pros/cons) based on {budget}
- 🍽 Must-try foods & local drinks
- 🛍 Shopping list
- 🧳 Packing list tailored to weather & cultural etiquette
- 💡 Local etiquette & cultural tips
- 🎩 Exclusive, off-the-beaten-path experiences
- 💰 Budget allocation tips: how to spend smartly for maximum luxury
- 🔒 Insider travel hacks & VIP access ideas
- 🚖 Transport options: chauffeur, private car, premium ride-sharing
- 🧠 Smart local apps to download

**Format:**
- Use bullet points & clear day headings: e.g., **Day 1: Arrival & Sunset Welcome**
- For each day: include time slots (e.g., 08:00–10:00), activity details, venue names, signature dishes, and why it's unique
- Keep the tone: professional, sophisticated, aspirational

**If budget is 'high':**
- Suggest hyper-exclusive extras (yacht charter, helicopter tour, after-hours museum tour, bespoke tastings)

Finish with a **Trip Summary** section:
- Destination, number of days, interests, weather, top highlights

**Goal:** Create an itinerary so compelling, personalized, and luxury-focused that it feels like a private travel designer curated it just for the user.
        """),
        ("human", "Kindly generate the complete luxury itinerary, including packing guide, budgeting tips, and exclusive local insights.")
    ])
    
    response = llm.invoke(itinerary_prompt.format_messages(
        city=city,
        interests=', '.join(interests),
        duration=duration,
        budget=budget,
        starting_month=travel_month or "your travel month"
    ))
    
    return response.content

st.title("🌟 AI Travel Planner - Professional Edition")
st.markdown("""
Your personal AI travel assistant powered .\
Enhanced with dynamic data from Google Places API.\
Professional itinerary planning with real-time information.
""")

# Load destinations efficiently
destination_names, descriptions = load_destination_data()
if destination_names is None:
    st.error("No data files found! Please run demo.py or add a destinations file.")
    st.stop()

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'state' not in st.session_state:
    st.session_state.state = {
        "messages": [],
        "budget": "",
        "duration": "",
        "interests": [],
        "travel_month": "",
        "suggestions": [],
        "selected_city": "",
        "itinerary": "",
    }

# Sidebar for progress
st.sidebar.header("Planning Progress")
steps = ["Trip Idea", "Budget", "Duration", "Interests", "Travel Month", "Destination", "Itinerary"]
for i, step in enumerate(steps):
    if i <= st.session_state.step:
        st.sidebar.success(f"✅ {step}")
    else:
        st.sidebar.info(f"⏳ {step}")

# Step 1: Trip Idea
if st.session_state.step == 0:
    st.subheader("Step 1: Tell us about your trip")
    user_request = st.text_input("Describe your trip idea:", value="I want to plan a trip")
    if st.button("Start Planning"):
        st.session_state.state["messages"] = [HumanMessage(content=user_request)]
        st.session_state.step = 1
        st.rerun()

# Step 2: Budget
elif st.session_state.step == 1:
    st.subheader("Step 2: Select your budget")
    budget = st.selectbox("Budget level:", ["low", "medium", "high"])
    budget_descriptions = {
        "low": "Budget-friendly options, hostels, street food, public transport",
        "medium": "Mid-range hotels, mix of dining options, some private transport",
        "high": "Luxury accommodations, fine dining, private tours, premium experiences"
    }
    st.info(budget_descriptions[budget])
    if st.button("Continue"):
        st.session_state.state["budget"] = budget
        st.session_state.state["messages"].append(HumanMessage(content=budget))
        st.session_state.step = 2
        st.rerun()

# Step 3: Duration
elif st.session_state.step == 2:
    st.subheader("Step 3: How long is your trip?")
    duration = st.number_input("Number of days:", min_value=1, max_value=60, value=5)
    if st.button("Continue"):
        st.session_state.state["duration"] = str(duration)
        st.session_state.state["messages"].append(HumanMessage(content=str(duration)))
        st.session_state.step = 3
        st.rerun()

# Step 4: Interests
elif st.session_state.step == 3:
    st.subheader("Step 4: What are your interests?")
    st.write("Examples: history, food, nature, art, adventure, culture, shopping, nightlife")
    interests = st.text_input("Your interests (comma-separated):")
    if st.button("Continue") and interests:
        interest_list = [i.strip() for i in interests.split(",") if i.strip()]
        st.session_state.state["interests"] = interest_list
        st.session_state.state["messages"].append(HumanMessage(content=", ".join(interest_list)))
        st.session_state.step = 4
        st.rerun()

# Step 5: Travel Month
elif st.session_state.step == 4:
    st.subheader("Step 5: When are you planning to travel?")
    st.write("This helps us provide seasonal weather information and recommendations.")
    
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    selected_month = st.selectbox("Select your travel month:", months)
    
    # Show seasonal information
    if selected_month:
        seasonal_info = {
            "January": "❄️ Winter - Cold weather, fewer crowds, winter activities",
            "February": "❄️ Winter - Valentine's season, winter sports",
            "March": "🌸 Spring - Blooming flowers, moderate temperatures",
            "April": "🌸 Spring - Easter season, pleasant weather",
            "May": "🌺 Spring - Perfect weather, outdoor activities",
            "June": "☀️ Summer - Warm weather, peak tourist season",
            "July": "☀️ Summer - Hottest month, beach destinations popular",
            "August": "☀️ Summer - Family vacation peak, festivals",
            "September": "🍂 Fall - Mild weather, fewer crowds, harvest season",
            "October": "🍂 Fall - Beautiful autumn colors, Halloween",
            "November": "🍂 Fall - Cooler weather, Thanksgiving travel",
            "December": "❄️ Winter - Holiday season, Christmas markets"
        }
        st.info(seasonal_info[selected_month])
    
    if st.button("Continue"):
        st.session_state.state["travel_month"] = selected_month
        st.session_state.state["messages"].append(HumanMessage(content=selected_month))
        st.session_state.step = 5
        st.rerun()

# Step 6: Destination Selection
elif st.session_state.step == 5:
    st.subheader("Step 6: Choose your destination")
    
    # Get suggestions with progress indicator
    if not st.session_state.state["suggestions"]:
        with st.spinner("Finding perfect destinations..."):
            suggestions = suggest_destinations_streamlit(
                st.session_state.state["interests"],
                st.session_state.state["budget"],
                destination_names,
                descriptions
            )
            st.session_state.state["suggestions"] = suggestions
    
    if st.session_state.state["suggestions"]:
        st.write("Based on your preferences, here are some great destinations:")
        city = st.selectbox("Choose your destination:", st.session_state.state["suggestions"])
        if st.button("Select Destination"):
            st.session_state.state["selected_city"] = city
            st.session_state.state["messages"].append(HumanMessage(content=city))
            st.session_state.step = 6
            st.rerun()

# Step 7: Generate Itinerary
elif st.session_state.step == 6:
    st.subheader("Step 7: Your Personalized Itinerary")
    st.success(f"Selected Destination: {st.session_state.state['selected_city']}")
    
    if not st.session_state.state["itinerary"]:
        with st.spinner("Creating your personalized itinerary..."):
            itinerary = create_itinerary_streamlit(
                st.session_state.state["selected_city"],
                st.session_state.state["interests"],
                st.session_state.state["duration"],
                st.session_state.state["budget"],
                st.session_state.state["travel_month"]
            )
            st.session_state.state["itinerary"] = itinerary
    
    if st.session_state.state["itinerary"]:
        st.markdown(st.session_state.state["itinerary"])
        
        # Show additional city information
        st.subheader("📊 Destination Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Trip Summary:**")
            st.write(f"🎯 Destination: {st.session_state.state['selected_city']}")
            st.write(f"⏰ Duration: {st.session_state.state['duration']} days")
            st.write(f"💰 Budget: {st.session_state.state['budget']}")
            st.write(f"🌟 Interests: {', '.join(st.session_state.state['interests'])}")
            st.write(f"📅 Travel Month: {st.session_state.state['travel_month']}")
            
            # Add real-time information
            st.write("**🌤️ Weather Information:**")
            weather_info = weather_tool.call(st.session_state.state['selected_city'], st.session_state.state['travel_month'])
            st.write(weather_info)
        
        with col2:
            st.write("**Next Steps:**")
            st.write("📅 Book your flights")
            st.write("🏨 Reserve accommodations")
            st.write("🎫 Book attractions in advance")
            st.write("📱 Download local apps")
            
            # Add local information
            st.write("**🏛️ Top Attractions:**")
            st.write(attractions_tool.call(st.session_state.state['selected_city']))
        
        # Additional information in expandable sections
        with st.expander("🍽️ Dining Options"):
            st.write(restaurant_tool.call(st.session_state.state['selected_city']))
        
        with st.expander("🏨 Accommodation Options"):
            st.write(accommodation_tool.call(st.session_state.state['selected_city']))
        
        with st.expander("🚇 Transportation"):
            st.write(transportation_tool.call(st.session_state.state['selected_city']))
    
    if st.button("Start New Trip"):
        st.session_state.step = 0
        st.session_state.state = {
            "messages": [],
            "budget": "",
            "duration": "",
            "interests": [],
            "travel_month": "",
            "suggestions": [],
            "selected_city": "",
            "itinerary": "",
        }
        st.rerun() 