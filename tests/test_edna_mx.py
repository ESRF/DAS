import PyTango
import time, sys, os, threading

if len(sys.argv) < 2:
    print "Usage: %s edna-tango-device-name" % os.path.basename(sys.argv[0])
    sys.exit(1)


class TestDasEdnaServer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._fTimeOut = 100.0 # s
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
<XSDataInputMXCuBE>
    <dataCollectionId>
        <value>976533</value>
    </dataCollectionId>
    <diffractionPlan>
        <aimedIOverSigmaAtHighestResolution>
            <value>3.000000e+00</value>
        </aimedIOverSigmaAtHighestResolution>
        <complexity>
            <value>none</value>
        </complexity>
        <maxExposureTimePerDataCollection>
            <value>6.000000e+03</value>
        </maxExposureTimePerDataCollection>
    </diffractionPlan>
    <experimentalCondition>
        <beam>
            <flux>
                <value>2.710000e+12</value>
            </flux>
            <minExposureTimePerImage>
                <value>8.000000e-02</value>
            </minExposureTimePerImage>
            <size>
                <x>
                    <value>5.000000e-02</value>
                </x>
                <y>
                    <value>3.000000e-02</value>
                </y>
            </size>
            <transmission>
                <value>1.000000e+02</value>
            </transmission>
            <wavelength>
                <value>9.136656e-01</value>
            </wavelength>
        </beam>
        <goniostat>
            <maxOscillationSpeed>
                <value>3.600000e+02</value>
            </maxOscillationSpeed>
            <minOscillationWidth>
                <value>5.000000e-02</value>
            </minOscillationWidth>
        </goniostat>
    </experimentalCondition>
    <sample>
        <shape>
            <value>1.000000e+00</value>
        </shape>
        <size>
            <x>
                <value>1.000000e-01</value>
            </x>
            <y>
                <value>1.000000e-01</value>
            </y>
            <z>
                <value>1.000000e-01</value>
            </z>
        </size>
        <susceptibility>
            <value>1.000000e+00</value>
        </susceptibility>
    </sample>
    <dataSet>
        <imageFile>
            <path>
                <value>/data/id29/inhouse/DAS/RAW_DATA/ref-4ESR372D11_1_0001.cbf</value>
            </path>
        </imageFile>
        <imageFile>
            <path>
                <value>/data/id29/inhouse/DAS/RAW_DATA/ref-4ESR372D11_1_0002.cbf</value>
            </path>
        </imageFile>
        <imageFile>
            <path>
                <value>/data/id29/inhouse/DAS/RAW_DATA/ref-4ESR372D11_1_0003.cbf</value>
            </path>
        </imageFile>
        <imageFile>
            <path>
                <value>/data/id29/inhouse/DAS/RAW_DATA/ref-4ESR372D11_1_0004.cbf</value>
            </path>
        </imageFile>
    </dataSet>
</XSDataInputMXCuBE>
"""

        strEdnaPlugin = "EDPluginControlInterfaceToMXCuBEv1_3"

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
            #print self.jobOutput
            if self._jobOutput.find("CharacterisationResult.xml") != -1:
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
        listTestDasEdnaServer = []
        # Start the servers
        for j in range(1):
            testDasEdnaServer = TestDasEdnaServer()
            testDasEdnaServer.start()
            listTestDasEdnaServer.append(testDasEdnaServer)
            time.sleep(1)
        for testDasEdnaServer in listTestDasEdnaServer:
            while testDasEdnaServer.getJobId() is None:
                time.sleep(1)
            print("%s started!" % testDasEdnaServer.getJobId())
        # Synchronize servers
        for testDasEdnaServer in listTestDasEdnaServer:
            testDasEdnaServer.join()
            if testDasEdnaServer.isSuccess():
                print("%s success! %.1f s" % (testDasEdnaServer.getJobId(), testDasEdnaServer.getExecutionTime()))
            else:
                print("%s failure! %.1f s" % (testDasEdnaServer.getJobId(), testDasEdnaServer.getExecutionTime()))
        time.sleep(1)





