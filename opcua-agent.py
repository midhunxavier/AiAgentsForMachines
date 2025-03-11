import streamlit as st
import json

# Replace with your actual import that finds variables
# Example: from client.findVariablesByEndpoint import find_variables_by_endpoint
from client.findVariablesByEndpoint import find_variables_by_endpoint

# Replace with your own workflow/graph logic
from OPCUA_EXE.opcua_graph import set_opcua_graph
from langchain_core.messages import HumanMessage

# Initialize session state for storing variables and chat visibility
if "variables" not in st.session_state:
    st.session_state["variables"] = {}
if "saved_variables" not in st.session_state:
    st.session_state["saved_variables"] = {}
if "chat_visible" not in st.session_state:
    st.session_state["chat_visible"] = False
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "agent_started" not in st.session_state:
    st.session_state["agent_started"] = False
if "connection_string" not in st.session_state:
    st.session_state["connection_string"] = "opc.tcp://localhost:4840/freeopcua/server/"
if "agent_instructions" not in st.session_state:
    st.session_state["agent_instructions"] = (
        """Rotating Arm Control System
            You are an intelligent assistant responsible for controlling a ROTATING ARM in a factory environment using OPC UA variables. Your objective is to transfer workpieces from the left (magazine side) to the right (next processing station) by correctly reading sensor values and activating actuators.

            Rotating Arm Sensors:
            at_mgz: TRUE if the arm is positioned at the magazine (Left side).
            at_next: TRUE if the arm is at the next processing station (Right side).
            Rotating Arm Actuators:
            to_mgz: Moves the arm to the magazine side. Set to TRUE to start moving, then FALSE once it arrives.
            to_next: Moves the arm to the next processing station. Set to TRUE to start moving, then FALSE once it arrives.
            Task Execution Flow:
            Move the rotating arm to the magazine side if it's not already there.
            Move the rotating arm to the next processing station.
            Return the rotating arm to the magazine side to repeat the cycle.
            Your task is to control the ROTATING ARM efficiently while ensuring correct sensor readings and actuator commands.
            Exexcution constraints:
            1. Check the sensor value of before of at_mgz or at_next find the location ARM and then execute the ARM movement.

            """
    )

# Sidebar: Connection String Input
st.sidebar.subheader("🔗 Connection Setup")
st.session_state["connection_string"] = st.sidebar.text_input(
    "Enter OPC UA Connection String", 
    st.session_state["connection_string"]
)

if st.sidebar.button("Connect"):
    # Find variables instead of methods
    variables = find_variables_by_endpoint(st.session_state["connection_string"])
    if variables:
        for variable in variables:
            var_name = variable["name"]
            # Only add if it's not already in session state
            if var_name not in st.session_state["variables"] and var_name not in st.session_state["saved_variables"]:
                st.session_state["variables"][var_name] = {
                    "connection_string": st.session_state["connection_string"],
                    "object_id": variable["object_id"],
                    "nodeid": variable["nodeid"],
                    "description": variable["description"],
                    "value": variable["value"],
                    "data_type": variable["data_type"],
                }
    else:
        st.sidebar.write("No variables found or an error occurred.")

# Sidebar: Display Unsaved Variables
st.sidebar.subheader("📌 Available Variables")
for var_name, var_info in list(st.session_state["variables"].items()):
    with st.sidebar.expander(var_name, expanded=True):
        st.write(f"**Node ID:** {var_info['nodeid']}")
        st.write(f"**Data Type:** {var_info['data_type']}")
        st.write(f"**Current Value:** {var_info['value']}")
        st.write(f"**Description:** {var_info['description']}")
        if st.sidebar.button("Add to Agent environment", key=f"save_sidebar_{var_name}"):
            st.session_state["saved_variables"][var_name] = var_info
            del st.session_state["variables"][var_name]

# Main: Build Your AI Agent
st.subheader("📌 Build your AI agent")
st.session_state["agent_instructions"] = st.text_area(
    "Provide instructions for the AI Agent:",
    st.session_state["agent_instructions"],
    height=300
)

keys_to_remove = []

# Show the saved variables (those added to the Agent environment)
if st.session_state["saved_variables"]:
    for var_name, var_info in st.session_state["saved_variables"].items():
        with st.expander(var_name, expanded=True):
            st.write(f"**Object ID:** {var_info['object_id']}")
            st.write(f"**Node ID:** {var_info['nodeid']}")
            st.write(f"**Data Type:** {var_info['data_type']}")
            st.write(f"**Current Value:** {var_info['value']}")

            # Allow editing the description
            new_desc = st.text_area(
                "Edit Description", var_info['description'], 
                key=f"edit_{var_name}"
            )

            if st.button("Integrate", key=f"save_{var_name}"):
                st.session_state["saved_variables"][var_name]['description'] = new_desc
                st.write("Updated successfully!")

            if st.button("Remove", key=f"remove_{var_name}"):
                # Move back to sidebar
                st.session_state["variables"][var_name] = var_info
                keys_to_remove.append(var_name)

    # Remove any variables that were flagged for removal
    for key in keys_to_remove:
        del st.session_state["saved_variables"][key]

    # Toggle Chat / Configure
    button_label = "Test Agent" if not st.session_state["chat_visible"] else "Configure"
    if st.button(button_label):
        if not st.session_state["chat_visible"]:
            st.session_state["chat_visible"] = True
            st.session_state["messages"] = [{
                "role": "assistant", 
                "content": "AI Agent started with given config. How can I assist?"
            }]
            # Pass the variables in JSON form to your workflow function
            st.session_state["workflow"] = set_opcua_graph(json.dumps({
                "connection_string": st.session_state["connection_string"],
                "instructions": st.session_state["agent_instructions"],
                "variables": st.session_state["saved_variables"]
            }))
            print("Workflow set up with variables:", st.session_state["saved_variables"])
        else:
            st.session_state["chat_visible"] = False
            st.session_state["messages"] = []
            st.session_state.pop("workflow", None)

    # Display chat only if "Test Agent" is activated
    if st.session_state["chat_visible"]:
        st.title("📝 AI Agent")
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        # Chat Input
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            workflow = st.session_state.get("workflow")
            if workflow:
                # Example: streaming or direct call to workflow
                for event in workflow.stream({"messages": ("user", prompt), "recursion_limit": 5}):
                    for value in event.values():
                        response = value["messages"][-1].content
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.chat_message("assistant").write(response)
