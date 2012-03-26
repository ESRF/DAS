
import PyTango
import os, socket, time, threading


from ServerControl import ServerControl


class DASStateMachine(threading.Thread):

    def __init__(self, _das=None):
        threading.Thread.__init__(self)
        self._das = _das
        self._state = 
        
    def run(self):
        """Thread for the state machine"""
        
        
        
        
    def setStateOn(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.ON)
        
    def setStateFault(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.FAULT)

    def setStateRunning(self):
        if self._das is not None:
            self._das.set_state(PyTango.DevState.RUNNING)
