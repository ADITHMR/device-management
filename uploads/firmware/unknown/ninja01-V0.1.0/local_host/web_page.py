import gc
import machine
import uio  # Optimized file I/O for MicroPython
from machine_id import get_serial_no
from utils import write_file

@micropython.native
def web_page(project_topic_list):
    try:
        # Generate HTML dropdown as a single string
        html_dropdown = (
            '<select id="mydropdown" name="selectedItem" class="form-select" required>\n'
            '<option value="">--Select Project--</option>\n' +
            ''.join(f'<option value="{proj}">{proj}</option>\n' for proj in project_topic_list) +
            '</select>'
        )

        serial_no = get_serial_no()

        # Process index.html
        _process_template('local_host/index.html', 'local_host/index_page.html', html_dropdown, serial_no)

        # Process config.html
        _process_template('local_host/config.html', 'local_host/config_page.html', html_dropdown, serial_no)

    except Exception as e:
        print("Error: on web_page()", e)

    finally:
        gc.collect()

@micropython.native
def _process_template(input_path, output_path, dropdown, serial_no):
    try:
        with open(input_path, 'r') as f:
            content = f.read()

        content = content.replace("{html_dropdown}", dropdown)
        content = content.replace("{*Serial No*}", serial_no)
        content = content.replace("{machine_id}", f"S/N: {serial_no}")

        write_file(output_path, content)
        
    finally:
        del content
        gc.collect()

@micropython.native
def successProjectPage(data):
    return _read_and_replace('local_host/project_sel_success.html', "{data}", data)

@micropython.native
def errorPage():
    return _read_file('local_host/error404.html')

@micropython.native
def restartSuccessPage():
    return _read_file('local_host/restart_success_page.html')

@micropython.native
def message_page(message):
    serial_no = get_serial_no()
    return _read_and_replace('local_host/message.html', "{message}", message, "{machine_id}", f"S/N: {serial_no}")

# Helper function to read a file and replace placeholders
@micropython.native
def _read_and_replace(filepath, *replace_pairs):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        for i in range(0, len(replace_pairs), 2):
            content = content.replace(replace_pairs[i], replace_pairs[i + 1])

        return content
        
    finally:
        gc.collect()

# Helper function to read a file
@micropython.native
def _read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
        
    finally:
        gc.collect()
