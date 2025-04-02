# AI Agents for OPC UA Industrial Systems

An intelligent agent platform that connects to OPC UA servers and allows users to manage industrial automation systems through natural language instructions.

## Overview

This project enables users to:
- Connect to OPC UA servers and discover variables
- Create AI agents with custom instructions to manage industrial systems
- Control and monitor industrial automation equipment through conversational interfaces
- Test and deploy agents that understand the context of industrial systems

## Features

- **OPC UA Connectivity**: Connect to any OPC UA server using standard connection strings
- **Variable Discovery**: Automatically discover and browse all variables on connected servers
- **Agent Configuration**: Configure AI agents with custom instructions about your system
- **Natural Language Control**: Control industrial systems through simple conversations
- **Real-time Monitoring**: Monitor system variables in real-time
- **Test Mode**: Test your agents before deployment in a safe environment

## Getting Started

### Prerequisites

- Python 3.8+
- OPC UA server (or use the default test server)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AiAgentsForMachines.git
   cd AiAgentsForMachines
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Usage

1. Start the application:
   ```
   streamlit run opcua-agent.py
   ```

2. Connect to an OPC UA server:
   - Enter your connection string (or use the default test server)
   - Click "Connect" to discover available variables

3. Configure your agent:
   - Select variables to include in your agent's environment
   - Customize the agent instructions to match your system
   - Click "Test Agent" to start interacting with your system

4. Interact with your industrial system using natural language

## Example Commands

Once your agent is configured, you can interact with it using commands like:

- "What is the current temperature?"
- "Turn ON the motor."
- "Open the valve to decrease pressure."
- "Check the motor speed."
- "What is the current system status?"

## Advanced Configuration

You can customize the agent's understanding of your system by editing the instructions in the text area. Provide detailed information about your variables, their relationships, and acceptable value ranges.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, contact:
- Midhun Xavier
- Email: midhun.xavier@ltu.se
- Website: www.midhunxavier.com 