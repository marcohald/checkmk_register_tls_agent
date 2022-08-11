#!/usr/bin/env python

from mkp import dist

dist({
    'author': 'Marco Hald',
    'description': 'This Extension contains Agent Plugins for Windows and Linux '
                'to register the Agent TLS Connection.\n'
                'It works only with the cee Edition\n'
                'It should be only used on secure network, because it skips  '
                'all certificate validation.\n'
                'The plugins provide no output.\n'
                '\n'
                'The checkmk User should have this privileges:\n'
                '- Agent pairing\n'
                '- Read access to all hosts and folders\n'
                '- Write access to all hosts and folders\n\n'
                'The supplied Secret is stored in Plaintext in the '
                'Configuration File.\n'
                'The Server can also Contain the AGENT_RECEIVER_PORT (this is '
                'the only way to skip certificate checks against the checkmk '
                'Server HTTPS Certificate) You can find it with omd config '
                'site -> Basic\n'
                'The default Configuration uses the site and host name from '
                'the Updater.\n'
                'You can specify another Site Name and you could use the '
                'hostname of the device instead of the one from the Updater\n'
                '\n'
                'The Windows Agent Plugin contains powershell-yaml Version '
                '0.4.2\n',
    'download_url': 'https://github.com/marcohald/checkmk_register_tls_agent',
    'name': 'register-tls-agent',
    'title': 'Register Agent via TLS',
    'version': '1.0.6',
    'version.min_required': '2.1.0',
})
