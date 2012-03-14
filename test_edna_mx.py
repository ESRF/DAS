import PyTango
import time

dev = PyTango.DeviceProxy("mx/edna/1")
def success(event):
    print "SUCCESS!", event.attr_value.value
def failure(event):
    print "FAILURE!", event.attr_value.value
dev.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, success, [])
dev.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, failure, [])

f = open("/data/id29/inhouse/DAS/PROCESSED_DATA/EDNAInput_976533.xml")
strXML = f.read()
f.close()
strEdnaPlugin = "EDPluginControlInterfaceToMXCuBEv1_3"

jobId = dev.command_inout("startJob", [strEdnaPlugin, strXML])

print "Started job: ", jobId


while True:
    time.sleep(60)
