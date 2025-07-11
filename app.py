from planner.graph import build_workflow
from langchain_core.messages import HumanMessage
import os

def print_welcome_banner():
    print("=" * 70)
    print("🌟 AI TRAVEL PLANNER - PROFESSIONAL EDITION 🌟")
    print("=" * 70)
    print("🗺️  Your personal AI travel assistant powereds")
    print("📊 Enhanced with dynamic data from Google Places API")
    print("🎯 Professional itinerary planning with real-time information")
    print("=" * 70)

def print_features():
    print("\n✨ FEATURES:")
    print("   🎯 Personalized destination recommendations")
    print("   📝 Detailed day-by-day itineraries")
    print("   🌤️  Real-time weather information")
    print("   🏛️  Top attractions with ratings")
    print("   🍽️  Popular restaurants and cuisine")
    print("   🏨  Accommodation options")
    print("   🚇  Transportation information")
    print("   💰 Budget-optimized suggestions")
    print("   🎨 AI-powered luxury travel planning")

def check_data_availability():
    """Check if dynamic data is available and provide status"""
    dynamic_data_file = "travel_data/traveldata.json"
    fallback_data_file = "data/destinations.json"
    
    if os.path.exists(dynamic_data_file):
        print(f"✅ Dynamic data available: {dynamic_data_file}")
        return True
    elif os.path.exists(fallback_data_file):
        print(f"⚠️  Using fallback data: {fallback_data_file}")
        print("💡 Run demo.py to generate dynamic data for enhanced experience")
        return True
    else:
        print("❌ No data files found!")
        print("💡 Please ensure either travel_data/traveldata.json or data/destinations.json exists")
        return False

app = build_workflow()

GOOGLE_API_KEY = "AIzaSyCj8z2l6ukPj-gqQeNBDikNO4WAXeUjk34"

def travel_planner(user_request: str = None):
    """Enhanced travel planner with professional UX"""
    
    if not check_data_availability():
        print("❌ Cannot start travel planner without data files")
        return
    
    print_welcome_banner()
    print_features()
    
    if user_request:
        print(f"\n🎯 Processing your request: {user_request}")
    else:
        print("\n🚀 Ready to plan your perfect trip!")
        print("💡 You can start with a general request like 'I want to plan a trip'")
        print("   or be specific like 'I want to visit Paris for 5 days'")
    
    print("\n" + "="*50)
    
    # Initialize state
    state = {
        "messages": [HumanMessage(content=user_request or "I want to plan a trip")],
        "budget": "",
        "duration": "",
        "interests": [],
        "suggestions": [],
        "selected_city": "",
        "itinerary": "",
    }
    
    try:
        # Stream through the workflow
        for step in app.stream(state):
            pass
        
        print("\n🎉 Travel planning session completed successfully!")
        
    except Exception as e:
        print(f"\n❌ An error occurred during travel planning: {str(e)}")
        print("💡 Please try again or check your internet connection")

if __name__ == "__main__":
    print_welcome_banner()
    
    # Check if user wants to provide a specific request
    print("\n💭 How would you like to start?")
    print("   1. Enter a specific travel request")
    print("   2. Start with general planning")
    
    choice = input("\n🎯 Your choice (1 or 2): ").strip()
    
    if choice == "1":
        user_input = input("\n✈️  Tell me your trip idea: ")
        travel_planner(user_input)
    else:
        travel_planner()