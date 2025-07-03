import ujson as json
#        01 Fun with LED Lights
@micropython.native 
def get_project_html(project_name):
    
    with open('project/project_routing.json', 'r') as f:
        activity = json.load(f)
    if project_name in activity:
        path=f"html/{activity[project_name]}.html"
        
#         with open(path, 'r') as f:
#             page = f.read()
        return path
       
           
        
