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
st.set_page_config(page_title="Climate Action Plan Generator", page_icon="🌍", layout="wide")
st.title("🌱 Climate Change Research & Action Plan, powered by CrewAI")
st.markdown("Generate actionable plans to combat climate change in your region.")

# Sidebar
with st.sidebar:
    st.header("Climate Settings")
    region = st.text_input("Enter your region", placeholder="e.g., California, USA")
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.markdown("---")
    generate_button = st.button("Generate Action Plan", type="primary", use_container_width=True)

def generate_climate_plan(region, temperature):
    search_tool = SerperDevTool()

    # Agents
    climate_researcher = Agent(
        role="Climate Researcher",
        goal=f"Research climate change impacts and challenges in {region}.",
        backstory="You're a climate researcher specializing in analyzing environmental data...",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
    )

    policy_advisor = Agent(
        role="Policy Advisor",
        goal="Propose actionable solutions to address climate change challenges in the region.",
        backstory="You're a policy advisor skilled in creating actionable plans for environmental challenges...",
        allow_delegation=False,
        verbose=True,
    )

    # Tasks
    research_task = Task(
        description=f"Research climate change impacts, challenges, and data for {region}.",
        expected_output="A detailed research report on climate change impacts in the region.",
        agent=climate_researcher
    )

    action_plan_task = Task(
        description=f"Propose actionable solutions to address climate change challenges in {region}.",
        expected_output="An action plan with specific recommendations and steps.",
        agent=policy_advisor
    )

    # Crew
    crew = Crew(
        agents=[climate_researcher, policy_advisor],
        tasks=[research_task, action_plan_task],
        verbose=True
    )

    return crew.kickoff(inputs={"region": region})

# Main content
if generate_button:
    if not region:
        st.warning("Please enter a region!")
    else:
        with st.spinner('Generating action plan...'):
            try:
                result = generate_climate_plan(region, temperature)
                st.markdown("### Generated Climate Action Plan")
                st.markdown(result, unsafe_allow_html=True)
                st.download_button(
                    label="Download Action Plan",
                    data=str(result),
                    file_name=f"{region.lower().replace(' ', '_')}_climate_plan.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit, and OpenAI Implemented By Furquan")