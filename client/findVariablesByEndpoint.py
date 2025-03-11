from opcua import Client
from opcua.ua import NodeClass
import json

def find_variables_by_endpoint(endpoint):
    """
    Connects to an OPC UA server and finds all available variables,
    excluding those that are under the built-in 'Server' object.
    
    Args:
        endpoint (str): The full OPC UA connection string 
                        (e.g., opc.tcp://localhost:4840/freeopcua/server/).
    
    Returns:
        list of dict: Each dict contains the variable's 'name', 
                      'nodeid', 'object_id', 'value', 'data_type', 
                      and 'description'.
    """
    client = Client(endpoint)
    variables_info = []
    
    try:
        client.connect()
        print(f"Connected to OPC UA Server at {endpoint}")

        objects_node = client.get_objects_node()

        def search_variables(node):
            try:
                children = node.get_children()
            except Exception:
                return

            for child in children:
                try:
                    node_class = child.get_node_class()
                except Exception:
                    continue

                # --- Skip the entire "Server" subtree ---
                # If this child's browse name is "Server", we don't go further.
                child_browse_name = child.get_browse_name().Name
                if child_browse_name == "Server":
                    continue

                if node_class == NodeClass.Variable:
                    browse_name = child_browse_name
                    node_id = child.nodeid.to_string()
                    
                    try:
                        parent_node = child.get_parent()
                        object_id = parent_node.nodeid.to_string() if parent_node else "N/A"
                    except Exception:
                        object_id = "N/A"

                    try:
                        value = child.get_value()
                    except Exception:
                        value = None

                    try:
                        data_type = child.get_data_type().to_string()
                    except Exception:
                        data_type = ""

                    try:
                        desc = child.get_description().Text
                    except Exception:
                        desc = ""
                    
                    variables_info.append({
                        "name": browse_name,
                        "nodeid": node_id,
                        "object_id": object_id,
                        "value": value,
                        "data_type": data_type,
                        "description": desc
                    })
                elif node_class == NodeClass.Object:
                    # Recursively search children of this object,
                    # unless it is the "Server" object.
                    search_variables(child)

        search_variables(objects_node)
        return variables_info
    except Exception as e:
        print("An error occurred while finding variables:", e)
        return []
    finally:
        client.disconnect()
        print("Disconnected from OPC UA Server.")

if __name__ == "__main__":
    endpoint = "opc.tcp://B6426.ltuad.ltu.se:4840"
    variables = find_variables_by_endpoint(endpoint)
    # Convert to JSON, skipping non-serializable types by defaulting to string
    json_data = json.dumps(variables, default=str)
    print(json_data)
