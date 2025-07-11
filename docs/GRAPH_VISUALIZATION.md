# 🎨 LangGraph Workflow Visualization

This document provides visual representations of the Travel Planner AI Agent's LangGraph workflow.

## 📊 Workflow Overview

The Travel Planner AI Agent uses a multi-node LangGraph workflow with the following structure:

```
🚀 START
   ↓
💰 ask_budget → 📅 ask_duration → 🌟 ask_interests
   ↓
🔍 suggest_destinations → 🎯 select_city
   ↓
📝 create_itinerary → 🛠️ call_tools → 📚 rag_follow_up
   ↓
✅ END
```

## 🔄 Detailed Workflow Phases

### Phase 1: User Input Collection
```
💰 ask_budget
├── Input: User budget preference (low/medium/high)
├── State Update: {budget: "low/medium/high"}
└── Output: Budget level stored in state

📅 ask_duration  
├── Input: Number of days for trip
├── State Update: {duration: "5"}
└── Output: Trip duration stored in state

🌟 ask_interests
├── Input: Comma-separated interests
├── State Update: {interests: ["history", "food", "culture"]}
└── Output: User interests stored in state
```

### Phase 2: AI-Powered Destination Selection
```
🔍 suggest_destinations
├── Input: User interests + budget
├── Process: Vector embeddings + FAISS similarity search
├── State Update: {suggestions: ["Paris", "Rome", "Tokyo"]}
└── Output: Filtered destination suggestions

🎯 select_city
├── Input: User selects from suggestions
├── Process: Dynamic refinement with additional options
├── State Update: {selected_city: "Paris"}
└── Output: Final destination selection
```

### Phase 3: Planning & External Tools
```
📝 create_itinerary
├── Input: Selected city + user preferences
├── Process: Google Gemini AI generation
├── State Update: {itinerary: "Day 1: ..."}
└── Output: Detailed day-by-day itinerary

🛠️ call_tools
├── Input: Selected city
├── Process: Multiple API calls (weather, attractions, etc.)
├── Tools: WeatherTool, AttractionsTool, RestaurantTool, etc.
└── Output: Real-time destination information
```

### Phase 4: Knowledge Enhancement & Completion
```
📚 rag_follow_up
├── Input: Selected city + itinerary
├── Process: RAG with vector embeddings
├── State Update: {enhanced_info: "..."}
└── Output: Additional destination knowledge

✅ END
├── State: Complete
└── Output: Final travel plan with all information
```

## 🏗️ State Management

The workflow maintains a `PlannerState` object that evolves through each node:

```python
class PlannerState(TypedDict):
    messages: List[HumanMessage | AIMessage]  # Conversation history
    budget: str                               # "low", "medium", "high"
    duration: str                             # Number of days
    interests: List[str]                      # User interests
    suggestions: List[str]                    # AI-suggested destinations
    selected_city: str                        # Final destination choice
    itinerary: str                           # Generated travel plan
```

## 🛠️ Generating Visualizations

### Prerequisites
Install Graphviz:
```bash
# Windows
# Download from https://graphviz.org/download/

# macOS
brew install graphviz

# Linux
sudo apt-get install graphviz
```

### Generate Graph Images
```bash
# Install Python dependency
pip install graphviz

# Run visualization script
python visualize_graph.py
```

This will generate three types of visualizations:
- `graph_workflow.png/svg`: Basic workflow diagram
- `graph_detailed.png/svg`: Detailed phase-based view
- `graph_state_flow.png/svg`: State transition diagram

## 📋 Node Functions

### Input Collection Nodes
- **ask_budget**: Collects user budget preference
- **ask_duration**: Collects trip duration
- **ask_interests**: Collects user interests

### AI Processing Nodes
- **suggest_destinations**: Uses embeddings to suggest destinations
- **select_city**: Handles user destination selection
- **create_itinerary**: Generates detailed itinerary with Gemini AI

### Tool Integration Nodes
- **call_tools**: Executes external API tools
- **rag_follow_up**: Performs RAG-based knowledge enhancement

## 🔧 Customization

### Adding New Nodes
1. Define the node function in `planner/nodes.py`
2. Add the node to the workflow in `planner/graph.py`
3. Update the visualization script if needed

### Modifying Workflow Flow
Edit the edges in `planner/graph.py`:
```python
workflow.add_edge("node1", "node2")
workflow.add_edge("node2", "node3")
```

### Adding New Tools
1. Create tool class in `planner/tools.py`
2. Import and use in relevant nodes
3. Update visualization if needed

## 📈 Performance Considerations

- **Caching**: Embeddings and models are cached for performance
- **Lazy Loading**: Heavy components loaded only when needed
- **State Persistence**: State maintained throughout workflow
- **Error Handling**: Fallbacks for API failures and missing data

## 🎯 Use Cases

This workflow is designed for:
- **Personal Travel Planning**: Individual trip planning
- **Group Travel**: Can be extended for group preferences
- **Business Travel**: Corporate travel planning
- **Educational**: Learning LangGraph and AI workflows
- **Research**: AI-powered travel recommendation systems 