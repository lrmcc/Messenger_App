import unittest

from Messenger_Client import *

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.ADDR = (socket.gethostbyname(socket.gethostname()), 5050)

    def tearDown(self):
        pass

    def test_get_client_instance(self):
        client = MessengerClient(self.ADDR)
        self.assertTrue(type(client) is MessengerClient)
    
if __name__ == '__main__':
    unittest.main()