# Beagle

Beagle is a tool that lets you locally search your browsing history.

## Installation

1. Clone this repo and navigate to it 
2. Create a virtual environment with `python3 -m venv venv`
3. Start the virtual environment with `source venv/bin/activate`
3. Install python packages `pip install -r requirements.txt`
4. Run the server `python server.py`
5. Go to `chrome://extensions` in your chromium based browser
6. Activate developer mode and click `Load unpacked`
7. Select the `extension` folder from this repository 

## Usage

1. Close and reopen your browser. This lets Beagle create an index of existing tabs. Otherwise you'll only be able to search pages you visit after Beagle was installed.
2. Ensure the server is running in a terminal using the instructions from the installation. On MacOS you can minimize the terminal window to keep it out of the way.
3. Click on the Beagle extension icon from your browser
4. Search!
