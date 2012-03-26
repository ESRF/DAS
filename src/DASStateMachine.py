
import PyTango
import os, socket, time, threading


from ServerControl import ServerControl


class DASStateMachine(threading.Thread):

    def __init__(self, _das = None, _config = None):
        threading.Thread.__init__(self)
        self._das = _das
        self.setStateOn()
        # Default polling time
        self._fPollingTime = 10 # seconds
        # Default email
        self._contactEmail = None
        if self._das is not None:
            self._config = _das.getConfig()
            if self._config.pollingTime is not None:
                self._fPollingTime = self._config.pollingTime
            self._contactEmail = self._config.contactEmail
        # For testing purposes:
        if _config is not None:
            self._config = _config
        self._bContinue = True
        self._ednaClient = None
        self._workflowClient = None

    def run(self):
        """Thread for the state machine"""
        # First time we need to start the remote servers
        self.startRemoteEdnaServer()
        if self._config.Workflow is not None:
            self.startRemoteWorkflowServer()
        # Continue till aborted
        while self._bContinue:
            # Sleep the polling time
            time.sleep(self._fPollingTime)
            # Check servers and start them if not running
            if not ServerControl.checkServer(self._config.EDNA.tangoDevice):
                self.startRemoteEdnaServer()
            if self._config.Workflow is not None:
                if not ServerControl.checkServer(self._config.Workflow.tangoDevice):
                    self.startRemoteWorkflowServer()



    def startRemoteEdnaServer(self):
        try:
            self.setStateOn()
            ServerControl.startServer(self._config.EDNA)
            strEdnaDevice = str(self._config.EDNA.tangoDevice)
            print strEdnaDevice
            self._ednaClient = PyTango.DeviceProxy(strEdnaDevice)
            if self._das is not None:
                # Since we restarted Edna Servers, we need to re-subscribe
                self._das.setEdnaClient(self._ednaClient)
            self.setStateRunning()
        except Exception, e:
            # Something horrible happened!!!
            self.setStateFault()
            self._bContinue = False
            # TODO: send email
            raise


    def startRemoteWorkflowServer(self):
        try:
            self.setStateOn()
            ServerControl.startServer(self._config.Workflow)
            strWorkflowDevice = str(self._config.Workflow.tangoDevice)
            print strWorkflowDevice
            self._workflowClient = PyTango.DeviceProxy(strWorkflowDevice)
            if self._das is not None:
                # Since we restarted Edna Servers, we need to re-subscribe
                self._das.setWorkflowClient(self._workflowClient)
            self.setStateRunning()
        except Exception, e:
            # Something horrible happened!!!
            self.setStateFault()
            self._bContinue = False
            # TODO: send email
            raise


    def setStateOn(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.ON)

    def setStateFault(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.FAULT)

    def setStateRunning(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.RUNNING)

    def stop(self):
        self._bContinue = False
