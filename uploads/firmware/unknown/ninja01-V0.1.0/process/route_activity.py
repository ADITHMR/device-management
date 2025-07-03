import ujson as json
import gc

def route_activity(activity_name):
    with open('project/project_routing.json', 'r') as f:
        data = json.load(f)
    
    activity=data[activity_name]
    del data
    gc.collect()
    return (activity)
                    
