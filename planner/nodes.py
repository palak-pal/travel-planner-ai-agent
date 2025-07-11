from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import weather_tool, attractions_tool, transportation_tool, restaurant_tool, accommodation_tool

# Get API key from environment
import os
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY", "demo_key")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                             google_api_key=api_key,
                             temperature=0.5)
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

def ask_budget(state):
    print("\n💰 Let's start with your budget preferences...")
    while True:
        budget = input("💳 Budget level (low, medium, high): ").strip().lower()
        if budget in {"low", "medium", "high"}:
            budget_descriptions = {
                "low": "Budget-friendly options, hostels, street food, public transport",
                "medium": "Mid-range hotels, mix of dining options, some private transport",
                "high": "Luxury accommodations, fine dining, private tours, premium experiences"
            }
            print(f"✅ {budget_descriptions[budget]}")
            break
        print("❌ [Error] Please enter 'low', 'medium', or 'high'.")
    return {**state, "budget": budget, "messages": state["messages"] + [HumanMessage(content=budget)]}

def ask_duration(state):
    print("\n📅 How long will your adventure be?")
    while True:
        duration = input("⏰ Number of days: ").strip()
        if duration.isdigit() and int(duration) > 0:
            days = int(duration)
            if days == 1:
                print("✅ Perfect for a day trip!")
            elif days <= 3:
                print("✅ Great for a weekend getaway!")
            elif days <= 7:
                print("✅ Excellent for a week-long adventure!")
            else:
                print("✅ Fantastic for an extended journey!")
            break
        print("❌ [Error] Please enter a positive number for days.")
    return {**state, "duration": duration, "messages": state["messages"] + [HumanMessage(content=duration)]}

def ask_interests(state):
    print("\n🌟 What interests you most?")
    print("💡 Examples: history, food, nature, art, adventure, culture, shopping, nightlife")
    while True:
        interests = input("🎯 Your interests (comma-separated): ").split(",")
        interests = [i.strip().lower() for i in interests if i.strip()]
        if interests:
            print(f"✅ Interests captured: {', '.join(interests)}")
            break
        print("❌ [Error] Please enter at least one interest.")
    return {**state, "interests": interests, "messages": state["messages"] + [HumanMessage(content=', '.join(interests))]}

def suggest_destinations(state, dest_index, destination_names, embedding_model):
    print(f"\n🔍 Finding perfect destinations for your {state['budget']} budget...")
    query = ' '.join(state["interests"])
    query_vec = embedding_model.encode([query])
    D, I = dest_index.search(query_vec, k=8)  # get more to filter by budget
    
    # Filter by budget: low=first 2, medium=middle 2, high=last 2
    budget = state.get("budget", "medium")
    if budget == "low":
        idxs = I[0][:2]
    elif budget == "high":
        idxs = I[0][-2:]
    else:
        idxs = I[0][2:4]
    
    suggestions = [destination_names[i] for i in idxs]
    print(f"🌍 Perfect destinations for your {budget} budget:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion}")
    return {**state, "suggestions": suggestions}

def select_city(state, embedding_model, dest_index, names):
    def match_city(user_input, suggestions):
        user_input = user_input.strip().lower()
        for s in suggestions:
            if user_input == s.lower():
                return s
            if user_input in s.lower():
                return s
        return None

    # First selection
    print(f"\n🎯 Choose your destination:")
    while True:
        selected1 = input(f"📍 Select from ({', '.join(state['suggestions'])}): ").strip()
        match1 = match_city(selected1, state['suggestions'])
        if match1:
            selected1 = match1
            print(f"✅ First choice: {selected1}")
            break
        print("❌ [Error] Please choose a valid city from the suggestions.")

    # Dynamically generate a new set of suggestions for refinement
    print(f"\n🔄 Let's refine your choice with more options...")
    query = ' '.join(state["interests"])
    query_vec = embedding_model.encode([query])
    D, I = dest_index.search(query_vec, k=10)
    new_suggestions = [names[i] for i in I[0] if names[i] != selected1]
    dynamic_suggestions = new_suggestions[:3]
    if selected1 not in dynamic_suggestions:
        dynamic_suggestions.append(selected1)

    while True:
        selected2 = input(f"🎯 Final choice ({', '.join(dynamic_suggestions)}): ").strip()
        match2 = match_city(selected2, dynamic_suggestions)
        if match2:
            selected2 = match2
            print(f"🎉 Excellent choice: {selected2}")
            break
        print("❌ [Error] Please choose a valid city from the suggestions.")
    
    # Show comprehensive tool outputs for the selected city
    print(f"\n📊 Quick overview of {selected2}:")
    print(f"🌤️  {weather_tool.call(selected2)}")
    print(f"🏛️  {attractions_tool.call(selected2)}")
    print(f"🍽️  {restaurant_tool.call(selected2)}")
    print(f"🏨  {accommodation_tool.call(selected2)}")
    print(f"🚇  {transportation_tool.call(selected2)}")
    
    return {**state, "selected_city": selected2, "messages": state["messages"] + [HumanMessage(content=selected1), HumanMessage(content=selected2)]}

def create_itinerary(state):
    print(f"\n📝 Creating your personalized {state['duration']}-day itinerary for {state['selected_city']}...")
    print("⏳ This may take a moment...")
    
    response = llm.invoke(itinerary_prompt.format_messages(
        city=state["selected_city"],
        interests=', '.join(state["interests"]),
        duration=state["duration"],
        budget=state["budget"],
        starting_month="your travel month"  # You could add a month input if needed
    ))
    
    print("\n" + "="*60)
    print("🗺️  YOUR PERSONALIZED ITINERARY")
    print("="*60)
    print(response.content)
    print("="*60)
    
    return {**state, "itinerary": response.content, "messages": state["messages"] + [AIMessage(content=response.content)]}

def call_tools(state):
    print(f"\n📋 Final Destination Summary for {state['selected_city']}:")
    print("-" * 50)
    
    # Weather
    weather_info = weather_tool.call(state['selected_city'])
    print(f"🌤️  Weather: {weather_info}")
    
    # Attractions
    attractions_info = attractions_tool.call(state['selected_city'])
    print(f"🏛️  Attractions: {attractions_info}")
    
    # Restaurants
    restaurants_info = restaurant_tool.call(state['selected_city'])
    print(f"🍽️  Dining: {restaurants_info}")
    
    # Accommodations
    accommodations_info = accommodation_tool.call(state['selected_city'])
    print(f"🏨  Accommodations: {accommodations_info}")
    
    # Transportation
    transport_info = transportation_tool.call(state['selected_city'])
    print(f"🚇  Transportation: {transport_info}")
    
    print("\n" + "="*50)
    print("📋 TRIP SUMMARY")
    print("="*50)
    print(f"🎯 Destination: {state['selected_city']}")
    print(f"⏰ Duration: {state['duration']} days")
    print(f"💰 Budget: {state['budget']}")
    print(f"🌟 Interests: {', '.join(state['interests'])}")
    print("="*50)
    print("🎉 Your travel planning is complete! Have a wonderful trip!")
    print("="*50 + "\n")
    
    return state