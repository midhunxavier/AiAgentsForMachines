# Project Structure Documentation

This document provides a technical overview of the AI Agents for OPC UA Industrial Systems project, intended for AI assistants to understand the codebase.

## Architecture

The project follows a modular architecture with these key components:

1. **UI Layer**: Streamlit-based web interface
2. **OPC UA Client**: Interface for communicating with OPC UA servers
3. **Agent Framework**: LangGraph-based workflow for agent interaction
4. **Natural Language Processing**: OpenAI API integration for language understanding

## Core Components

### 1. Main Application (`opcua-agent.py`)

This is the entry point to the application, containing:
- Streamlit UI setup and rendering
- Session state management
- Variable management workflows (discovery, saving, editing)
- Agent testing interface

The main application manages:
- Connection to OPC UA servers
- Variable discovery and management
- Agent configuration
- Chat interface for testing agents

### 2. OPC UA Client (`client/findVariablesByEndpoint.py`)

This module handles:
- Connection to OPC UA servers
- Discovery of variables and their properties
- Parsing and organizing variable data

The main function `find_variables_by_endpoint(endpoint)` connects to an OPC UA server, recursively discovers all variables, and returns their details including:
- Name
- NodeID
- Object ID
- Current value
- Data type
- Description

### 3. Agent Graph (`OPCUA_EXE/opcua_graph.py`)

This module implements the agent's reasoning and action workflow:
- Sets up a LangGraph workflow for agent-based reasoning
- Defines OPC UA read/write functions as tools
- Manages the agent's state and conversation flow

Key components:
- `opcua_read_variable`: Tool for reading values from OPC UA servers
- `opcua_write_variable`: Tool for writing boolean values to OPC UA servers
- `set_opcua_graph`: Function to create and configure the agent workflow

## Data Flow

1. User connects to an OPC UA server
2. Application discovers variables via `findVariablesByEndpoint.py`
3. User selects variables to include in the agent environment
4. User configures agent instructions
5. When testing, the agent:
   - Receives user prompts
   - Uses LangGraph to determine actions
   - Calls OPC UA tools to read/write values
   - Returns responses to the user

## Dependencies

Major dependencies include:
- `streamlit`: For the web interface
- `opcua`: For OPC UA communication
- `langchain-openai`: For OpenAI API integration
- `langgraph`: For agent workflow management
- `python-dotenv`: For environment variable management

## Security Considerations

- OpenAI API keys are managed through environment variables
- OPC UA connections handle basic error recovery
- No authentication is currently implemented for the web interface
- Variable write operations have no validation or permissions management

## Extension Points

The project can be extended in these areas:
- Adding authentication for the web interface
- Implementing validation for variable writes
- Supporting more complex OPC UA data types
- Adding monitoring and alerting capabilities
- Implementing agent persistence 