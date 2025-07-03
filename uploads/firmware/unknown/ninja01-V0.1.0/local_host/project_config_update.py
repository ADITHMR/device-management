import ujson as json  # Use MicroPython's lightweight JSON parser
from process.route_activity import route_activity
from utils import url_decode, put_jsonvalue_to_file
from process.file_mgr import set_parameter

def update_project_config(conf_list):
    try:
        proj_name = url_decode(conf_list.get('project', ''))  # Use .get() to avoid KeyError
        if not proj_name:
            print("Error: No project name provided.")
            return

        activity_name = route_activity(proj_name)
        print(activity_name)

        path = f"{activity_name}/config.txt"

        # Read existing config data efficiently
        conf_data = {}
        try:
            with open(path, 'r') as f:
                conf_data = json.load(f)  # ujson consumes less memory than json
        except (OSError, ValueError) as e:
            print(f"Error reading config file: {e}")
            return  # Prevent further execution if file is missing or corrupted

        print(conf_data)

        # Update project configuration
        for conf, value in conf_list.items():
            decoded_value = url_decode(value)
            if conf == 'project':
                pass
            else:
                conf_data.setdefault("params", {})[conf] = decoded_value  # Use .setdefault() to avoid KeyError

        print(conf_data)

        # Write updated config efficiently
        try:
            with open(path, 'w') as f:
                json.dump(conf_data, f)
        except OSError as e:
            print(f"Error writing to config file: {e}")
            return

        print(f"Configuration for project '{proj_name}' has been updated successfully.")

        # Clean up large variables
        del conf_data

    except Exception as e:
        print(f"An error occurred in 'update_project_config(conf_list)': {e}")
