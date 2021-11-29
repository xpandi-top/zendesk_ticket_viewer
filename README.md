# Zendesk Ticket Viewer
client viewer for the tickets in the zendesk

## Installation
1. Install prerequisites
    - Install [python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/)
    - For Linux/Mac, python3 is most likely already installed, use below command to verify
    - python: `python --version`
    - pip: `pip --version`
2. Install required dependency
    - Under package directory, run `pip install -r requirements.txt`
## Usage
1. Fill in required config in `config.ini`
    - Sign up at [zendesk](https://www.zendesk.com/register#getstarted) to get a free trial account if you haven't
    - Go to `config.ini` under package root, fill in your email, password and Zendesk domain, and save the file

2. start the script then go to the main view of ticket viewer
    - In the terminal Enter `python3 TicketViews.py` and you would enter the ticket viewer

3. Main view
    - type 'quit' to exit the application
    - type 'help' to show the instructions
    - type 'list' to enter the view of ticket list
    - Enter a number to go to ticket detail view for a ticket you want

4. Ticket list view
    - Type 'n' for next page
    - Type 'p' for previous page
    - Type 'curr' for current page
    - Type page+number to go to individual page
    - Type 'help' to display this message
    - Type 'back' to exit the tickets list view and back to main menu
    - Type 'quit' to exit the application
    - Enter number to a single ticket by id

5. Ticket detail view
    - Type 'n' for next ticket
    - Type 'p' for previous ticket
    - Type 'curr' for curr ticket
    - Type number of a ticket id to go to a ticket
    - Type 'back' to exit the tickets view and back to main menu
    - Type 'quit' to exit the application
    - Type 'help' to display this message

## Testing
Unit test cases are located at `unit_test.py`.
- Tests can be ran locally by `python3 -m unittest unit_test.py`
- This GitHub repository is setup to run unit tests automatically, on each new commit to `origin/master`. View test result [here](https://github.com/xpandi-top/zendesk_ticket_viewer/actions)
