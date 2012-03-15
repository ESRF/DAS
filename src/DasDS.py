#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        DasDS.py
#
# description : Python source for the DasDS and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                DasDS are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  $
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys

from config import DASConfig

#==================================================================
#   DasDS Class Description:
#
#   <b>DasDS</b> is a TANGO device server meant to be an interface between mxCuBE/bsxCuBE and the EDNA TANGO device server<br>
#   (<a href="https://github.com/edna-site/edna/blob/master/tango/bin/tango-EdnaDS.py">tango-EdnaDS</a>) and the DAWN workflow server (WorkflowDS).
#
#   <hr>
#   <h2>The communication sequence UML diagram:</h2>
#   <br><img src="Communication.png" alt="The communication sequence UML diagram"</img>
#
#   <hr>
#   <a href="../../tests/test_edna_mx.py">Sample Python client</a>
#   <hr>
#
#==================================================================


class DasDS(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        DasDS.init_device(self)
        self._ednaClient = None

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        print "[Device delete_device method] for device", self.get_name()


#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        print "In ", self.get_name(), "::init_device()"
        # Get configuration from Tango properties
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())
        db = PyTango.Database()
        listXmlConfig = db.get_device_property(self.get_name(), "Config")["Config"]
        print listXmlConfig, type(listXmlConfig)
        if len(listXmlConfig) == 0:
            print "ERROR! No property 'Config' found for device server %s" % self.get_name()
            sys.exit(1)
        try:
            # Convert list of lines to one string
            strXmlConfig = ''.join(listXmlConfig)
            self._config = DASConfig.parseString(strXmlConfig)
            print self._config.marshal()
        except Exception, e:
            print "ERROR! Exception caught when trying to unmarshal config XML for server %s" % self.get_name()
            print "Config XML:"
            print strXmlConfig
            sys.exit(1)
            
            #TODO: fix this
#        strDevice = str(self._config.EDNA[0].device)
#        print strDevice
#        self._ednaClient = PyTango.DeviceProxy(strDevice)
#        self._ednaClient.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.jobSuccess, [])
#        self._ednaClient.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.jobFailure, [])



#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        pass
#        print "In ", self.get_name(), "::always_excuted_hook()"


#==================================================================
#
#    DasDS read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self, data):
        print "In ", self.get_name(), "::read_attr_hardware()"



#------------------------------------------------------------------
#    Read JobSuccess attribute
#------------------------------------------------------------------
    def read_JobSuccess(self, attr):
        print "In ", self.get_name(), "::read_JobSuccess()"

        #    Add your own code here

        attr_JobSuccess_read = "Hello Tango world"
        attr.set_value(attr_JobSuccess_read)


#------------------------------------------------------------------
#    Read JobFailure attribute
#------------------------------------------------------------------
    def read_JobFailure(self, attr):
        print "In ", self.get_name(), "::read_JobFailure()"

        #    Add your own code here

        attr_JobFailure_read = "Hello Tango world"
        attr.set_value(attr_JobFailure_read)
        
        
#------------------------------------------------------------------
#    Read jobFinished attribute
#------------------------------------------------------------------
    def read_jobFinished(self, attr):
        print "In ", self.get_name(), "::read_jobFinished()"

        #    Add your own code here

        attr_jobFinished_read = ["No job launched yet", "failure"]
        attr.set_value(attr_jobFinished_read)


#==================================================================
#
#    DasDS command methods
#
#==================================================================

#------------------------------------------------------------------
#    startJob command:
#
#    Description:  
#    argin:  DevVarStringArray    [<Job to execute>,<XML input for job>]
#    argout: DevString    job id
#------------------------------------------------------------------
    def startJob(self, argin):
        print "In ", self.get_name(), "::startJob()"
        strDevice = str(self._config.EDNA[0].device)
        print strDevice
        self._ednaClient = PyTango.DeviceProxy(strDevice)
        self._ednaClient.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.jobSuccess, [])
        self._ednaClient.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.jobFailure, [])
        argout = self._ednaClient.startJob(argin)
        return argout


#------------------------------------------------------------------
#    abort command:
#
#    Description: 
#    argin:  DevString    job id
#    argout: DevBoolean    
#------------------------------------------------------------------
    def abort(self, argin):
        print "In ", self.get_name(), "::abort()"
        #    Add your own code here
        argout = False
        return argout


#------------------------------------------------------------------
#    getJobState command:
#
#    Description: 
#    argin:  DevString    job_id
#    argout: DevString    job state
#------------------------------------------------------------------
    def getJobState(self, argin):
        print "In ", self.get_name(), "::getJobState()"
        #    Add your own code here
        argout = "Not implemented"
        return argout


#------------------------------------------------------------------
#    initPlugin command:
#
#    Description: 
#    argin:  DevString    plugin name
#    argout: DevString    Message
#------------------------------------------------------------------
    def initPlugin(self, argin):
        print "In ", self.get_name(), "::initPlugin()"
        #    Add your own code here
        argout = "Not implemented"
        return argout


#------------------------------------------------------------------
#    getJobOutput command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: DevString    job output xml
#------------------------------------------------------------------
    def getJobOutput(self, argin):
        print "In ", self.get_name(), "::getJobOutput()"
        #    Add your own code here
        argout = "Not implemented"
        return argout


#------------------------------------------------------------------
#    jobSuccess command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: None
#------------------------------------------------------------------
    def jobSuccess(self, argin):
        print argin.attr_value.value
        self.push_change_event("jobFinished", [argin.attr_value.value, "success"])


#------------------------------------------------------------------
#    jobFailure command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: None
#------------------------------------------------------------------
    def jobFailure(self, argin):
        print argin.attr_value.value
        self.push_change_event("jobFinished", [argin.attr_value.value, "failure"])


#==================================================================
#
#    DasDSClass class definition
#
#==================================================================
class DasDSClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'Config':
            [PyTango.DevString,
            "General configuration in XML format",
            [] ],
        }


    #    Command definitions
    cmd_list = {
        'startJob':
            [[PyTango.DevVarStringArray, "[<Module to execute>,<XML input>]"],
            [PyTango.DevString, "job id"]],
        'abort':
            [[PyTango.DevString, "job id"],
            [PyTango.DevBoolean, ""]],
        'getJobState':
            [[PyTango.DevString, "job_id"],
            [PyTango.DevString, "job state"]],
        'initPlugin':
            [[PyTango.DevString, "plugin name"],
            [PyTango.DevString, "Message"]],
        'getJobOutput':
            [[PyTango.DevString, "jobId"],
            [PyTango.DevString, "job output xml"]],
        }


    #    Attribute definitions
    attr_list = {
        'JobSuccess':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'JobFailure':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'jobFinished':
            [[PyTango.DevString,
            PyTango.SPECTRUM,
            PyTango.READ, 2],
            {
                'Polling period':100000,
            } ],
        }


#------------------------------------------------------------------
#    DasDSClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print "In DasDSClass  constructor"

#==================================================================
#
#    DasDS class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        py = PyTango.Util(sys.argv)
        py.add_TgClass(DasDSClass, DasDS, 'DasDS')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed, e:
        print '-------> Received a DevFailed exception:', e
    except Exception, e:
        print '-------> An unforeseen exception occured....', e
