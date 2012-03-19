
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
    def startServers(_listServers):
        """Starts the EDNA and Workflow servers - if necessary"""
        bServerStarted = False
        for server in _listServers:
            strTangoDevice = str(server.tangoDevice)
            strTangoHost = server.tangoHost
            strHost = server.host
            strServerName = server.tangoServerName
            strPathToStartScript = server.startScriptPath
            strPathToStopScript = server.stopScriptPath
            tangoDeviceProxy = PyTango.DeviceProxy(strTangoDevice)
            if not bServerStarted:
                try:
                    tangoDeviceProxy.ping()
                    bServerStarted = True
                except Exception:
                    print "Server %s not responding" % strTangoDevice
            if not bServerStarted:
                # The server doesn't run - we try to start it
                print "Trying to start DasDS server '%s' on the computer %s" % (strServerName, strHost)
                if ServerControl.isLocalHost(strHost):
                    # First run the stop server script - in case the server is stuck
                    os.system("%s %s" % (strPathToStopScript, strServerName))
                    # Then start the server
                    os.system("%s %s" % (strPathToStartScript, strServerName))
                else:
                    # First run the stop server script - in case the server is stuck
                    #strStopCommand = 'ssh %s "bash -ls -c \\\"%s %s\\\"" 2\>\&1 \> /dev/null' % (strHost, strPathToStopScript, strServerName)
                    strStopCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, strTangoHost, strPathToStopScript, strServerName)
                    print strStopCommand
                    os.system(strStopCommand)
                    # Then start the server
                    strStartCommand = 'ssh %s "env TANGO_HOST=%s %s %s" 2\>\&1 \> /dev/null' % (strHost, strTangoHost, strPathToStartScript, strServerName)
                    os.system(strStartCommand)
                time.sleep(1)
                try:
                    tangoDeviceProxy.ping()
                    print "\nServer %s on host %s is now up and running!\n" % (strTangoDevice, strHost)
                    bServerStarted = True
                except Exception:
                    print "\nCould not start server %s on host %s!\n" % (strTangoDevice, strHost)
