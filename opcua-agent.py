import streamlit as st
import json
import pandas as pd
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
    st.session_state["connection_string"] = "opc.tcp://18.212.12.234:4840/freeopcua/server/"
if "agent_instructions" not in st.session_state:
    st.session_state["agent_instructions"] = (
        """System Description:
This is an industrial automation system controlled via an OPC UA server. The system consists of sensors that monitor key operational parameters and actuators that allow external control. The AI agent can read sensor values and modify actuator states to control the system dynamically.

System Components & Variables:
1. Sensors (Read-Only)
Temperature Sensor (Temperature)

Measures system temperature in °C (Celsius).
Temperature increases when the motor is ON.
Temperature decreases when the motor is OFF.
Normal operating range: 20°C - 100°C.
Pressure Sensor (Pressure)

Measures system pressure in bar.
Pressure increases when the valve is CLOSED.
Pressure decreases when the valve is OPEN.
Operating range: 0.5 - 5.0 bar.
Motor Speed Sensor (MotorSpeed)

Measures motor speed in RPM (Revolutions Per Minute).
Motor speed increases when the motor is ON.
Motor speed decreases when the motor is OFF.
Max motor speed: 3000 RPM.
2. Actuators (Writeable - Can be Controlled by AI)
Motor State (MotorState)

Controls whether the motor is ON or OFF.
TRUE → Motor is ON (Speed and Temperature increase).
FALSE → Motor is OFF (Speed and Temperature decrease).
Can be modified by AI to start or stop the motor.
Valve Position (ValvePosition)

Controls whether the valve is OPEN or CLOSED.
TRUE → Valve is OPEN (Pressure decreases).
FALSE → Valve is CLOSED (Pressure increases).
Can be modified by AI to regulate pressure.
AI Agent Capabilities:
The AI agent can interpret and execute user commands to control the system. Here are some examples:

Start/Stop the Motor:

"Turn ON the motor." → Sets MotorState = TRUE.
"Stop the motor." → Sets MotorState = FALSE.
Check System Status:

"What is the current temperature?" → Reads Temperature.
"How fast is the motor running?" → Reads MotorSpeed.
"What is the current pressure level?" → Reads Pressure.
Control the Valve:

"Open the valve to decrease pressure." → Sets ValvePosition = TRUE.
"Close the valve to increase pressure." → Sets ValvePosition = FALSE.
"""
    )



# Fetch variables from the OPC UA server
def fetch_variables():
    opcua_variables = find_variables_by_endpoint(st.session_state["connection_string"])
    if opcua_variables:
        st.session_state["opcua_variables"] = {
            var["name"]: {
                "value": var["value"],
            }
            for var in opcua_variables
        }
        # Update the table format
        st.session_state["variable_table"] = pd.DataFrame(
            [[name, info["value"]] for name, info in st.session_state["opcua_variables"].items()],
            columns=["Variable Name", "Value"]
        )
        st.success("✅ Variables fetched successfully! Use OPC UA client for realtime analysis")
    else:
        st.session_state["variable_table"] = None
        st.warning("⚠ No variables found or an error occurred.")

# Sidebar: Refresh Variables Button
if st.button("🔄 Refresh Variables"):
    fetch_variables()

# Sidebar: Connection String Input
st.sidebar.subheader("🔗 Connection Setup")
st.session_state["connection_string"] = st.sidebar.text_input(
    "Enter OPC UA Connection String", 
    st.session_state["connection_string"]
)
st.sidebar.write("Default opc ua server has been deployed to the cloud for testing purpose.")

if st.sidebar.button("Connect"):
    # Find variables instead of methods
    variables = find_variables_by_endpoint(st.session_state["connection_string"])
    fetch_variables()
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





# Display the variable table if available
if "variable_table" in st.session_state and st.session_state["variable_table"] is not None:
    st.subheader("📊 OPC UA Variables")
    st.dataframe(st.session_state["variable_table"])
else:
    st.write("No variables to display.")


# Sidebar: Display Unsaved Variables
st.sidebar.subheader("📌 Available Variables")
for var_name, var_info in list(st.session_state["variables"].items()):
    with st.sidebar.expander(var_name, expanded=True):
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
        st.button("Deploy your Agent - Coming soon!")
        st.download_button(
            label="Download config",
            data=json.dumps(st.session_state["saved_variables"]),
            file_name="variables.json",
            mime="application/json"
        )
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
                st.button("save workflow coming soon!")


st.sidebar.write("Made with ❤️ by Midhun Xavier")
st.sidebar.write("website :  www.midhunxavier.com")
st.sidebar.write("Email : midhun.xavier@ltu.se")
