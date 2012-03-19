
import PyTango
import socket



class ServerControl(object):


    @staticmethod
    def isLocalHost(_strHostName):
        strLocalHostName = socket.gethostname()
        bIsLocalHost =  (_strHostName in strLocalHostName) or \
                        (strLocalHostName in _strHostName)
        return bIsLocalHost



    @staticmethod
    def startServers(_listServers):
        """Starts the EDNA and Workflow servers - if necessary"""
        bServerStarted = False
        for server in _listServers:
            strTangoDevice = server.tangoDevice
            strHost = server.host
            strServerName = server.tangoServerName
            strPathToStartScript = server.startScriptPath
            strPathToStopScript = server.stopScriptPath
            if not bServerStarted:
                try:
                    tangoDeviceProxy = PyTango.DeviceProxy(strTangoDevice)
                    tangoDeviceProxy.ping()
                    bServerStarted = True
                except Exception:
                    print "Server %s not responding" % strTangoDevice
            if not bServerStarted:
                # The server doesn't run - we try to start it
                print "Trying to start DasDS server '%s' on the computer %s" % (strServerName, strHost)
                # First run the stop server script - in case the server is stuck
                os.system("%s %s" % (strPathToStartScript, strServerName)
                
                
                
        
