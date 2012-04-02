#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        DAS.py
#
# description : Python source for the DAS and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                DAS are implemented in this file.
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


import PyTango, sys

from config import DASConfig
from ServerControl import ServerControl

#==================================================================
#   DAS Class Description:
#
#         <b>DAS</b> is a TANGO device server meant to be an interface between mxCuBE/bsxCuBE and the EDNA TANGO device server<br>
#         (<a href="https://github.com/edna-site/edna/blob/master/tango/bin/tango-EdnaDS.py">tango-EdnaDS</a>) and the DAWN workflow server (WorkflowDS).
#         <hr>
#         <h2>The communication sequence UML diagram:</h2>
#         <br><img src="Communication.png" alt="The communication sequence UML diagram"</img>
#         <hr>
#         <a href="../../tests/test_edna_mx.py">Sample Python client</a>
#         <hr>
#
#==================================================================
#     Device States Description:
#
#   DevState.OFF :
#   DevState.FAULT :
#   DevState.RUNNING :
#==================================================================


class DAS(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        DAS.init_device(self)

#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.get_device_properties(self.get_device_class())
        # To make sure we get events without polling
        self.set_change_event("State", True, False)
        self.set_change_event("jobSuccess", True, False)
        self.set_change_event("jobFailure", True, False)
        self.set_change_event("dataAnalysisInformation", True, False)
        # Get configuration from Tango properties
        self._config = self.loadConfig()
        # Start the state machine
        #self._dasStateMachine = DASStateMachine(self)
        #self._dasStateMachine.start()
        #self._serverControl = ServerControl()
        self._serverControl = ServerControl(_logger_method=self.debug_stream)
        self.startRemoteEdnaServer()
        if self._config.Workflow is not None:
            self.startRemoteWorkflowServer()
        self.push_change_event("State", self.get_state())


#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        self.debug_stream("[Device delete_device method] for device", self.get_name())


#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        #self.debug_stream("In ", self.get_name(), "::always_excuted_hook()")
        pass


#------------------------------------------------------------------
#    jobFailure command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: None
#------------------------------------------------------------------
    def jobFailure(self, argin):
        self.debug_stream("In ", self.get_name(), "::jobFailure()")
        # Sometimes argin can be None...
        if argin is None:
            self.debug_stream("argin is None")
        else:
            self.debug_stream(" argin is ", argin)
            # And sometimes even argin.attr_value can be None!
            if argin.attr_value is None:
                self.debug_stream("argin.attr_value is None")
            elif argin.attr_value.value is None:
                self.debug_stream("argin.attr_value.value is None")
            else:
                self.push_change_event("jobFailure", argin.attr_value.value)
                self.push_change_event("dataAnalysisInformation", [argin.attr_value.value, "failure"])


#------------------------------------------------------------------
#    jobSuccess command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: None
#------------------------------------------------------------------
    def jobSuccess(self, argin):
        self.debug_stream("In ", self.get_name(), "::jobSuccess()")
        # Sometimes argin can be None...
        if argin is None:
            self.debug_stream("argin is None")
        else:
            self.debug_stream(" argin is ", argin)
            # And sometimes even argin.attr_value can be None!
            if argin.attr_value is None:
                self.debug_stream("argin.attr_value is None")
            elif argin.attr_value.value is None:
                self.debug_stream("argin.attr_value.value is None")
            else:
                self.push_change_event("jobSuccess", argin.attr_value.value)
                self.push_change_event("dataAnalysisInformation", [argin.attr_value.value, "success"])


#---- JobFailure attribute State Machine -----------------
    def is_JobFailure_allowed(self, req_type):
        if self.get_state() in [PyTango.DevState.OFF, PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    Read JobFailure attribute
#------------------------------------------------------------------
    def read_JobFailure(self, attr):
        self.debug_stream("In ", self.get_name(), "::read_JobFailure()")

        #    Add your own code here

        attr_JobFailure_read = "Hello Tango world"
        attr.set_value(attr_JobFailure_read)


#---- JobSuccess attribute State Machine -----------------
    def is_JobSuccess_allowed(self, req_type):
        if self.get_state() in [PyTango.DevState.OFF, PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    Read JobSuccess attribute
#------------------------------------------------------------------
    def read_JobSuccess(self, attr):
        self.debug_stream("In ", self.get_name(), "::read_JobSuccess()")

        #    Add your own code here

        attr_JobSuccess_read = "Hello Tango world"
        attr.set_value(attr_JobSuccess_read)


#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self, data):
        self.debug_stream("In ", self.get_name(), "::read_attr_hardware()")


    def getConfig(self):
        return self._config


    def loadConfig(self):
        db = PyTango.Database()
        listXmlConfig = db.get_device_property(self.get_name(), "Config")["Config"]
        #self.debug_stream(listXmlConfig, type(listXmlConfig))
        config = None
        if len(listXmlConfig) == 0:
            self.debug_stream("ERROR! No property 'Config' defined in Tango data base for device server %s" % self.get_name())
            sys.exit(1)
        try:
            # Convert list of lines to one string
            strXmlConfig = ''.join(listXmlConfig)
            config = DASConfig.parseString(strXmlConfig)
            #self.debug_stream(config.marshal())
        except Exception:
            self.debug_stream("ERROR! Exception caught when trying to unmarshal config XML for server %s" % self.get_name())
            self.debug_stream("Config XML:")
            self.debug_stream(strXmlConfig)
            raise
        return config

#==================================================================
#
#    DAS read/write attribute methods
#
#==================================================================


#------------------------------------------------------------------
#    Read jobSuccess attribute
#------------------------------------------------------------------
    def read_jobSuccess(self, attr):
        self.debug_stream("In ", self.get_name(), "::read_jobSuccess()")

        #    Add your own code here

        attr_jobSuccess_read = "Hello Tango world"
        attr.set_value(attr_jobSuccess_read)


#------------------------------------------------------------------
#    Read jobFailure attribute
#------------------------------------------------------------------
    def read_jobFailure(self, attr):
        self.debug_stream("In ", self.get_name(), "::read_jobFailure()")

        #    Add your own code here

        attr_jobFailure_read = "Hello Tango world"
        attr.set_value(attr_jobFailure_read)


#------------------------------------------------------------------
#    Read dataAnalysisInformation attribute
#------------------------------------------------------------------
    def read_dataAnalysisInformation(self, attr):
        self.debug_stream("In ", self.get_name(), "::read_dataAnalysisInformation()")

        #    Add your own code here

        attr_dataAnalysisInformation_read = ["No job launched yet", "failure"]
        attr.set_value(attr_dataAnalysisInformation_read)


#---- dataAnalysisInformation attribute State Machine -----------------
    def is_dataAnalysisInformation_allowed(self, req_type):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True



#==================================================================
#
#    DAS command methods
#
#==================================================================

#------------------------------------------------------------------
#    State command:
#
#    Description: This command gets the device state (stored in its <i>device_state</i> data member) and returns it to the caller.
#                
#    argout: DevState    State Code
#------------------------------------------------------------------
    def dev_state(self):
        #self.debug_stream("In ", self.get_name(), "::dev_state() = " , self.get_state())
        #    Add your own code here
        if not self._serverControl.checkServer(self._config.EDNA.tangoDevice):
# trick - only restart the server if the server has already been detected down
#         this will happen the second time dev_state()
            if self.get_state() == PyTango.DevState.OFF:
                self.startRemoteEdnaServer()
            else:
                self.set_state(PyTango.DevState.OFF)

        if self._config.Workflow is not None:
            if not self._serverControl.checkServer(self._config.Workflow.tangoDevice):
# trick - same trick as above
                if self.get_state() == PyTango.DevState.OFF:
                    self.startRemoteWorkflowServer()
                else:
                    self.set_state(PyTango.DevState.OFF)
        argout = self.get_state()
        return argout


#------------------------------------------------------------------
#    Status command:
#
#    Description: This command gets the device status (stored in its <i>device_status</i> data member) and returns it to the caller.
#                
#    argout: ConstDevString    Status description
#------------------------------------------------------------------
    def dev_status(self):
        self.debug_stream("In ", self.get_name(), "::dev_status()")
        self.the_status = self.get_status()
        #    Add your own code here

        self.set_status(self.the_status)
        return self.the_status


#------------------------------------------------------------------
#    startJob command:
#
#    Description: 
#    argin:  DevVarStringArray    [<Module to execute>,<XML input>]
#    argout: DevString    job id
#------------------------------------------------------------------
    def startJob(self, argin):
        self.debug_stream("In ", self.get_name(), "::startJob()")
        #self._config = self.loadConfig()        
        self.debug_stream("argin = ", argin)
        try:
            argout = self._ednaClient.startJob(argin)
        except Exception, e:
            self.debug_stream("ERROR in startJob! ", type(e))
            # TODO: Restart EDNA server
            raise
        self.debug_stream("argout = ", argout)
        return argout


#---- startJob command State Machine -----------------
    def is_startJob_allowed(self):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    abort command:
#
#    Description: 
#    argin:  DevString    job id
#    argout: DevBoolean    
#------------------------------------------------------------------
    def abort(self, argin):
        self.debug_stream("In ", self.get_name(), "::abort()")
        #    Add your own code here
        argout = False
        return argout


#---- abort command State Machine -----------------
    def is_abort_allowed(self):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    getJobState command:
#
#    Description: 
#    argin:  DevString    job_id
#    argout: DevString    job state
#------------------------------------------------------------------
    def getJobState(self, argin):
        self.debug_stream("In ", self.get_name(), "::getJobState()")
        #    Add your own code here
        argout = "Not implemented"
        return argout


#---- getJobState command State Machine -----------------
    def is_getJobState_allowed(self):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    initPlugin command:
#
#    Description: 
#    argin:  DevString    plugin name
#    argout: DevString    Message
#------------------------------------------------------------------
    def initPlugin(self, argin):
        self.debug_stream("In ", self.get_name(), "::initPlugin()")
        #    Add your own code here
        argout = "Not implemented"
        return argout


#---- initPlugin command State Machine -----------------
    def is_initPlugin_allowed(self):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#    getJobOutput command:
#
#    Description: 
#    argin:  DevString    jobId
#    argout: DevString    job output xml
#------------------------------------------------------------------
    def getJobOutput(self, argin):
        self.debug_stream("In ", self.get_name(), "::getJobOutput()")
        argout = self._ednaClient.getJobOutput(argin)
        return argout


#---- getJobOutput command State Machine -----------------
    def is_getJobOutput_allowed(self):
        if self.get_state() in [PyTango.DevState.OFF,
                                PyTango.DevState.FAULT]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True


    def startRemoteEdnaServer(self):
        try:
            self.set_state(PyTango.DevState.OFF)
            self._serverControl.startServer(self._config.EDNA)
            strEdnaDevice = str(self._config.EDNA.tangoDevice)
            self.debug_stream(strEdnaDevice)
            self._ednaClient = PyTango.DeviceProxy(strEdnaDevice)
            self._ednaClient.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.jobSuccess, [])
            self._ednaClient.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.jobFailure, [])
            self.set_state(PyTango.DevState.RUNNING)
        except Exception, e:
            # Something horrible happened!!!
            self.set_state(PyTango.DevState.FAULT)
            # TODO: send email
            raise


    def startRemoteWorkflowServer(self):
        try:
            self.set_state(PyTango.DevState.OFF)
            self._serverControl.startServer(self._config.Workflow)
            strWorkflowDevice = str(self._config.Workflow.tangoDevice)
            self.debug_stream(strWorkflowDevice)
            self._workflowClient = PyTango.DeviceProxy(strWorkflowDevice)
            self._workflowClient.subscribe_event("jobSuccess", PyTango.EventType.CHANGE_EVENT, self.jobSuccess, [])
            self._workflowClient.subscribe_event("jobFailure", PyTango.EventType.CHANGE_EVENT, self.jobFailure, [])
            self.set_state(PyTango.DevState.RUNNING)
        except Exception, e:
            # Something horrible happened!!!
            self.set_state(PyTango.DevState.FAULT)
            # TODO: send email
            raise

#==================================================================
#
#    DASClass class definition
#
#==================================================================
class DASClass(PyTango.DeviceClass):

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
        'jobSuccess':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'jobFailure':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'dataAnalysisInformation':
            [[PyTango.DevString,
            PyTango.SPECTRUM,
            PyTango.READ, 2]],
        }


#------------------------------------------------------------------
#    DASClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print("In DASClass  constructor")

#==================================================================
#
#    DAS class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        py = PyTango.Util(sys.argv)
        py.add_TgClass(DASClass, DAS, 'DAS')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed, e:
        print('-------> Received a DevFailed exception:', e)
    except Exception, e:
        print('-------> An unforeseen exception occured....', e)
