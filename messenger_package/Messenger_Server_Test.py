import unittest

from Messenger_Server import *

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.ADDR = (socket.gethostbyname(socket.gethostname()), 5050)

    def tearDown(self):
        pass

    def test_get_server_instance(self):
        server = MessengerServer(self.ADDR)
        self.assertTrue(type(server) is MessengerServer)
    
if __name__ == '__main__':
    unittest.main()