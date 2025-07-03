#
# This is a picoweb example showing a centralized web page route
# specification (classical Django style).
#
import ure as re
import picoweb
import uasyncio as asyncio
from local_host.connect_wifi import connect_wifi
from local_host.web_page import web_page


connect_wifi()
app = picoweb.WebApp(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index(req, resp):
#     yield from resp.awrite(web_page())

@app.route('/', methods=['GET', 'POST'])
def index(req, resp):
    if req.method == 'POST':
        # Reading form data
        form_data = yield from req.read_form_data()
        # Assume a form field named 'name' is being submitted
        name = form_data.get('name', [''])[0]  # Default to empty string if no data
        
        # Process the form data (you can print, store, or use it as needed)
        print(f"Received name: {name}")
        
        # Respond to user
        yield from resp.awrite(f"<h1>Hello, {name}!</h1>")
    else:
        # Handle GET request by serving the HTML page with a form
        html_form = """
        <html>
            <body>
                <h1>Enter your name</h1>
                <form method="POST" action="/">
                    <input type="text" name="name" placeholder="Your name">
                    <button type="submit">Submit</button>
                </form>
            </body>
        </html>
        """
        yield from resp.awrite(html_form)

@app.route('/hello')
def hello(req, resp):
    yield from resp.awrite('Hello, from another page!')

def run_server():
    asyncio.run(app.run(debug=1, host='0.0.0.0', port=80))

run_server()