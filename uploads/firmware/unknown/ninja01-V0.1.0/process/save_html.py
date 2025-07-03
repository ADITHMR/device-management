import json
import gc
from machine_id import get_serial_no
from utils import (
    get_jsonvalue_from_file,
    read_file,
    write_file,
    file_exists,
)
from drivers.oled import oled_log, oled_two_data


def save_html():
    try:
        gc.collect()  # Initial cleanup
        folders = ["activity1", "activity2", "activity3", "activity4", "activity5"]
#         project_page = read_file("local_host/project_page.html")  # Load template once

        progress = 0
        for folder in folders:
            web_items_path = f"{folder}/web_data.html"
            config_items_path = f"{folder}/config.txt"
            output_path = f"html/{folder}.html"
            temp_file1 = "temp1.txt"
            temp_file2 = "temp2.txt"
            if file_exists(web_items_path) and file_exists(config_items_path):
                # Load JSON data
                gc.collect()
                web_items_list = get_jsonvalue_from_file(web_items_path, "data")
                project_name = get_jsonvalue_from_file(config_items_path, "project_name")
                # Progress update
                progress += 5
                print(f"Progress: {progress}%")
                oled_two_data( 1, 2, "Saving Pages",  f"{progress}%")
                print(gc.mem_free())
                if web_items_list != "error" and project_name != "error":
                    web_items_list_modified = json.dumps(web_items_list)  # JSON format
                    description = get_jsonvalue_from_file("project/project_description.dat", folder)
                    with open("local_host/project_page.html", "r") as fr, open(temp_file1, "w") as fw:
                        for line in fr:
                            fw.write(line.replace('{config_list}', web_items_list_modified))  # Replace while writing
                            gc.collect()  # Free memory after each line
                        del fr,fw
                        gc.collect()
                    # Progress update
                    progress += 5
                    print(f"Progress: {progress}%")
                    oled_two_data( 1, 2, "Saving Pages",  f"{progress}%")
                    print(gc.mem_free())
                    with open(temp_file1, "r") as fr, open(temp_file2, "w") as fw:
                        for line in fr:
                            fw.write(line.replace('{heading}', project_name))  # Replace while writing
                            gc.collect()  # Free memory after each line
                        del fr,fw
                        gc.collect()
                    # Progress update
                    progress += 5
                    print(f"Progress: {progress}%")
                    oled_two_data( 1, 2, "Saving Pages",  f"{progress}%")
                    print(gc.mem_free())
                    with open(temp_file2, "r") as fr, open(output_path, "w") as fw:
                        for line in fr:
                            fw.write(line.replace('{description}', description))  # Replace while writing
                            gc.collect()  # Free memory after each line
                        del fr,fw
                        gc.collect()
                    # Progress update
                    progress += 5
                    print(f"Progress: {progress}%")
                    oled_two_data( 1, 2, "Saving Pages",  f"{progress}%")
                    print(gc.mem_free())
                            
#                     def generate_response():
#                         for line in project_page.splitlines():
#                             line = line.replace('{config_list}', web_items_list_modified)
#                             line = line.replace('{heading}', project_name)
#                             line = line.replace('{description}', description)
#                             yield line + "\n"  # Send one line at a time
#                     response = "".join(generate_response()) # Response is now a generator (low RAM usage)

                    # Generate response
#                     response = project_page.replace('{*config_list*}', web_items_list_modified)
#                     response = response.replace('{*heading*}', project_name)
#                     response = response.replace('{description}', description)
                    

                    # Write output file
#                     write_file(output_path, response)

                    # Free memory after processing each activity
                    del web_items_list, project_name, web_items_list_modified, description
                    gc.collect()

                    # Progress update
#                     progress += 20
#                     print(f"Progress: {progress}%")
#                     oled_two_data(1, 1, 2, "Saving Pages", "Pages", f"{progress}%")

        
        gc.collect()

    except Exception as e:
        print("Error in save_html():", e)

    try:
        gc.collect()
        oled_log("Saved index.html")
        oled_log("Saved all html files")
        print("Successfully saved HTML files...")
    except Exception as e:
        print("Error in save_html() on index page:", e)
