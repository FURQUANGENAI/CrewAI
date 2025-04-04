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
st.set_page_config(page_title="Personalized Fitness Plan Generator", page_icon="💪", layout="wide")
st.title("🏋️ Personalized Fitness Plan Generator, powered by CrewAI")
st.markdown("Get a customized fitness and diet plan tailored to your goals and preferences.")

# Sidebar
with st.sidebar:
    st.header("Fitness Plan Settings")
    fitness_goal = st.text_input("Enter your fitness goal", placeholder="e.g., Lose weight, Build muscle")
    preferences = st.text_area("Enter your preferences or constraints", height=100, placeholder="e.g., Vegetarian, No dairy, Limited time for workouts")
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    st.markdown("---")
    generate_button = st.button("Generate Plan", type="primary", use_container_width=True)
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Enter your fitness goal
        2. Specify any preferences or constraints
        3. Adjust temperature (higher = more creative)
        4. Click 'Generate Plan'
        5. Download the Markdown result
        """)

def generate_fitness_plan(fitness_goal, preferences, temperature):
    search_tool = SerperDevTool()

    # Agents
    fitness_expert = Agent(
        role="Fitness Expert",
        goal=f"Create a personalized fitness plan for the goal: {fitness_goal}, considering preferences: {preferences}",
        backstory="You're a certified fitness trainer and nutritionist specializing in creating personalized fitness and diet plans...",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
    )

    dietitian = Agent(
        role="Dietitian",
        goal="Design a personalized diet plan that complements the fitness plan and adheres to the user's preferences.",
        backstory="You're a professional dietitian skilled in creating balanced and personalized meal plans...",
        allow_delegation=False,
        verbose=True,
    )

    # Tasks
    fitness_task = Task(
        description=f"Design a fitness plan for the goal: {fitness_goal}, considering preferences: {preferences}. Include workout routines, schedules, and tips.",
        expected_output="A detailed fitness plan with workout routines, schedules, and tips tailored to the user's goal and preferences.",
        agent=fitness_expert
    )

    diet_task = Task(
        description=f"Create a diet plan that complements the fitness plan for the goal: {fitness_goal}, considering preferences: {preferences}.",
        expected_output="A personalized diet plan with meal suggestions, nutritional breakdowns, and adherence to preferences.",
        agent=dietitian
    )

    # Crew
    crew = Crew(
        agents=[fitness_expert, dietitian],
        tasks=[fitness_task, diet_task],
        verbose=True
    )

    return crew.kickoff(inputs={"fitness_goal": fitness_goal, "preferences": preferences})

# Main content
if generate_button:
    if not fitness_goal:
        st.warning("Please enter your fitness goal!")
    elif not preferences:
        st.warning("Please enter your preferences or constraints!")
    else:
        with st.spinner('Generating your personalized fitness plan...'):
            try:
                result = generate_fitness_plan(fitness_goal, preferences, temperature)
                st.markdown("### Generated Fitness Plan")
                st.markdown(result, unsafe_allow_html=True)
                st.download_button(
                    label="Download Plan",
                    data=str(result),
                    file_name=f"{fitness_goal.lower().replace(' ', '_')}_fitness_plan.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit, and OpenAI Done by Furquan Ahmed T")