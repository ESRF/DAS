import PyTango
import time, sys, os, threading

if len(sys.argv) < 2:
    print "Usage: %s edna-tango-device-name" % os.path.basename(sys.argv[0])
    sys.exit(1)


class TestDasID29CreateThumbnail(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._fTimeOut = 10.0 # s
        self._dev = PyTango.DeviceProxy(sys.argv[1])
        self._dev.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.successCallback, [])
        self._dev.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.failureCallback, [])
        self._success = None
        self._failure = None
        self._jobOutput = None
        self._fExecutionTime = 0.0
        self._strJobId = None
        self._bSuccess = None

    def successCallback(self, event):
        if event.attr_value is not None:
            self._success = event.attr_value.value
            #print "SUCCESS!", event.attr_value.value
            if event.attr_value.value is not None:
                self._jobOutput = self._dev.getJobOutput(event.attr_value.value)
    
    def failureCallback(self, event):
        if event.attr_value is not None:
            self._failure = event.attr_value.value
        #print "FAILURE!", event.attr_value.value


    def run(self):
        
        #print "------------------------------------------------------------------------"

        strXML = """<?xml version="1.0" ?>
<XSDataInputPyarchThumbnailGenerator>
    <diffractionImage>
        <path>
            <value>/data/id29/inhouse/opid291/20120502/RAW_DATA/opid291_4_0001.cbf</value>
        </path>
    </diffractionImage>
    <waitForFileTimeOut>
        <value>1000</value>
    </waitForFileTimeOut>
</XSDataInputPyarchThumbnailGenerator>
"""

        strEdnaPlugin = "EDPluginControlPyarchThumbnailGeneratorv1_0"

        self._strJobId = self._dev.command_inout("startJob", [strEdnaPlugin, strXML])
        #print "Started job: ", self._strJobId

        # Wait for callback...
        bContinue = True
        self._fExecutionTime = 0.0
        while bContinue:
            #print "self._strJobId %s : Waiting for callback, time %f" % (self._strJobId, fExecutionTime)
            if self._success == self._strJobId:
                #print self.jobOutput
                bContinue = False
            elif self._failure == self._strJobId:
                #print "FAILURE!"
                bContinue = False
            else:
                time.sleep(1)
                self._fExecutionTime += 1.0
                if self._fExecutionTime > self._fTimeOut:
                    bContinue = False
        
        if self._jobOutput is not None:
            #print self._strJobId
            #print self._jobOutput
            if self._jobOutput.find("pathToJPEGImage") != -1:
                self._bSuccess = True
            else:
                self._bSuccess = False
                
                
    def isSuccess(self):
        return self._bSuccess
                
    def getJobId(self):
        return self._strJobId
    
    def getExecutionTime(self):
        return self._fExecutionTime
    
    def setTimeOut(self, _fValue):
        self._fTimeOut = _fValue

if __name__ == '__main__':
    for i in range(5):
        listTestDasID29CreateThumbnail = []
        # Start the servers
        for j in range(5):
            testDasEdnaServer = TestDasID29CreateThumbnail()
            testDasEdnaServer.start()
            listTestDasID29CreateThumbnail.append(testDasEdnaServer)
            time.sleep(1)
        for testDasEdnaServer in listTestDasID29CreateThumbnail:
            while testDasEdnaServer.getJobId() is None:
                time.sleep(1)
            print("%s started!" % testDasEdnaServer.getJobId())
        # Synchronize servers
        for testDasEdnaServer in listTestDasID29CreateThumbnail:
            testDasEdnaServer.join()
            if testDasEdnaServer.isSuccess():
                print("%s success! %.1f s" % (testDasEdnaServer.getJobId(), testDasEdnaServer.getExecutionTime()))
            else:
                print("%s failure! %.1f s" % (testDasEdnaServer.getJobId(), testDasEdnaServer.getExecutionTime()))
        time.sleep(1)





