import PyTango
import time, sys, os

if len(sys.argv) < 2:
    print "Usage: %s edna-tango-device-name" % os.path.basename(sys.argv[0])
    sys.exit(1)


class TestDasEdnaServer(object):

    def setUp(self):
        self.dev = PyTango.DeviceProxy(sys.argv[1])
        self.dev.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.successCallback, [])
        self.dev.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.failureCallback, [])
        self.success = None
        self.failure = None
        self.jobOutput = None

    def successCallback(self, event):
        self.success = event.attr_value.value
        #print "SUCCESS!", event.attr_value.value
        if event.attr_value.value is not None:
            self.jobOutput = self.dev.getJobOutput(event.attr_value.value)
    
    def failureCallback(self, event):
        self.failure = event.attr_value.value
        #print "FAILURE!", event.attr_value.value


    def test_EDPluginTestPluginFactory(self):
        
        print "------------------------------------------------------------------------"

        strXML = """<?xml version="1.0" ?>
        <XSDataString>
            <value>Test string value.</value>
        </XSDataString>"""

        strEdnaPlugin = "EDPluginTestPluginFactory"

        jobId = self.dev.command_inout("startJob", [strEdnaPlugin, strXML])
        print "Started job: ", jobId

        # Wait for callback...
        bContinue = True
        fTotalTime = 0.0
        fMaxTime = 10.0
        while bContinue:
            print "Waiting for callback..."
            if self.success == jobId:
                #print self.jobOutput
                bContinue = False
            elif self.failure == jobId:
                #print "FAILURE!"
                bContinue = False
            else:
                time.sleep(1)
                fTotalTime += 1.0
                if fTotalTime > fMaxTime:
                    bContinue = False
        
        if self.jobOutput.find("Test string value.") != -1:
            print "Test succeeded!"
            sys.exit(0)
        else:
            print "Test failed..."
            sys.exit(1)

if __name__ == '__main__':
    testDasEdnaServer = TestDasEdnaServer()
    testDasEdnaServer.setUp()
    testDasEdnaServer.test_EDPluginTestPluginFactory()





