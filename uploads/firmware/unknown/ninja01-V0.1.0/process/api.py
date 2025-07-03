import urequests
import ujson  # MicroPython-optimized JSON
import gc
from local_host.connect_wifi import connect_wifi
from utils import get_jsonvalue_from_file, put_jsonvalue_to_file, write_file
from project.projectList import project_topic_list
from drivers.oled import oled_three_data
from local_host.web_page import web_page

class Api:
    user_login_url = "http://roboninjaz.com:8010/api/user/login"
    get_projects_url = "http://roboninjaz.com:8010/api/projects/getAllacquired-projects"
    get_projectfile_url = "http://roboninjaz.com:8010/api/projects/download/"
    
    def __init__(self):
        self.username = get_jsonvalue_from_file("schema.dat", "username")
        self.password = get_jsonvalue_from_file("schema.dat", "password")
        self.auth_header = {"Authorization": "Bearer 0", "Content-Type": "application/json"}

    def user_login(self):
        data = ujson.dumps({"email": self.username, "password": self.password})
        response = None
        try:
            response = urequests.post(self.user_login_url, data=data, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                response_data = response.json()
                token = response_data["token"]
                user = response_data["user"]["username"]
                
                put_jsonvalue_to_file("schema.dat", "token", token)
                put_jsonvalue_to_file("schema.dat", "user", user)
                self.auth_header["Authorization"] = "Bearer {}".format(token)
                
                print("Login successful:", user)
                return True
            else:
                print("Login failed:", response.status_code)
                return False
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            if response:
                response.close()  # Close connection to free memory
                gc.collect()

    def get_projects(self):
        token = get_jsonvalue_from_file("schema.dat", "token")
        if token == "0":
            return False

        response = None
        try:
            response = urequests.get(self.get_projects_url, headers=self.auth_header)
            if response.status_code == 200:
                projects = response.json().get("projects", [])
                self.save_projects(projects)
                return True
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            if response:
                response.close()  # Close connection
                gc.collect()

    def save_projects(self, projects):
        if not projects:
            return

        project_routing_json = {}
        folders = ["activity1", "activity2", "activity3", "activity4", "activity5"]
        progress = 0
        inc = 100 / (len(projects) * 3)

        for i, project in enumerate(projects):
            if i >= len(folders):
                break  # Prevent out-of-range errors

            put_jsonvalue_to_file("project/project_description.dat", folders[i], project['description'])
            
            for file in project["files"]:
                file_path = "{}/{}".format(folders[i], file['filename'].split('-')[1])
                file_content = self.get_project_file(file['id'])
                
                if file_content != "0":
                    with open(file_path, 'w') as f:
                        f.write(file_content)

                    progress += inc
                    oled_three_data(1, 1, 2, "Acquiring", "Projects", "{}%".format(round(progress)))
                    print("Saved {} to {}".format(file['id'], file_path))

                del file_content
                gc.collect()

            file_path = "{}/config.txt".format(folders[i])
            project_name = get_jsonvalue_from_file(file_path, "project_name")
            project_routing_json[project_name] = folders[i]

        write_file("project/project_routing.json", ujson.dumps(project_routing_json))
        
        project_list = list(project_routing_json.keys())
        write_file("project/projectList.py", "project_topic_list = {}".format(project_list))
        
        web_page(project_list)

        selected_proj = get_jsonvalue_from_file("schema.dat", "PROJECT")
        if selected_proj not in project_list:
            put_jsonvalue_to_file("schema.dat", "PROJECT", project_list[0] if project_list else "None")

    def get_project_file(self, file_id):
        response = None
        try:
            response = urequests.get("{}{}".format(self.get_projectfile_url, file_id), headers=self.auth_header)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print("Error:", e)
        finally:
            if response:
                response.close()  # Ensure connection is closed
                gc.collect()
        return "0"
