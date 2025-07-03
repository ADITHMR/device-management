import picoweb
# import network
import time
import ujson as json
import urequests
import machine
import gc

from local_host.get_project_html import get_project_html
from local_host.web_page import web_page, successProjectPage, message_page, errorPage
from utils import url_decode,put_jsonvalue_to_file,get_jsonvalue_from_file,load_url
from local_host.project_config_update import update_project_config

# Create Picoweb app
app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
#     print(gc.mem_free())
#     gc.collect()
#     print(gc.mem_free())
#     print(load_url("https://raw.githubusercontent.com/ADITHMR/probots_micropython/refs/heads/device_branch/version.dat"))
    if req.method == "GET":
        try:
            with open("local_host/index_page.html", 'r') as f:
                yield from picoweb.start_response(resp)
                while True:
                    chunk = f.read(512)  # Read in small chunks
                    if not chunk:
                        break
                    yield from resp.awrite(chunk)
        except Exception as e:
            print("Error loading index page:", e)
        finally:
            gc.collect()
    else:
        try:
            yield from req.read_form_data()
            project = req.form.get("selectedItem", "no data")
           
            put_jsonvalue_to_file("schema.dat","PROJECT",project)
            
            response = message_page(f'''
    <h3>You have selected</h3>
    <h2 class="text-success">{project}</h2>
    <a href="/restart" class="btn btn-danger">Restart the system</a>
    ''')
            yield from picoweb.start_response(resp)
            yield from resp.awrite(response)

#             with open(path, 'r') as f:
#                 yield from picoweb.start_response(resp)
#                 while True:
#                     chunk = f.read(512)  # Read in small chunks
#                     if not chunk:
#                         break
#                     yield from resp.awrite(chunk)
        except Exception as e:
            print("Error loading index page:", e)
        finally:
            del response,project
            gc.collect()
@app.route("/config")
def config(req, resp):
    if req.method == "GET":
        try:
            with open("local_host/config_page.html", 'r') as f:
                yield from picoweb.start_response(resp)
                while True:
                    chunk = f.read(512)  # Read in small chunks
                    if not chunk:
                        break
                    yield from resp.awrite(chunk)
        except Exception as e:
            print("Error loading index page:", e)
        finally:
            gc.collect()
    else:
        try:
            yield from req.read_form_data()
            project = req.form.get("selectedItem", "no data")
            path = get_project_html(project)

            with open(path, 'r') as f:
                yield from picoweb.start_response(resp)
                while True:
                    chunk = f.read(512)  # Read in small chunks
                    if not chunk:
                        break
                    yield from resp.awrite(chunk)
        except Exception as e:
            print("Error loading index page:", e)
        finally:
            gc.collect()
        

@app.route("/checkUpdate")
def check_update(req, resp):
#     with open('version.dat', 'r') as f:
#         html_content = json.load(f)
#         html_path = str(html_content["version_path"])
#         print(html_path)
    url ="https://example-files.online-convert.com/document/txt/example.txt"
#     url ="https://raw.githubusercontent.com/ADITHMR/probots_micropython/refs/heads/device_branch/version.dat"
    #"http://google.com/"#"https://raw.githubusercontent.com/ADITHMR/probots_micropython/refs/heads/device_branch/version.dat" #html_path#"https://jsonplaceholder.typicode.com/todos/1"  # Replace with your desired URL
    
    try:
        response = message_page('''
            <h1--------------------------</h1>
            <h2> Page Under Process</h2>
            
            ''')

#         response = urequests.get(url)
#         data = response.text  # Get response as text
#         response.close()  # Always close response to free memory
    except Exception as e:
        response = "Error fetching data: " + str(e)
    yield from picoweb.start_response(resp)
    yield from resp.awrite(response)  # Send fetched data as response
#     try:
#         gc.collect()
#         with open('version.dat', 'r') as f:
#             html_content = json.load(f)
# 
#         version_now = html_content["version"]
#         html_path = html_content["version_path"]
#         gc.collect()
# 
#         response_data = load_url(html_path)
#         response_data = json.loads(response_data)  # Decode properly
#       
# 
#         latest_version = data["version"]
#         del response_data
#         if latest_version == version_now:
#             response = message_page("<h2> You are up to date!</h2>")
#         else:
#             response = message_page('''
#             <h1>Update available.</h1>
#             <h2> Do you want to update device?</h2>
#             <a href="/updatenow" class="btn btn-warning">Update Now</a>
#             ''')
# 
#         yield from picoweb.start_response(resp)
#         yield from resp.awrite(response)
# 
#     except Exception as e:
#         print(f"Error in check_update(): {e}")
#         response = errorPage
# 
#     finally:
#         gc.collect()  # Free memory


@app.route("/updatenow")
def update_now(req, resp):
    try:
        with open('schema.dat', 'r+') as f:
            schema = json.load(f)
            schema["update_flag"] = "True"
            f.seek(0)
            json.dump(schema, f)
            f.truncate()

        response = message_page('''
        <h2>Update Initiated...</h2>
        <h1 class="text-danger">Press the reset button to proceed with the update...</h1>
        <h2 class="text-danger">Do not interrupt the update process.</h2>''')

        yield from picoweb.start_response(resp)
        yield from resp.awrite(response)
    except Exception as e:
        print(f"Error in update_now(): {e}")
    finally:
        del response
        gc.collect()

@app.route("/restart")
def restart(req, resp):
    response = message_page("<h2 class='text-danger'>Device restarted successfully</h2>")

    yield from picoweb.start_response(resp)
    yield from resp.awrite(response)
    
    time.sleep(0.1)
    machine.reset()

@app.route("/project", methods=["POST"])
def submit(req, resp):
    yield from req.read_form_data()
    data = req.form
    data_str = json.dumps(data)  # Avoid unnecessary conversion back and forth
    json_data = json.loads(data_str)

    update_project_config(json_data)

    response = message_page(f'''
    <h3>You have updated config for </h3>
    <h2 class="text-success">{data.get('project', 'Unknown')}</h2>
    <a class="btn btn-primary" href="/config">Back</a>
    ''')

    yield from picoweb.start_response(resp)
    yield from resp.awrite(response)

    del response
    gc.collect()

@micropython.native
def runWebServer():
    import uasyncio
    try:
        
        uasyncio.run(app.run(debug=True, host="0.0.0.0", port=80))
    except Exception as e:
        print("Error in runWebServer():", e)
    finally:
        gc.collect()
