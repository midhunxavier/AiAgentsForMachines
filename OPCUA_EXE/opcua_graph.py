from opcua import Client, ua
import uuid
import time
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
import json
from functools import partial
from typing import Any
from dotenv import load_dotenv
import os 

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


# Extend the MessagesState as needed
class MessagesState(MessagesState):
    myname: str

def opcua_read_variable(endpoint: str, node_id_str: str) -> str:
    """ Reads an OPC UA variable from the server. 
    Args:
        endpoint (str): The full OPC UA connection string.
        node_id_str (str): The full node ID string in the format 'ns=X;g=GUID'.
    Returns:
        The value of the OPC UA variable, or an error message if an error occurs.
    """
    client = Client(endpoint)
    try:
        client.connect()

        # Parse node ID string
        parts = node_id_str.split(";")
        namespace_idx = int(parts[0].split("=")[1])  # Extract namespace index (ns=X)
        guid_str = parts[1].split("=")[1]  # Extract GUID (g=GUID)


        
        # Get the node
        if len(guid_str) <3:
            node = client.get_node(node_id_str)
        else:
            # Convert GUID string to UUID
            node_guid = uuid.UUID(guid_str)
            node = client.get_node(ua.NodeId(node_guid, namespace_idx))

        # Read the value
        value = node.get_value()

        return str(value)

    except Exception as e:
        return f"Error while reading: {e}"

    finally:
        client.disconnect()

    
def opcua_write_variable(endpoint: str, node_id_str: str, value_to_write: bool) -> str:
    """
    Writes a value to an OPC UA variable on the server.
    
    Args:
        endpoint (str): The full OPC UA connection string.
        node_id_str (str): The full node ID string in the format 'ns=X;g=GUID'.
        value_to_write (bool): The value to write to the variable.
    
    Returns:
        str: A message indicating the result of the write operation.
    """
    client = Client(endpoint)
    try:
        client.connect()

        # Parse node ID string
        parts = node_id_str.split(";")
        namespace_idx = int(parts[0].split("=")[1])  # Extract namespace index (ns=X)
        guid_str = parts[1].split("=")[1]  # Extract GUID (g=GUID)



        if len(guid_str) <3:
            node = client.get_node(node_id_str)
        else:
            # Convert GUID string to UUID
            node_guid = uuid.UUID(guid_str)
            node = client.get_node(ua.NodeId(node_guid, namespace_idx))



        # Create DataValue and write the new value
        dv = ua.DataValue()
        dv.Value = ua.Variant(value_to_write, ua.VariantType.Boolean)  
        node.set_value(dv)

        return "Value written successfully"

    except Exception as e:
        return f"Error while writing: {e}"

    finally:
        client.disconnect()

# Define your available tools
tools = [opcua_read_variable, opcua_write_variable]

# Create your ChatOpenAI LLM and bind the tools to it
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

def assistant(state: MessagesState, actions: str) -> dict:
    """
    The main assistant function invoked by the StateGraph.
    It appends a SystemMessage containing 'actions' to the existing messages,
    then calls the language model with bound tools.
    """
    sys_msg = SystemMessage(content=actions)
    messages = state["messages"] if isinstance(state["messages"], list) else []
    result = llm_with_tools.invoke([sys_msg] + messages)
    return {
        "messages": [result],
        "myNmae": "midhun"  # Keeping the original key to match your code
    }

def set_opcua_graph(actions):
    builder = StateGraph(MessagesState)

    # Wrap assistant function to pass actions
    assistant_node = partial(assistant, actions=actions)

    builder.add_node("assistant", assistant_node)  # Pass function reference, not a dictionary
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    # Compile the graph
    react_graph = builder.compile()
    return react_graph
