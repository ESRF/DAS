
import PyTango
import os, socket, time



class ServerControl(object):


    @staticmethod
    def isLocalHost(_strHostName):
        strLocalHostName = socket.gethostname()
        bIsLocalHost = (_strHostName in strLocalHostName) or \
                        (strLocalHostName in _strHostName)
        return bIsLocalHost



    @staticmethod
    def startServer(_server):
        """Starts the EDNA and Workflow servers - if necessary"""
        if _server is not None:
            strTangoDevice = str(_server.tangoDevice)
            # Check if server is running
            bServerIsRunning = ServerControl.checkServer(strTangoDevice)
            if not bServerIsRunning:
                # We must try to start a server
                strTangoHost = _server.tangoHost
                strServerName = _server.tangoServerName
                # Try to start the principal server
                ServerControl.startIndividualServer(strTangoDevice, strTangoHost, strServerName, _server.principalServer)
                # Check if server is running
                bServerIsRunning = ServerControl.checkServer(strTangoDevice, 10)
                if not bServerIsRunning:
                    # We try to start one of the alternative servers (if available)
                    for alternativeServer in _server.alternativeServer:
                        ServerControl.startIndividualServer(strTangoDevice, strTangoHost, strServerName, alternativeServer)
                        # Check if server is running
                        bServerIsRunning = ServerControl.checkServer(strTangoDevice, 10)
                        if bServerIsRunning:
                            break
            if bServerIsRunning:
                print "Server %s is up and running!" % strTangoDevice
            else:
                raise Exception("ERROR! Could not start server %s!" % strTangoDevice)

    @staticmethod
    def checkServer(_strTangoDevice, _fWaitTime = -1):
        bServerStarted = False
        bContinue = True
        fWaitTime = float(_fWaitTime)
        tangoDeviceProxy = PyTango.DeviceProxy(_strTangoDevice)
        while bContinue:
            try:
                tangoDeviceProxy.ping()
                bServerStarted = True
                bContinue = False
            except Exception:
                print "Device server %s is not running!" % _strTangoDevice
            finally:
                if fWaitTime < 0:
                    bContinue = False
                else:
                    print "Trying again in a second, remaining time %.1f seconds..." % fWaitTime
                    time.sleep(1)
                    fWaitTime = fWaitTime - 1
        return bServerStarted



    @staticmethod
    def startIndividualServer(_strTangoDevice, _strTangoHost, _strServerName, _serverData):
        # The server doesn't run - we try to start it
        strHost = _serverData.host
        strPathToStartScript = _serverData.startScriptPath
        strPathToStopScript = _serverData.stopScriptPath
        print "Trying to start DasDS server '%s' on the computer %s" % (_strServerName, strHost)
        if ServerControl.isLocalHost(strHost):
            # First run the stop server script - in case the server is stuck
            os.system("%s %s" % (strPathToStopScript, _strServerName))
            # Then start the server
            os.system("%s %s" % (strPathToStartScript, _strServerName))
        else:
            # First run the stop server script - in case the server is stuck
            #strStopCommand = 'ssh %s "bash -ls -c \\\"%s %s\\\"" 2\>\&1 \> /dev/null' % (strHost, strPathToStopScript, strServerName)
            strStopCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, _strTangoHost, strPathToStopScript, _strServerName)
            print strStopCommand
            os.system(strStopCommand)
            # Then start the server
            strStartCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, _strTangoHost, strPathToStartScript, _strServerName)
            os.system(strStartCommand)
