# CrewAI Multi-Agent System: AI in Healthcare Research and Blog Generator

This project uses [CrewAI](https://github.com/crewAIInc/crewAI) to build a multi-agent system that researches "AI in Healthcare" and generates an engaging blog post. It features two agents: a **Senior Research Analyst** who gathers and analyzes web data, and a **Content Writer** who transforms findings into a polished Markdown blog post.

## Features
- **Research Agent**: Searches the web using `SerperDevTool`, compiles a detailed brief with trends, stats, and citations.
- **Writing Agent**: Converts the research into an accessible, well-structured blog post with inline citations.
- **Modular Design**: Easily adaptable to other topics by changing the `topic` variable.

## Prerequisites
- **Python**: 3.10+ (tested with 3.12 in `venv`).
- **API Keys**:
  - [OpenAI API Key](https://platform.openai.com/api-keys) for LLM.
  - [Serper API Key](https://serper.dev) for web search (free tier: 2,500 searches).
- **Windows**: Tested on Windows 10; requires Microsoft Visual C++ Build Tools for some dependencies.

