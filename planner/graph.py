from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage
from .nodes import ask_budget, ask_duration, ask_interests, suggest_destinations, select_city, create_itinerary, call_tools
from .rag import rag_follow_up
from sentence_transformers import SentenceTransformer
import faiss
import json
import os

class PlannerState(TypedDict):
    messages: List[HumanMessage | AIMessage]
    budget: str
    duration: str
    interests: List[str]
    suggestions: List[str]
    selected_city: str
    itinerary: str

def build_workflow():
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Load dynamic data from travel_data/traveldata.json
    data_file = "travel_data/traveldata.json"
    if not os.path.exists(data_file):
        print(f"⚠️  Dynamic data file not found: {data_file}")
        print("📝 Using fallback data from destinations.json")
        data_file = "data/destinations.json"
    
    with open(data_file, encoding="utf-8") as f:
        destinations = json.load(f)
    
    # Enhanced data processing for dynamic data
    if data_file == "travel_data/traveldata.json":
        # Process dynamic data structure
        descriptions = []
        names = []
        for dest in destinations:
            name = dest.get("name", "")
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
            names.append(name)
    else:
        # Fallback to original structure
        descriptions = [d["description"] for d in destinations]
        names = [d["name"] for d in destinations]
    
    print(f"🗺️  Loaded {len(names)} destinations for travel planning")
    
    # Create FAISS index for similarity search
    embeddings = embedding_model.encode(descriptions)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    print(f"🔍 FAISS index created with {embeddings.shape[0]} embeddings")

    workflow = StateGraph(state_schema=PlannerState)
    workflow.add_node("ask_budget", ask_budget)
    workflow.add_node("ask_duration", ask_duration)
    workflow.add_node("ask_interests", ask_interests)
    workflow.add_node("suggest_destinations", lambda state: suggest_destinations(state, index, names, embedding_model))
    workflow.add_node("select_city", lambda state: select_city(state, embedding_model, index, names))
    workflow.add_node("create_itinerary", create_itinerary)
    workflow.add_node("call_tools", call_tools)
    workflow.add_node("rag_follow_up", rag_follow_up)

    workflow.set_entry_point("ask_budget")
    workflow.add_edge("ask_budget", "ask_duration")
    workflow.add_edge("ask_duration", "ask_interests")
    workflow.add_edge("ask_interests", "suggest_destinations")
    workflow.add_edge("suggest_destinations", "select_city")
    workflow.add_edge("select_city", "create_itinerary")
    workflow.add_edge("create_itinerary", "call_tools")
    workflow.add_edge("call_tools", "rag_follow_up")
    workflow.add_edge("rag_follow_up", END)

    app = workflow.compile()
    return app