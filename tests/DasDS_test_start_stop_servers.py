from unittest import TestCase

import sys, socket
sys.path.append("../src")

from config import DASConfig # IGNORE:E0611

from ServerControl import ServerControl

class DasDS_test_start_stop_servers(TestCase):


    def test_isLocalHost(self):
        strLocalHost = socket.gethostname() 
        self.assertTrue(ServerControl.isLocalHost(strLocalHost), "Host is localhost")
        self.assertTrue(ServerControl.isLocalHost(strLocalHost+".esrf.fr"), "Host + .esrf.fr is localhost")
        
        




    def test_start_EDNA_server(self):
        # Read test data - note that this depends on the system
        with open("../config/astros.xml") as f:
            strXmlConfig = f.read()
            config = DASConfig.parseString(strXmlConfig)
            ServerControl.startServers(config.EDNA)
    