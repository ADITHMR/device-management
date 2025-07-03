import os
import json

def list_files_and_folders(directory):
    folder_files = []

    # List files and directories directly in the specified directory
    try:
        # List contents of the directory
        entries = os.listdir(directory)
        
        # Separate files and folders
        files_in_current_dir = []
        subfolders = []
        
        for entry in entries:
            entry_path = directory + '/' + entry
            
            try:
                # Try to list files in the directory (only directories will succeed)
                sub_files = os.listdir(entry_path)
                subfolders.append({
                    "folder": entry_path,
                    "files": sub_files
                })
            except OSError:
                # If listing failed, this is a file in the current directory
                files_in_current_dir.append(entry)

        # Add the files in the current directory to the list (if any)
        if files_in_current_dir:
            folder_files.append({
                "folder": directory,
                "files": files_in_current_dir
            })

        # Add subfolders to the list (if any)
        if subfolders:
            folder_files.extend(subfolders)
    
    except Exception as e:
        print("Error:", e)

    return folder_files

def json_dumps_pretty(data):
    # Custom function to pretty-print JSON with indentation
    json_string = json.dumps(data)
    indented_string = ""
    level = 0

    for char in json_string:
        if char == '{' or char == '[':
            indented_string += char + "\n" + "    " * (level + 1)
            level += 1
        elif char == '}' or char == ']':
            level -= 1
            indented_string += "\n" + "    " * level + char
        elif char == ',':
            indented_string += char + "\n" + "    " * level
        else:
            indented_string += char

    return indented_string

def save_json_to_file(data, filename):
    # Save the JSON data to a file
    with open(filename, 'w') as file:
        # Write the encoded byte string to the file
        file.write(data.encode('utf-8'))  # Encoding to bytes

    print(f"File saved to: {filename}")

# Replace with your directory path (e.g., '/sd' if using an SD card)
directory_path = '/'

# Get the list of folder and file names
folder_file_list = list_files_and_folders(directory_path)
folder_file_list.append(folder_file_list.pop(0))
json_data = json_dumps_pretty(folder_file_list)
# Pretty-print the result (since MicroPython doesn't support indent in json.dumps)


# Save the JSON output to a file
output_filename = 'files_list.txt'  # Adjust the path as needed (without .json)
save_json_to_file(json_data, output_filename)
