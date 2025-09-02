from langchain.agents import Tool, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.schema import HumanMessage, SystemMessage
import time
import os
from dotenv import load_dotenv

# Load environment variables (.env must have GROQ_API_KEY="your_key_here")
load_dotenv()


class ResearchAgent:
    """Base class for all research agents"""

    def __init__(self, name: str, role: str, model_name: str = "llama-3.1-8b-instant"):
        self.name = name
        self.role = role
        self.llm = ChatGroq(
            model=model_name,                 # Groq-supported model
            temperature=0.7,
            max_tokens=1000,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.search_tool = DuckDuckGoSearchRun()

    def get_system_prompt(self) -> str:
        return f"""You are {self.name}, a specialized AI agent with the role of {self.role}.
        Your task is to provide accurate, well-researched information in your area of expertise.
        Always be thorough, objective, and cite your sources when possible."""

    def process_query(self, query: str, context: str = ""):
        """To be implemented by subclasses"""
        raise NotImplementedError


class InformationGatherer(ResearchAgent):
    """Agent responsible for gathering comprehensive information"""

    def __init__(self):
        super().__init__("InfoGatherer", "Information Gathering Specialist")

    def get_system_prompt(self) -> str:
        return """You are InfoGatherer, an expert at finding and collecting comprehensive information on any topic.
        Your role is to:
        1. Search for relevant information from multiple sources
        2. Gather facts, statistics, and key details
        3. Organize information in a structured format
        4. Identify gaps in information that need further research

        Always provide factual, well-sourced information."""

    def process_query(self, query: str, context: str = ""):
        # Step 1: Search
        search_results = self.search_tool.run(f"{query} comprehensive information")

        # Step 2: Build messages
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=f"""
            Research Topic: {query}
            Context: {context}
            Search Results: {search_results}

            Please provide a comprehensive overview of this topic, including:
            1. Key facts and statistics
            2. Important details and context
            3. Current trends or developments
            4. Areas that need further investigation

            Format your response as structured information.
            """)
        ]

        # Step 3: Call LLM
        response = self.llm.invoke(messages)

        return {
            "agent": self.name,
            "role": self.role,
            "query": query,
            "response": response.content if hasattr(response, "content") else str(response),
            "search_results": search_results,
            "timestamp": time.time()
        }


class DataAnalyzer(ResearchAgent):
    """Agent responsible for analyzing and interpreting data"""

    def __init__(self):
        super().__init__("DataAnalyzer", "Data Analysis Specialist")

    def get_system_prompt(self) -> str:
        return """You are DataAnalyzer, an expert at analyzing information and extracting meaningful insights.
        Your role is to:
        1. Analyze provided information for patterns and trends
        2. Identify key relationships and correlations
        3. Provide statistical insights where applicable
        4. Highlight important implications and conclusions

        Focus on analytical depth and critical thinking."""

    def process_query(self, query: str, context: str = ""):
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=f"""
            Analysis Request: {query}
            Context to Analyze: {context}

            Please provide a detailed analysis including:
            1. Key patterns and trends identified
            2. Statistical insights and correlations
            3. Critical evaluation of the information
            4. Implications and conclusions
            5. Areas requiring further investigation
            """)
        ]

        response = self.llm.invoke(messages)

        return {
            "agent": self.name,
            "role": self.role,
            "query": query,
            "response": response.content,
            "analysis_type": "comprehensive",
            "timestamp": time.time()
        }


class SummaryGenerator(ResearchAgent):
    """Agent responsible for creating concise summaries"""

    def __init__(self):
        super().__init__("SummaryGen", "Summary Generation Specialist")

    def get_system_prompt(self) -> str:
        return """You are SummaryGen, an expert at creating clear, concise, and comprehensive summaries.
        Your role is to:
        1. Synthesize complex information into digestible summaries
        2. Maintain accuracy while improving readability
        3. Highlight the most important points
        4. Create executive summaries for decision-making

        Focus on clarity and completeness."""

    def process_query(self, query: str, context: str = ""):
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=f"""
            Summary Request: {query}
            Information to Summarize: {context}

            Please create a comprehensive summary including:
            1. Executive summary (2-3 sentences)
            2. Key points and findings
            3. Important details and context
            4. Conclusions and recommendations
            """)
        ]

        response = self.llm.invoke(messages)

        return {
            "agent": self.name,
            "role": self.role,
            "query": query,
            "response": response.content,
            "summary_type": "comprehensive",
            "timestamp": time.time()
        }


class InsightGenerator(ResearchAgent):
    """Agent responsible for generating insights and recommendations"""

    def __init__(self):
        super().__init__("InsightGen", "Insight Generation Specialist")

    def get_system_prompt(self) -> str:
        return """You are InsightGen, an expert at generating actionable insights and strategic recommendations.
        Your role is to:
        1. Identify strategic implications and opportunities
        2. Provide actionable recommendations
        3. Suggest next steps and future considerations
        4. Highlight potential risks and challenges

        Focus on practical value and strategic thinking."""

    def process_query(self, query: str, context: str = ""):
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=f"""
            Insight Request: {query}
            Research Context: {context}

            Please provide strategic insights including:
            1. Key opportunities and implications
            2. Actionable recommendations
            3. Potential risks and challenges
            4. Strategic next steps
            5. Future considerations and trends
            """)
        ]

        response = self.llm.invoke(messages)

        return {
            "agent": self.name,
            "role": self.role,
            "query": query,
            "response": response.content,
            "insight_type": "strategic",
            "timestamp": time.time()
        }


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to work together on research tasks"""

    def __init__(self):
        self.agents = {
            "gatherer": InformationGatherer(),
            "analyzer": DataAnalyzer(),
            "summarizer": SummaryGenerator(),
            "insight_generator": InsightGenerator()
        }
        self.results = {}

    def conduct_research(self, query: str):
        print(f"🚀 Starting research on: {query}")

        # Step 1: Gather
        print("🔍 Step 1: Gathering information...")
        gatherer_result = self.agents["gatherer"].process_query(query)
        self.results["information"] = gatherer_result

        # Step 2: Analyze
        print("📊 Step 2: Analyzing information...")
        analyzer_result = self.agents["analyzer"].process_query(
            f"Analyze this information: {query}",
            gatherer_result["response"]
        )
        self.results["analysis"] = analyzer_result

        # Step 3: Summarize
        print("📝 Step 3: Generating summary...")
        combined_context = f"{gatherer_result['response']}\n\n{analyzer_result['response']}"
        summary_result = self.agents["summarizer"].process_query(
            f"Summarize research on: {query}",
            combined_context
        )
        self.results["summary"] = summary_result

        # Step 4: Insights
        print("💡 Step 4: Generating insights...")
        insight_result = self.agents["insight_generator"].process_query(
            f"Generate insights for: {query}",
            combined_context
        )
        self.results["insights"] = insight_result

        return {
            "query": query,
            "results": self.results,
            "timestamp": time.time(),
            "agents_used": list(self.agents.keys())
        }

    def get_agent_status(self):
        return {name: "active" for name in self.agents.keys()}
