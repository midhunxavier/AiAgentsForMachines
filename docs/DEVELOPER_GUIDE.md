# Developer Guide

This guide is for developers who want to contribute to the AI Agents for OPC UA Industrial Systems project.

## Development Environment Setup

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/AiAgentsForMachines.git
   cd AiAgentsForMachines
   ```

2. **Set up a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Start the application**:
   ```
   streamlit run opcua-agent.py
   ```

## Project Structure

```
AiAgentsForMachines/
├── .devcontainer/       # Docker development container configuration
├── .git/                # Git directory
├── client/              # OPC UA client functionality
│   ├── findVariablesByEndpoint.py  # OPC UA variable discovery
│   └── __pycache__/     # Python cache directory
├── docs/                # Documentation
│   ├── PROJECT_STRUCTURE.md  # Project structure documentation
│   ├── TECHNICAL_DETAILS.md  # Technical implementation details
│   └── DEVELOPER_GUIDE.md    # This file
├── OPCUA_EXE/           # OPC UA execution logic 
│   ├── opcua_graph.py   # LangGraph implementation
│   └── __pycache__/     # Python cache directory
├── .cursor.json         # Cursor development environment rules
├── .gitignore           # Git ignore rules
├── opcua-agent.py       # Main application entry point
├── README.md            # User documentation
└── requirements.txt     # Project dependencies
```

## Contribution Guidelines

### Code Style

Follow these style guidelines:
- Use PEP 8 for Python code formatting
- Use descriptive variable and function names
- Add docstrings to all functions
- Keep functions focused on a single responsibility
- Handle exceptions appropriately

### Development Workflow

1. **Create a feature branch**:
   ```
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test**:
   - Implement your feature
   - Test thoroughly
   - Update documentation

3. **Commit changes**:
   ```
   git add .
   git commit -m "Description of changes"
   ```

4. **Submit a pull request**:
   - Push your branch to the repository
   - Create a pull request
   - Describe your changes in detail

### Testing

The project does not have automated tests yet, but when implementing changes:
- Test with the default test server
- Test with a real OPC UA server if possible
- Verify that all UI components work as expected
- Check for proper error handling

## Extension Areas

Here are some areas where the project can be extended:

### 1. UI Improvements

- Implement a dark mode
- Add responsive design for mobile devices
- Create a dashboard for monitoring variables
- Add visualization for variable history

### 2. OPC UA Extensions

- Support for more data types (currently focused on boolean for write)
- Implement subscriptions for real-time updates
- Add browse functionality for better navigation
- Support for OPC UA security modes

### 3. Agent Capabilities

- Add agent memory/history
- Implement agent templates for common scenarios
- Add support for more complex reasoning chains
- Create a library of pre-built agents

### 4. Deployment Features

- Add authentication for the web interface
- Create deployment packaging
- Implement agent persistence
- Add monitoring and alerting capabilities

## Troubleshooting

### Common Issues

1. **OPC UA Connection Issues**:
   - Verify the connection string format
   - Ensure the OPC UA server is running
   - Check firewall settings
   - Verify network connectivity

2. **OpenAI API Issues**:
   - Verify your API key is correct
   - Check your API usage limits
   - Ensure the selected model is available

3. **Streamlit Interface Issues**:
   - Clear browser cache
   - Restart the Streamlit server
   - Check for JavaScript console errors

### Debugging

The application prints various debug information:
- Connection status to OPC UA servers
- Variable discovery results
- Tool call details

Use `print()` statements or a proper logging framework for additional debugging.

## Resources

- [OPC UA Python Documentation](https://python-opcua.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)

## Contact

For questions or support, contact:
- Midhun Xavier
- Email: midhun.xavier@ltu.se
- Website: www.midhunxavier.com 