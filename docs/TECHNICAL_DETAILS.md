# Technical Implementation Details

This document provides in-depth technical information about the implementation of the AI Agents for OPC UA Industrial Systems.

## OPC UA Communication

### Connection Handling

The project uses the Python OPC UA client library (`opcua`) to establish connections to OPC UA servers. The connection process:

1. Creates a `Client` object with the endpoint URL
2. Calls `client.connect()` to establish the connection
3. Performs operations (read/write/browse)
4. Always calls `client.disconnect()` in a `finally` block to ensure clean disconnection

Node identification follows the OPC UA standard, supporting:
- String NodeIDs (`ns=X;s=StringID`)
- Numeric NodeIDs (`ns=X;i=NumericID`) 
- GUID NodeIDs (`ns=X;g=GUID`)

### Variable Discovery

Variable discovery recursively traverses the OPC UA address space:

1. Starts from the Objects node (`client.get_objects_node()`)
2. Recursively visits all child nodes
3. For each Variable node, collects:
   - Name from browse name
   - NodeID in string format
   - Parent object ID
   - Current value
   - Data type
   - Description
4. Filters out the built-in 'Server' subtree to avoid system variables

The process handles exceptions at each step to ensure robustness against:
- Missing permissions
- Disconnections
- Invalid node types

## Agent Framework

### LangGraph Implementation

The agent uses LangGraph to implement a tool-using pattern:

1. The agent receives a message from the user
2. The agent determines if it needs to use a tool
3. If yes, it calls the appropriate tool with parameters
4. The tool returns results
5. The agent processes the results and responds to the user

The graph structure is defined in `set_opcua_graph`:
```
START → assistant → [conditional] → tools → assistant
```

### Tool Implementation

Two main tools are implemented:

1. `opcua_read_variable`: 
   - Takes endpoint and node_id arguments
   - Connects to the server
   - Reads and returns the variable value
   - Handles various NodeID formats

2. `opcua_write_variable`: 
   - Takes endpoint, node_id, and value_to_write arguments
   - Connects to the server
   - Creates a DataValue with the appropriate VariantType
   - Writes the value to the node
   - Only supports boolean values currently

Both tools implement robust error handling and ensure proper disconnection.

## Streamlit UI

### Session State Management

The application uses Streamlit's session state to maintain:
- Discovered variables (`variables`)
- Variables added to the agent environment (`saved_variables`)
- Connection string (`connection_string`)
- Agent instructions (`agent_instructions`)
- Chat visibility state (`chat_visible`)
- Chat message history (`messages`)
- Workflow configuration (`workflow`)

### UI Components

The interface consists of:
1. **Sidebar**:
   - Connection string input
   - Connect button
   - Available variables display
   - Variables can be added to the agent environment

2. **Main Panel**:
   - Variable table display
   - Agent instructions text area
   - Variables in agent environment with edit capabilities
   - Test/Configure toggle button
   - Chat interface when in test mode

### Variable Management

The UI provides a workflow for managing variables:
1. Variables are discovered when connecting to a server
2. Variables appear in the sidebar initially
3. Users add variables to the agent environment
4. In the environment, users can edit descriptions or remove variables
5. When testing, variables are passed to the agent in JSON format

## OpenAI Integration

The agent utilizes OpenAI for natural language understanding:

1. OpenAI API key is loaded from environment variables
2. ChatOpenAI client is configured with the "gpt-4o-mini" model
3. Tools are bound to the model using `llm.bind_tools()`
4. System instructions and variable details are provided as context
5. The agent processes messages and tool results using the model

## Security Implementation

### API Key Management

API keys are managed using environment variables loaded via `python-dotenv`:
1. Keys are stored in a `.env` file (not committed to version control)
2. `.env` file is loaded at startup
3. Keys are accessed via `os.getenv()`

### Error Handling

The application implements error handling:
1. OPC UA operations are wrapped in try/except blocks
2. Connection errors are reported to the user
3. Tool calls include error reporting in return values
4. All OPC UA connections are properly closed in finally blocks

## Configuration Management

### Agent Configuration

Agent configuration consists of:
1. Connection string to the OPC UA server
2. Instructions for the agent (system context)
3. Variables included in the agent environment
    - Name
    - NodeID
    - Description
    - Current value

The configuration can be:
- Tested in the interface
- Downloaded as a JSON file
- (Future) Deployed as a standalone agent 