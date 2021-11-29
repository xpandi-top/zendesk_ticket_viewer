import configparser
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from TicketViews import Ticket, TicketListView, start_main_view, TicketView


test_ticket = {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None,
               'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}},
               'created_at': '2021-11-24T17:17:14Z', 'updated_at': '2021-11-24T17:17:14Z', 'type': 'incident',
               'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket',
               'description': 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new '
                              'product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n',
               'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 1524116881702,
               'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': None,
               'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
               'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
               'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None,
               'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
               'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True}

test_ticket_list_5 = [
    {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None,
     'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}},
     'created_at': '2021-11-24T17:17:14Z', 'updated_at': '2021-11-24T17:17:14Z', 'type': 'incident',
     'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket',
     'description': 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n',
     'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 1524116881702,
     'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': None,
     'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
     'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
     'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None,
     'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
     'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True},
    {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None,
     'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}},
     'created_at': '2021-11-24T17:52:04Z', 'updated_at': '2021-11-24T17:52:04Z', 'type': None,
     'subject': 'velit eiusmod reprehenderit officia cupidatat',
     'raw_subject': 'velit eiusmod reprehenderit officia cupidatat',
     'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.',
     'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 1524218942861,
     'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': 1500630745722,
     'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
     'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
     'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None,
     'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
     'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True},
    {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None,
     'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}},
     'created_at': '2021-11-24T17:52:05Z', 'updated_at': '2021-11-24T17:52:05Z', 'type': None,
     'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem',
     'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.',
     'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 1524218942861,
     'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': 1500630745722,
     'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
     'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
     'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None,
     'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
     'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True},
    {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/4.json', 'id': 4, 'external_id': None,
     'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}},
     'created_at': '2021-11-24T17:52:05Z', 'updated_at': '2021-11-24T17:52:05Z', 'type': None,
     'subject': 'ad sunt qui aute ullamco', 'raw_subject': 'ad sunt qui aute ullamco',
     'description': 'Sunt incididunt officia proident elit anim ullamco reprehenderit ut. Aliqua sint amet aliquip cillum minim magna consequat excepteur fugiat exercitation est exercitation. Adipisicing occaecat nisi aliqua exercitation.\n\nAute Lorem aute tempor sunt mollit dolor in consequat non cillum irure reprehenderit. Nulla deserunt qui aliquip officia duis incididunt et est velit nulla irure in fugiat in. Deserunt proident est in dolore culpa mollit exercitation ea anim consequat incididunt. Mollit et occaecat ullamco ut id incididunt laboris occaecat qui.',
     'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 1524218942861,
     'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': 1500630745722,
     'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
     'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
     'tags': ['laborum', 'mollit', 'proident'], 'custom_fields': [], 'satisfaction_rating': None,
     'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
     'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True},
    {'url': 'https://zccdimo.zendesk.com/api/v2/tickets/5.json', 'id': 5, 'external_id': None,
     'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}},
     'created_at': '2021-11-24T17:52:06Z', 'updated_at': '2021-11-24T17:52:06Z', 'type': None,
     'subject': 'aliquip mollit quis laborum incididunt',
     'raw_subject': 'aliquip mollit quis laborum incididunt',
     'description': 'Pariatur voluptate laborum voluptate sunt ad magna exercitation nulla. In in Lorem minim dolor laboris reprehenderit ad Lorem. Cupidatat laborum qui mollit nostrud magna ullamco. Tempor nisi ex ipsum fugiat dolor proident qui consectetur anim sunt. Dolore consectetur in ex esse et aliqua fugiat enim Lorem ea Lorem incididunt. Non amet elit pariatur commodo labore officia esse anim. In do mollit commodo nulla ullamco culpa cillum incididunt.\n\nEt nostrud aute fugiat voluptate tempor ad labore in elit et sunt. Enim quis nulla eu ut sit. Pariatur irure officia occaecat non dolor est excepteur anim incididunt commodo ea cupidatat minim excepteur. Cillum proident tempor laborum amet est ipsum ipsum aliqua sit sunt reprehenderit fugiat aliqua ea.',
     'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 1524218942861,
     'submitter_id': 1524218942861, 'assignee_id': 1524218942861, 'organization_id': 1500630745722,
     'group_id': 4414039174679, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [],
     'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None,
     'tags': ['consectetur', 'mollit', 'sit'], 'custom_fields': [], 'satisfaction_rating': None,
     'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 1500003391722,
     'brand_id': 1500002349462, 'allow_channelback': False, 'allow_attachments': True}]

ticket_list_table_5 = """  id  subject                                        created_at            updated_at            priority    status
----  ---------------------------------------------  --------------------  --------------------  ----------  --------
   1  Sample ticket: Meet the ticket                 2021-11-24T17:17:14Z  2021-11-24T17:17:14Z  normal      open
   2  velit eiusmod reprehenderit officia cupidatat  2021-11-24T17:52:04Z  2021-11-24T17:52:04Z              open
   3  excepteur laborum ex occaecat Lorem            2021-11-24T17:52:05Z  2021-11-24T17:52:05Z              open
   4  ad sunt qui aute ullamco                       2021-11-24T17:52:05Z  2021-11-24T17:52:05Z              open
   5  aliquip mollit quis laborum incididunt         2021-11-24T17:52:06Z  2021-11-24T17:52:06Z              open
"""

list_prompt = """----------
Type 'help' for help, Type 'n' for next page, 'p' for prev page, 'curr' for current page\n"""

config = configparser.ConfigParser()
config.read("config.ini")


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MyTestCase(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_Ticket_print_ticket(self, mock_stdout):
        get_dummy_ticket_detail = """    ID            :1
    CREATED_AT    :2021-11-24T17:17:14Z
    UPDATED_AT    :2021-11-24T17:17:14Z
    TYPE          :incident
    SUBJECT       :Sample ticket: Meet the ticket
    PRIORITY      :normal
    STATUS        :open
    REQUESTER_ID  :1524116881702
    SUBMITTER_ID  :1524218942861
    DESCRIPTION   :Hi there,

I’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?

Thanks,
 The Customer


"""
        t = Ticket(test_ticket)
        t.print_ticket()
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, get_dummy_ticket_detail)

    # test ticket get info
    def test_Ticket_get_info(self):
        dummy_tt_info = [1, 'Sample ticket: Meet the ticket', '2021-11-24T17:17:14Z',
                         '2021-11-24T17:17:14Z', 'normal', 'open']
        t = Ticket(test_ticket)
        actual_output = t.get_info()
        self.assertEqual(actual_output, dummy_tt_info)

    # test menu
    def test_menu_menu(self):
        menu_menu_output = """Welcome to the ticket viewer
===========================================
    This is menu
     * Type 'quit' to exit the application
     * Type 'help' to display this message
     * Type 'list' to view all tickets
     * Enter number to view a ticket by its ID
===========================================
----------
Type 'help' for help, Type 'quit' to quit
===========================================
    This is menu
     * Type 'quit' to exit the application
     * Type 'help' to display this message
     * Type 'list' to view all tickets
     * Enter number to view a ticket by its ID
===========================================
----------
Type 'help' for help, Type 'quit' to quit
"""
        with self.assertRaises(SystemExit) as sys_exit, \
                patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["help", "quit"]):
            start_main_view()
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, menu_menu_output)
        self.assertEqual(sys_exit.exception.code, 0)

    def test_menu_quit(self):
        menu_menu_output = """Welcome to the ticket viewer
===========================================
    This is menu
     * Type 'quit' to exit the application
     * Type 'help' to display this message
     * Type 'list' to view all tickets
     * Enter number to view a ticket by its ID
===========================================
----------
Type 'help' for help, Type 'quit' to quit
"""
        with self.assertRaises(SystemExit) as sys_exit, \
                patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["quit"]):
            start_main_view()
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, menu_menu_output)
        self.assertEqual(sys_exit.exception.code, 0)

    def test_menu_list(self):
        menu_list_output = """Welcome to the ticket viewer
===========================================
    This is menu
     * Type 'quit' to exit the application
     * Type 'help' to display this message
     * Type 'list' to view all tickets
     * Enter number to view a ticket by its ID
===========================================
----------
Type 'help' for help, Type 'quit' to quit
----------
Type 'help' for help, Type 'quit' to quit
"""
        with self.assertRaises(SystemExit) as sys_exit, \
                patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["list", "yes", "quit"]), \
                patch("TicketViews.TicketListView.fetch_ticket_list", return_value=None) as mock_fetch, \
                patch("TicketViews.TicketListView.start", return_value=0) as mock_list_run:
            start_main_view()
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, menu_list_output)
        self.assertEqual(sys_exit.exception.code, 0)
        mock_fetch.assert_called_once()
        mock_list_run.assert_called_once()

    # test functions in list view
    def test_list_fetch_empty(self):
        mock_response = MockResponse({"tickets": []}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes"]), \
                patch("requests.get", return_value=mock_response):
            TicketListView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Page 1 is empty\n")

    def test_list_fetch_error(self):
        mock_response = MockResponse("Internal Server Error", 500)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes"]), \
                patch("requests.get", return_value=mock_response):
            TicketListView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Oops. Failed to fetch ticket list from server\nInternal Server Error\n")

    def test_list_fetch_no_auth(self):
        mock_response = MockResponse({"tickets": []}, 401)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes"]), \
                patch("requests.get", return_value=mock_response):
            TicketListView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Not Authorized! Please check your credentials\n")

    def test_list_fetch_no_abort(self):
        with patch("builtins.input", side_effect=["no"]), \
                patch("requests.get", return_value=None) as mock_request:
            TicketListView(config["DEFAULT"], 1)
        mock_request.assert_not_called()

    def test_list_display(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes"]), \
                patch("requests.get", return_value=mock_response):
            TicketListView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Page 1\n" + ticket_list_table_5)

    def test_list_next_page(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "n", "quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.fetch_ticket_list = MagicMock(return_value=None)
            ticket_list.start()
        ticket_list.fetch_ticket_list.assert_called_with(2)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Page 1\n" + ticket_list_table_5 +
                         list_prompt * 2)

    def test_list_prev_page(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "p", "quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.fetch_ticket_list = MagicMock(return_value=None)
            ticket_list.start()
        ticket_list.fetch_ticket_list.assert_called_with(0)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Page 1\n" + ticket_list_table_5 +
                         list_prompt * 2)

    def test_list_curr_page(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "curr", "quit"]), \
                patch("requests.get", return_value=mock_response) as mock_request, \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.fetch_ticket_list = MagicMock(return_value=None)
            ticket_list.start()
        ticket_list.fetch_ticket_list.assert_not_called()
        mock_request.assert_called_once()
        actual_output = mock_stdout.getvalue()
        out = "Page 1\n" + ticket_list_table_5 + list_prompt
        self.assertEqual(actual_output, out * 2)

    def test_list_page_4(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "page4", "quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.fetch_ticket_list = MagicMock(return_value=None)
            ticket_list.start()
        ticket_list.fetch_ticket_list.assert_called_with(4)
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, "Page 1\n" + ticket_list_table_5 +
                         list_prompt * 2)

    def test_list_back(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "back", "quit"]), \
                patch("requests.get", return_value=mock_response) as mock_request:
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.start()
        mock_request.assert_called_once()
        actual_output = mock_stdout.getvalue()
        out = "Page 1\n" + ticket_list_table_5 + list_prompt
        self.assertEqual(actual_output, out + "Going back to main menu\n")

    def test_list_quit(self):
        mock_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "quit"]), \
                patch("requests.get", return_value=mock_response) as mock_request, \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.start()
        mock_request.assert_called_once()
        actual_output = mock_stdout.getvalue()
        out = "Page 1\n" + ticket_list_table_5 + list_prompt
        self.assertEqual(actual_output, out)

    def test_list_goto_ticket(self):
        mock_list_response = MockResponse({"tickets": test_ticket_list_5}, 200)
        mock_ticket_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["yes", "2", "quit"]), \
                patch("requests.get", side_effect=[mock_list_response, mock_ticket_response]) as mock_requests, \
                self.assertRaises(SystemExit):
            ticket_list = TicketListView(config["DEFAULT"], 1)
            ticket_list.fetch_ticket_list = MagicMock(return_value=None)
            ticket_list.start()
        actual_output = mock_stdout.getvalue()
        self.assertEqual(actual_output, """Page 1
  id  subject                                        created_at            updated_at            priority    status
----  ---------------------------------------------  --------------------  --------------------  ----------  --------
   1  Sample ticket: Meet the ticket                 2021-11-24T17:17:14Z  2021-11-24T17:17:14Z  normal      open
   2  velit eiusmod reprehenderit officia cupidatat  2021-11-24T17:52:04Z  2021-11-24T17:52:04Z              open
   3  excepteur laborum ex occaecat Lorem            2021-11-24T17:52:05Z  2021-11-24T17:52:05Z              open
   4  ad sunt qui aute ullamco                       2021-11-24T17:52:05Z  2021-11-24T17:52:05Z              open
   5  aliquip mollit quis laborum incididunt         2021-11-24T17:52:06Z  2021-11-24T17:52:06Z              open
----------
Type 'help' for help, Type 'n' for next page, 'p' for prev page, 'curr' for current page
===========================================
    This is Ticket View
    * Type 'n' for next ticket
    * Type 'p' for previous ticket
    * Type 'curr' for curr ticket
    * Type number of a ticket id to go to a ticket
    * Type 'quit' to exit the application
    * Type 'back' to exit this view and back to previous view
    * Type 'help' to display this message
===========================================
    ID            :1
    CREATED_AT    :2021-11-24T17:17:14Z
    UPDATED_AT    :2021-11-24T17:17:14Z
    TYPE          :incident
    SUBJECT       :Sample ticket: Meet the ticket
    PRIORITY      :normal
    STATUS        :open
    REQUESTER_ID  :1524116881702
    SUBMITTER_ID  :1524218942861
    DESCRIPTION   :Hi there,

I’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?

Thanks,
 The Customer


----------
Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket 
""")

    # test detail ticket view
    def test_ticket_no_auth(self):
        mock_response = MockResponse({"ticket": []}, 401)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["quit"]), \
                patch("requests.get", return_value=mock_response):
            TicketView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "Not Authorized! Please check your credentials\n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_no_found(self):
        mock_response = MockResponse("Internal Server Error", 500)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["quit"]), \
                patch("requests.get", return_value=mock_response):
            TicketView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "Oops. Ticket not 1 found\n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_display(self):
        mock_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["quit"]), \
                patch("requests.get", return_value=mock_response):
            TicketView(config["DEFAULT"], 1)
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "    ID            :1\n"
                         "    CREATED_AT    :2021-11-24T17:17:14Z\n"
                         "    UPDATED_AT    :2021-11-24T17:17:14Z\n"
                         "    TYPE          :incident\n"
                         "    SUBJECT       :Sample ticket: Meet the ticket\n"
                         "    PRIORITY      :normal\n"
                         "    STATUS        :open\n"
                         "    REQUESTER_ID  :1524116881702\n"
                         "    SUBMITTER_ID  :1524218942861\n"
                         "    DESCRIPTION   :Hi there,\n"
                         "\n"
                         "I’m sending an email because I’m having a problem setting up your new product. Can you help "
                         "me troubleshoot?\n"
                         "\n"
                         "Thanks,\n"
                         " The Customer\n"
                         "\n"
                         "\n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_prev_display(self):
        mock_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["p", "quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            t_ticket = TicketView(config["DEFAULT"], 1)
            t_ticket.fetch_ticket = MagicMock(return_value=None)
            t_ticket.start()
        t_ticket.fetch_ticket.assert_called_with(0)
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "    ID            :1\n"
                         "    CREATED_AT    :2021-11-24T17:17:14Z\n"
                         "    UPDATED_AT    :2021-11-24T17:17:14Z\n"
                         "    TYPE          :incident\n"
                         "    SUBJECT       :Sample ticket: Meet the ticket\n"
                         "    PRIORITY      :normal\n"
                         "    STATUS        :open\n"
                         "    REQUESTER_ID  :1524116881702\n"
                         "    SUBMITTER_ID  :1524218942861\n"
                         "    DESCRIPTION   :Hi there,\n"
                         "\n"
                         "I’m sending an email because I’m having a problem setting up your new product. Can you help "
                         "me troubleshoot?\n"
                         "\n"
                         "Thanks,\n"
                         " The Customer\n"
                         "\n"
                         "\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n"
                         "fetching previous ticket\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_next_display(self):
        mock_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["n", "quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            t_ticket = TicketView(config["DEFAULT"], 1)
            t_ticket.fetch_ticket = MagicMock(return_value=None)
            t_ticket.start()
        t_ticket.fetch_ticket.assert_called_with(2)
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "    ID            :1\n"
                         "    CREATED_AT    :2021-11-24T17:17:14Z\n"
                         "    UPDATED_AT    :2021-11-24T17:17:14Z\n"
                         "    TYPE          :incident\n"
                         "    SUBJECT       :Sample ticket: Meet the ticket\n"
                         "    PRIORITY      :normal\n"
                         "    STATUS        :open\n"
                         "    REQUESTER_ID  :1524116881702\n"
                         "    SUBMITTER_ID  :1524218942861\n"
                         "    DESCRIPTION   :Hi there,\n"
                         "\n"
                         "I’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n"
                         "\n"
                         "Thanks,\n"
                         " The Customer\n"
                         "\n"
                         "\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n"
                         "fetching next ticket\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_back_display(self):
        mock_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["back"]), \
                patch("requests.get", return_value=mock_response):
            t_ticket = TicketView(config["DEFAULT"], 1)
            t_ticket.start()
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "    ID            :1\n"
                         "    CREATED_AT    :2021-11-24T17:17:14Z\n"
                         "    UPDATED_AT    :2021-11-24T17:17:14Z\n"
                         "    TYPE          :incident\n"
                         "    SUBJECT       :Sample ticket: Meet the ticket\n"
                         "    PRIORITY      :normal\n"
                         "    STATUS        :open\n"
                         "    REQUESTER_ID  :1524116881702\n"
                         "    SUBMITTER_ID  :1524218942861\n"
                         "    DESCRIPTION   :Hi there,\n"
                         "\n"
                         "I’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n"
                         "\n"
                         "Thanks,\n"
                         " The Customer\n"
                         "\n"
                         "\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n"
                         "Going back to ticket list\n")
        self.assertEqual(expect_output, actual_output)

    def test_ticket_quit_display(self):
        mock_response = MockResponse({"ticket": test_ticket}, 200)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
                patch("builtins.input", side_effect=["quit"]), \
                patch("requests.get", return_value=mock_response), \
                self.assertRaises(SystemExit):
            t_ticket = TicketView(config["DEFAULT"], 1)
            t_ticket.start()
        actual_output = mock_stdout.getvalue()
        expect_output = ("===========================================\n"
                         "    This is Ticket View\n"
                         "    * Type 'n' for next ticket\n"
                         "    * Type 'p' for previous ticket\n"
                         "    * Type 'curr' for curr ticket\n"
                         "    * Type number of a ticket id to go to a ticket\n"
                         "    * Type 'quit' to exit the application\n"
                         "    * Type 'back' to exit this view and back to previous view\n"
                         "    * Type 'help' to display this message\n"
                         "===========================================\n"
                         "    ID            :1\n"
                         "    CREATED_AT    :2021-11-24T17:17:14Z\n"
                         "    UPDATED_AT    :2021-11-24T17:17:14Z\n"
                         "    TYPE          :incident\n"
                         "    SUBJECT       :Sample ticket: Meet the ticket\n"
                         "    PRIORITY      :normal\n"
                         "    STATUS        :open\n"
                         "    REQUESTER_ID  :1524116881702\n"
                         "    SUBMITTER_ID  :1524218942861\n"
                         "    DESCRIPTION   :Hi there,\n"
                         "\n"
                         "I’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n"
                         "\n"
                         "Thanks,\n"
                         " The Customer\n"
                         "\n"
                         "\n"
                         "----------\n"
                         "Type 'help' for help, Type 'n' for next ticket, 'p' for prev ticket, 'curr' for current ticket \n")
        self.assertEqual(expect_output, actual_output)

if __name__ == '__main__':
    unittest.main()
