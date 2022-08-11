# checkmk Register TLS Agent
## Description
This Extension contains Agent Plugins for Windows and Linux to register the Agent TLS Connection.  
It works only with the cee Edition  
It should be only used on secure network, because it skips  all certificate validation.  
The plugins provide no output.  

The checkmk User should have this privileges:
- Agent pairing
- Read access to all hosts and folders
- Write access to all hosts and folders


The supplied Secret is stored in Plaintext in the Configuration File.  
The Server can also Contain the AGENT_RECEIVER_PORT (this is the only way to skip certificate checks against the checkmk Server HTTPS Certificate) You can find it with omd config site -> Basic  
The default Configuration uses the site and host name from the Updater.  
You can specify another Site Name and you could use the hostname of the device instead of the one from the Updater


The Windows Agent Plugin contains powershell-yaml Version 0.4.2

## Build a new Version
to create a new Version you need to install https://github.com/copyleft/python-mkp and edit the dist.py
