import json


def set_parameter(parameter,value):
    with open('config.txt', 'r') as f: 
        data = json.load(f)
        if parameter in data:
            try:
                data[parameter]=str(value)
            except :
                return "Data format error"
            with open('config.txt', 'w') as f:
                json.dump(data, f)
                print("Data storedf in config.txt")
            read_data=get_parameter(parameter)
#                 return(f"-{type(read_data)}-{type(value)}")
            if read_data== str(value):
                return "OK"
            else:
                return "Error Saving Data"
        else: return f"Error 404: No parameter named {parameter}"
def get_parameter(parameter):
        with open('config.txt', 'r') as f:
            data= json.load(f)
            if parameter in data:
                result=data[parameter].replace("'","")
                return  (result)
                
            else:
                return "Error 404: No Such Parameter Found"



def get_project_config_data(project_name):
    try:
        # Read the current configurations from the file
        with open('projects/project_configurations.txt', 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print("The configuration file does not exist.")
    except json.JSONDecodeError:
        print("Error decoding the JSON configuration file.")
    except Exception as e:
        print(f"An error occurred: {e}")
#     data_str=json.loads(json_data)
    if project_name in json_data:
        return json_data[project_name]
    
    