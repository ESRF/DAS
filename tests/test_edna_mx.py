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


    def test_EDPluginControlInterfaceToMXCuBEv1_3(self):
        
        print "------------------------------------------------------------------------"

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

        jobId = self.dev.command_inout("startJob", [strEdnaPlugin, strXML])
        print "Started job: ", jobId

        # Wait for callback...
        bContinue = True
        fTotalTime = 0.0
        fMaxTime = 300.0
        while bContinue:
            print "JobID %s : Waiting for callback, time %f" % (jobId, fTotalTime)
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
        
        if self.jobOutput is not None:
            #print self.jobOutput
            if self.jobOutput.find("CharacterisationResult.xml") != -1:
                print "Test succeeded!"
                sys.exit(0)
            else:
                print "Test failed..."
                sys.exit(1)

if __name__ == '__main__':
    testDasEdnaServer = TestDasEdnaServer()
    testDasEdnaServer.setUp()
    testDasEdnaServer.test_EDPluginControlInterfaceToMXCuBEv1_3()





