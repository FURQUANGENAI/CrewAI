import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found in .env")
    st.stop()

# Streamlit config
st.set_page_config(page_title="Content Researcher & Writer", page_icon="📰", layout="wide")
st.title("🤖 Content Researcher & Writer, powered by CrewAI")
st.markdown("Generate blog posts about any topic using AI agents.")

# Sidebar
with st.sidebar:
    st.header("Content Settings")
    topic = st.text_area("Enter your topic", height=100, placeholder="e.g., AI in Healthcare")
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.markdown("---")
    generate_button = st.button("Generate Content", type="primary", use_container_width=True)
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Enter your topic
        2. Adjust temperature (higher = more creative)
        3. Click 'Generate Content'
        4. Download the Markdown result
        """)

def generate_content(topic, temperature):
    search_tool = SerperDevTool()

    # Agents
    senior_research_analyst = Agent(
        role="Senior Research Analyst",
        goal=f"Research and synthesize info on {topic} from reliable web sources",
        backstory="You're an expert analyst skilled in web research...",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
    )

    content_writer = Agent(
        role="Content Writer",
        goal="Turn research into engaging blog posts with accuracy",
        backstory="You're a writer who makes complex topics approachable...",
        allow_delegation=False,
        verbose=True,
    )

    # Tasks
    research_task = Task(
        description=f"Conduct comprehensive research on {topic} including trends, news, and stats. Organize into a brief with citations.",
        expected_output="A detailed research report with summary, analysis, and sources.",
        agent=senior_research_analyst
    )

    writing_task = Task(
        description=f"Create an engaging blog post for {topic} from the research brief, with intro, headings, conclusion, and citations.",
        expected_output="A Markdown blog post with # title, ### subsections, and [Source: URL] citations.",
        agent=content_writer
    )

    # Crew
    crew = Crew(
        agents=[senior_research_analyst, content_writer],
        tasks=[research_task, writing_task],
        verbose=True
    )

    return crew.kickoff(inputs={"topic": topic})

# Main content
if generate_button:
    if not topic:
        st.warning("Please enter a topic!")
    else:
        with st.spinner('Generating content...'):
            try:
                result = generate_content(topic, temperature)
                st.markdown("### Generated Content")
                st.markdown(result, unsafe_allow_html=True)
                st.download_button(
                    label="Download Content",
                    data=str(result),
                    file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit,Furquan's skills and OpenAI")