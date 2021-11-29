
import requests
from tabulate import tabulate
import configparser


class Ticket:
    """
    This class corresponds to the entity of ticket in zendesk system.
    This class handles ticket lifecycle and all ticket-specific actions like formatting.
    """
    tickets_list_headers = ['id', "subject", 'created_at', 'updated_at', 'priority', 'status']
    tickets_detail_headers = ['id', 'created_at', 'updated_at', 'type', 'subject', 'priority',
                              'status', 'requester_id', 'submitter_id', 'description']

    def __init__(self, ticket):
        self.ticket = ticket

    def print_ticket(self):
        for val in Ticket.tickets_detail_headers:
            print("    " + val.upper() + " " * (14 - len(val)) + ":" + str(self.ticket[val]))

    def get_info(self):
        return [self.ticket[val] for val in Ticket.tickets_list_headers]


class TicketView:
    """
    TicketView class handle session for viewing individual tickets.
    This class maintain a current ticket "pointer" and update it when user navigate through tickets.
    """
    def __init__(self, config, ticket_id, prompt="ticket> "):
        self.help = """===========================================
    This is Ticket View
    * Type 'n' for next ticket
    * Type 'p' for previous ticket
    * Type 'curr' for curr ticket
    * Type number of a ticket id to go to a ticket
    * Type 'quit' to exit the application
    * Type 'back' to exit this view and back to previous view
    * Type 'help' to display this message
==========================================="""
        self.base_url = config["Domain"] + "/api/v2/tickets/{}.json"
        self.ticket_id = ticket_id
        self.ticket = None
        self.prompt = prompt
        self.email = config["Email"]
        self.password = config["Password"]

        print(self.help)
        self.fetch_ticket(ticket_id)

    def fetch_ticket(self, ticket_id):
        url = self.base_url.format(ticket_id)
        response = requests.get(url, auth=(self.email, self.password))
        if response.status_code == 200:
            self.ticket = Ticket(response.json()['ticket'])
            self.ticket.print_ticket()
            self.ticket_id = ticket_id
        elif response.status_code == 401:
            print("Not Authorized! Please check your credentials")
        else:
            print("Oops. Ticket not %d found" % ticket_id)

    def start(self):
        shorten_help = "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket "
        while True:
            print("-"*10)
            print(shorten_help)
            single_ticket_input = input(self.prompt)
            if single_ticket_input == "help":
                print(self.help)
            if single_ticket_input == "n":
                print("fetching next ticket")
                self.fetch_ticket(self.ticket_id + 1)
            elif single_ticket_input == "p":
                print("fetching previous ticket")
                self.fetch_ticket(self.ticket_id - 1)
            elif single_ticket_input == "curr":
                self.ticket.print_ticket()
            elif single_ticket_input == "back":
                print("Going back to ticket list")
                return
            elif single_ticket_input == "quit":
                exit()
            else:
                try:
                    ticket_id = int(single_ticket_input)
                    self.fetch_ticket(ticket_id)
                except ValueError:
                    print(single_ticket_input, "is not a valid ticket id!")


class TicketListView:
    """
    TicketListView class handle session for viewing ticket list.
    This class maintain a current list "pointer" and update it when user navigate through ticket list.
    """
    def __init__(self, config, page, prompt="menu/ticket_list> "):
        self.ticket_list = []
        self.prompt = prompt
        self.abort = False
        self.base_url = config["Domain"] + "/api/v2/tickets.json?per_page=25&page={}"
        self.page = 1
        self.email = config["Email"]
        self.password = config["Password"]
        self.config = config

        while True:
            load_ = input("Are you going to load tickets? yes or no\n" + self.prompt)
            if load_ == "yes":
                break
            elif load_ == 'no':
                self.abort = True
                return
        self.fetch_ticket_list(page)

    def display_ticket_list(self):
        print(tabulate([t.get_info() for t in self.ticket_list], headers=Ticket.tickets_list_headers))

    # try fetch list and print error
    def fetch_ticket_list(self, page):
        try:
            url = self.base_url.format(page)
            response = requests.get(url, auth=(self.email, self.password))
            if response.status_code == 200:
                ticket_list = response.json()["tickets"]
                if ticket_list:
                    self.ticket_list = [Ticket(t) for t in ticket_list]
                    print("Page " + str(page))
                    self.display_ticket_list()
                    self.page = page
                else:
                    print("Page %d is empty" % page)
            elif response.status_code == 401:
                print("Not Authorized! Please check your credentials")
            else:
                print("Oops. Failed to fetch ticket list from server")
                print(response.json())
        except ValueError as ve:
            print(ve)

    def start(self):
        help_prompt = """===========================================
    This is Tickets List View
    * Type 'n' for next page
    * Type 'p' for previous page
    * Type 'curr' for current page
    * Type page+number to go to individual page
    * Type 'help' to display this message
    * Type 'back' to exit the tickets view
    * Type 'quit' to exit the application
    * Enter number to a single ticket by id
============================================"""
        shorten_help = "Type 'help' for help, Type 'n' for next page, 'p' for prev page, 'curr' for current page"
        if self.abort:
            return
        while True:
            print("-"*10)
            print(shorten_help)
            ticket_list_cmd = input(self.prompt)
            if ticket_list_cmd == "help":
                print(help_prompt)
            if ticket_list_cmd == "n":
                self.fetch_ticket_list(self.page + 1)
            elif ticket_list_cmd == "p":
                self.fetch_ticket_list(self.page - 1)
            elif ticket_list_cmd == "curr":
                print("Page " + str(self.page))
                self.display_ticket_list()
            elif ticket_list_cmd == "back":
                print("Going back to main menu")
                return
            elif ticket_list_cmd == "quit":
                exit(0)
            elif ticket_list_cmd[:4] == "page":
                page = ticket_list_cmd.strip()[4:]
                try:
                    self.fetch_ticket_list(int(page))
                except ValueError:
                    print(page, "is not a valid page number")
            else:
                try:
                    ticket_view = TicketView(self.config, int(ticket_list_cmd), "menu/ticket_list/ticket> ")
                    ticket_view.start()
                except ValueError:
                    print(ticket_list_cmd, "is not a valid ticket id!")


def start_main_view():
    config = configparser.ConfigParser()
    config.read("config.ini")

    menu_help = """===========================================
    This is menu
     * Type 'quit' to exit the application
     * Type 'help' to display this message
     * Type 'list' to view all tickets
     * Enter number to view a ticket by its ID
==========================================="""
    print("Welcome to the ticket viewer")
    print(menu_help)
    shorten_help = "Type 'help' for help, Type 'quit' to quit"
    while True:
        print("-"*10)
        print(shorten_help)
        cmd = input("menu> ")
        if cmd == 'help':
            print(menu_help)
        elif cmd == 'quit':
            # exit the program
            exit(0)

        # go to ticket list
        elif cmd == 'list':
            list_view = TicketListView(config["DEFAULT"], 1)
            list_view.start()

        # go to individual ticket
        else:
            try:
                ticket_view = TicketView(config["DEFAULT"], int(cmd))
                ticket_view.start()
            except ValueError:
                print(cmd, "is not a valid ticketId")


if __name__ == "__main__":
    start_main_view()
