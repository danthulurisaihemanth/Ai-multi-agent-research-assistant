import streamlit as st
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Import orchestrator
from agents.research_agents import MultiAgentOrchestrator

# Load environment variables
load_dotenv()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    /* Header */
    .main-header {
        background: linear-gradient(90deg, #2c3e50 0%, #4ca1af 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }

    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Agent Cards */
    .agent-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        text-align: center;
    }

    .agent-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }

    .agent-role {
        font-size: 0.85rem;
        color: #6c757d;
        margin-bottom: 0.8rem;
    }

    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .status-active { background-color: #28a745; }
    .status-processing { background-color: #ffc107; }
    .status-completed { background-color: #17a2b8; }

    /* Result Section */
    .result-section {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .result-section h4 {
        margin-bottom: 0.8rem;
        color: #2c3e50;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
def initialize_session_state():
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = MultiAgentOrchestrator()
    if 'research_results' not in st.session_state:
        st.session_state.research_results = None
    if 'research_history' not in st.session_state:
        st.session_state.research_history = []
    if 'current_query' not in st.session_state:
        st.session_state.current_query = ""

# -------------------- HEADER --------------------
def display_header():
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Research Assistant</h1>
        <p>Multi-Agent System for Comprehensive Research & Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------- AGENT STATUS --------------------
def display_agent_status():
    st.markdown("### Agent Status")

    agents_info = [
        ("InfoGatherer", "Information Gathering", "🔍"),
        ("DataAnalyzer", "Data Analysis", "📊"),
        ("SummaryGen", "Summary Generation", "📝"),
        ("InsightGen", "Insight Generation", "💡")
    ]

    for name, role, icon in agents_info:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-title">{icon} {name}</div>
            <div class="agent-role">{role}</div>
            <span class="status-indicator status-active"></span> Active
        </div>
        """, unsafe_allow_html=True)


def display_research_interface():
    st.markdown("### 🔍 Research Query")

    query = st.text_area(
        "Enter your research topic or question:",
        placeholder="e.g., 'Impact of AI in healthcare' or 'Trends in renewable energy'",
        height=100,
        value=st.session_state.current_query
    )

    # Use container with buttons side by side (no nested st.columns)
    with st.container():
        start = st.button("🚀 Start Research")
        history = st.button("📊 View History")

    if start:
        if query.strip():
            st.session_state.current_query = query
            conduct_research(query)
        else:
            st.error("Please enter a research query!")

    if history:
        display_research_history()

    st.info("💡 **Tip**: Be specific for better results.")


# -------------------- CONDUCT RESEARCH --------------------
def conduct_research(query):
    with st.spinner("🤖 Agents are working on your research..."):
        try:
            if not os.getenv("GROQ_API_KEY"):
                st.error("⚠️ Groq API key not found! Please set GROQ_API_KEY in your .env file.")
                return

            progress_bar = st.progress(0)
            status_text = st.empty()

            steps = [
                "🔍 InfoGatherer: Collecting information...",
                "📊 DataAnalyzer: Analyzing data...",
                "📝 SummaryGen: Creating summary...",
                "💡 InsightGen: Generating insights..."
            ]

            for i, step in enumerate(steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(steps))
                time.sleep(1)

            results = st.session_state.orchestrator.conduct_research(query)

            st.session_state.research_results = results
            st.session_state.research_history.append({
                "query": query,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": results
            })

            status_text.text("✅ Research completed!")
            progress_bar.progress(1.0)

            display_research_results(results)

        except Exception as e:
            st.error(f"❌ Error during research: {str(e)}")

# -------------------- DISPLAY RESULTS --------------------
def display_research_results(results):
    st.markdown("### 📋 Research Results")

    if not results:
        st.warning("No results available.")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Agents Used", len(results.get("agents_used", [])))
    with col2: st.metric("Research Time", datetime.now().strftime("%H:%M:%S"))
    with col3: st.metric("Query Length", len(results.get("query", "")))
    with col4: st.metric("Sections Generated", len(results.get("results", {})))

    agent_results = results.get("results", {})

    for key, title, icon in [
        ("information", "Information Gathering Results", "🔍"),
        ("analysis", "Data Analysis Results", "📊"),
        ("summary", "Executive Summary", "📝"),
        ("insights", "Strategic Insights", "💡")
    ]:
        if key in agent_results:
            with st.expander(f"{icon} {title}", expanded=True if key == "information" else False):
                st.markdown(f"""
                <div class="result-section">
                    <h4>{title}</h4>
                    <p>{agent_results[key].get('response', 'No data available')}</p>
                </div>
                """, unsafe_allow_html=True)

# -------------------- HISTORY --------------------
def display_research_history():
    st.markdown("### 📚 Research History")
    if not st.session_state.research_history:
        st.info("No research history yet.")
        return

    for i, entry in enumerate(reversed(st.session_state.research_history[-5:])):
        with st.expander(f"🔍 {entry['query'][:50]}... - {entry['timestamp']}"):
            st.write(f"**Query:** {entry['query']}")
            st.write(f"**Timestamp:** {entry['timestamp']}")
            if st.button("View Results", key=f"view_{i}"):
                st.session_state.research_results = entry['results']
                display_research_results(entry['results'])

# -------------------- SIDEBAR --------------------
def display_sidebar():
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        This system uses **multi-agent AI**:
        - 🔍 InfoGatherer: Collects information  
        - 📊 DataAnalyzer: Interprets data  
        - 📝 SummaryGen: Creates summaries  
        - 💡 InsightGen: Generates insights  
        """)

        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - LangChain  
        - Groq LLMs  
        - DuckDuckGo Search  
        - Streamlit  
        """)

        if os.getenv("GROQ_API_KEY"):
            st.success("✅ Groq API Key configured")
        else:
            st.error("❌ Groq API Key not found")

# -------------------- MAIN --------------------
def main():
    initialize_session_state()
    display_header()

    col1, col2 = st.columns([2, 1])

    with col1:
        display_agent_status()
        display_research_interface()

        if st.session_state.research_results:
            st.subheader("📊 Research Results")

            # Use tabs instead of nested columns
            tabs = st.tabs(["📚 Info Gatherer", "📈 Data Analysis", "📝 Summary", "💡 Insights"])

            with tabs[0]:
                st.markdown("### Information Gathering Results")
                st.write(st.session_state.research_results["results"]["information"]["response"])

            with tabs[1]:
                st.markdown("### Data Analysis Results")
                st.write(st.session_state.research_results["results"]["analysis"]["response"])

            with tabs[2]:
                st.markdown("### Summary Results")
                st.write(st.session_state.research_results["results"]["summary"]["response"])

            with tabs[3]:
                st.markdown("### Insights Results")
                st.write(st.session_state.research_results["results"]["insights"]["response"])

    with col2:
        display_sidebar()

if __name__ == "__main__":
    main()
