
import PyTango
import os, socket, time



class ServerControl(object):


    def __init__(self, _logger_method=None):
        self._logger_method = _logger_method


    def log(self, _strLogMessage):
        if self._logger_method is None:
            print _strLogMessage
        else:
            self._logger_method(_strLogMessage)


    def isLocalHost(self, _strHostName):
        strLocalHostName = socket.gethostname()
        bIsLocalHost = (_strHostName in strLocalHostName) or \
                        (strLocalHostName in _strHostName)
        return bIsLocalHost


    def startServer(self, _server):
        """Starts the EDNA and Workflow servers - if necessary"""
        if _server is not None:
            strTangoDevice = str(_server.tangoDevice)
            # Check if server is running
            bServerIsRunning = self.checkServer(strTangoDevice)
            if not bServerIsRunning:
                # We must try to start a server
                strTangoHost = _server.tangoHost
                strServerName = _server.tangoServerName
                # Try to start the principal server
                self.startIndividualServer(strTangoDevice, strTangoHost, strServerName, _server.principalServer)
                # Check if server is running
                bServerIsRunning = self.checkServer(strTangoDevice, 10)
                if not bServerIsRunning:
                    # We try to start one of the alternative servers (if available)
                    for alternativeServer in _server.alternativeServer:
                        self.startIndividualServer(strTangoDevice, strTangoHost, strServerName, alternativeServer)
                        # Check if server is running
                        bServerIsRunning = ServerControl.checkServer(strTangoDevice, 10)
                        if bServerIsRunning:
                            break
            if bServerIsRunning:
                self.log("Server %s is up and running!" % strTangoDevice)
            else:
                raise Exception("ERROR! Could not start server %s!" % strTangoDevice)


    def checkServer(self, _strTangoDevice, _fWaitTime = -1):
        bServerStarted = False
        bContinue = True
        fWaitTime = float(_fWaitTime)
        tangoDeviceProxy = PyTango.DeviceProxy(str(_strTangoDevice))
        while bContinue:
            try:
                tangoDeviceProxy.ping()
                bServerStarted = True
                bContinue = False
            except Exception:
                self.log("Device server %s is not running!" % _strTangoDevice)
                if fWaitTime > 0:
                    self.log("Trying again in a second, remaining time %.1f seconds..." % fWaitTime)
                    time.sleep(1)
                    fWaitTime = fWaitTime - 1
                else:
                    bContinue = False
        return bServerStarted



    def startIndividualServer(self, _strTangoDevice, _strTangoHost, _strServerName, _serverData):
        # The server doesn't run - we try to start it
        strHost = _serverData.host
        strPathToStartScript = _serverData.startScriptPath
        strPathToStopScript = _serverData.stopScriptPath
        self.log("Trying to start DasDS server '%s' on the computer %s" % (_strServerName, strHost))
        if self.isLocalHost(strHost):
            # First run the stop server script - in case the server is stuck
            os.system("%s %s" % (strPathToStopScript, _strServerName))
            # Then start the server
            os.system("%s %s" % (strPathToStartScript, _strServerName))
        else:
            # First run the stop server script - in case the server is stuck
            #strStopCommand = 'ssh %s "bash -ls -c \\\"%s %s\\\"" 2\>\&1 \> /dev/null' % (strHost, strPathToStopScript, strServerName)
            strStopCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, _strTangoHost, strPathToStopScript, _strServerName)
            self.log(strStopCommand)
            os.system(strStopCommand)
            # Then start the server
            strStartCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, _strTangoHost, strPathToStartScript, _strServerName)
            os.system(strStartCommand)
