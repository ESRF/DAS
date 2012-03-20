import PyTango
import time

def jobFinished(event):
    print "Job finished!", event.attr_value.value
    jobFinishedId, status = event.attr_value.value
    if status == "success":
        print dev.getJobOutput(jobFinishedId)
    
def success(event):
    print "SUCCESS!", event.attr_value.value
    print dev.getJobOutput(event.attr_value.value)
    
def failure(event):
    print "FAILURE!", event.attr_value.value


#dev = PyTango.DeviceProxy("DAS/linsvensson/1")
dev = PyTango.DeviceProxy("linsvensson/edna/1")
#dev.subscribe_event("jobFinished", PyTango.EventType.CHANGE_EVENT, jobFinished, [])
dev.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, success, [])
dev.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, failure, [])

print "------------------------------------------------------------------------"

strXML = """<?xml version="1.0" ?>
<XSDataString>
    <value>Test string value.</value>
</XSDataString>"""

#strEdnaPlugin = "EDPluginControlInterfaceToMXCuBEv1_3"
strEdnaPlugin = "EDPluginTestPluginFactory"
jobId = dev.command_inout("startJob", [strEdnaPlugin, strXML])
print "Started job: ", jobId

time.sleep(30)