from unittest import TestCase

import os, sys, socket
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
        strPathToConfigFile = "../config/%s.xml" % socket.gethostname()
        if not os.path.exists(strPathToConfigFile):
            raise BaseException("Cannot find configuration file: %s" % strPathToConfigFile)
        print "Using configuration file: %s" % os.path.abspath(strPathToConfigFile)
        with open(strPathToConfigFile) as f:
            strXmlConfig = f.read()
            config = DASConfig.parseString(strXmlConfig)
            ServerControl.startServer(config.EDNA)
    