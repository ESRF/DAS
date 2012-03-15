import PyTango
import time

def jobFinished(event):
    print "Job finished!", event.attr_value.value
    
def success(event):
    print "SUCCESS!", event.attr_value.value
    
def failure(event):
    print "FAILURE!", event.attr_value.value


dev = PyTango.DeviceProxy("mx/edna/1")
dev.subscribe_event("jobFinished", PyTango.EventType.CHANGE_EVENT, jobFinished, [])
dev.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, success, [])
dev.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, failure, [])


with open("/data/id29/inhouse/DAS/PROCESSED_DATA/EDNAInput_976533.xml") as f:
    strXML = f.read()
    strEdnaPlugin = "EDPluginControlInterfaceToMXCuBEv1_3"
    jobId = dev.command_inout("startJob", [strEdnaPlugin, strXML])
    print "Started job: ", jobId

