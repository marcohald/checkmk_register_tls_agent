#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.
import json
from pathlib import Path
from typing import Any, Dict,Iterable, TypedDict, List


from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register, WindowsConfigGenerator, WindowsConfigEntry

def _get_linux_cfg_lines(conf: Dict) -> List[str]:
   config = json.dumps({'user': conf['tls_server'], 'content': conf['tls_server']})
   return config.split('\n')

def _get_mk_docker_config(conf: Dict[str, Any]) -> Iterable[str]:

    yield "[DOCKER]"
    # beware of the inverting in the Transfom of the WATO rule!
    skip_sections = conf.get("node", []) + conf.get("containers", [])
    if skip_sections:
        yield "skip_sections: %s" % ",".join(skip_sections)
    else:
        yield "# skip_sections: no sections skipped"

    yield "container_id: %s" % conf.get("container_id", "short")

    if "base_url" in conf:
        yield "base_url: %s" % conf["base_url"]   

def get_register_tls_files(conf: Dict[str, Any]) -> FileGenerator:
    interval = conf.get('interval')

    yield Plugin(base_os=OS.WINDOWS,
                 source=Path("register-tls.ps1"),
                 interval=interval)
    yield Plugin(base_os=OS.WINDOWS,
                 source=Path("powershell-yaml-0.4.2.zip"),
                 interval=0)
#    if 'oids' in conf:
#        yield PluginConfig(base_os=OS.WINDOWS,
#                           lines=['CERT_DIRS="%s"' % " ".join(conf['directories'])],
#                           target=Path("sslcertificates"),
#                           include_header=True)
    yield Plugin(
        base_os=OS.LINUX,
        source=Path('register-tls.sh'),
        target=Path('register-tls.sh'),
        interval=interval,
    )

    yield PluginConfig(base_os=OS.LINUX,
                        lines=_get_linux_cfg_lines(conf),
                        target=Path('register-tls.json'),
                        include_header=False)

    iterate = [] 
    for key, val in conf.items(): 
     iterate.append("export " + str(key) + "='" + str(val) +"'") 

    yield PluginConfig(base_os=OS.LINUX, lines=iterate, target=Path("register-tls.cfg"))                        


def get_register_tls_windows_config(conf: Dict[str, Any]) -> WindowsConfigGenerator:
    yield WindowsConfigEntry(path=["register_tls", "tls_server"], content=conf["tls_server"])
    yield WindowsConfigEntry(path=["register_tls", "tls_usedevicehostname"], content=conf["tls_usedevicehostname"])
    yield WindowsConfigEntry(path=["register_tls", "tls_username"], content=conf["tls_username"])
    yield WindowsConfigEntry(path=["register_tls", "tls_password"], content=conf["tls_password"])
    if 'tls_site' in conf:
        yield WindowsConfigEntry(path=["register_tls", "tls_site"], content=conf["tls_site"])
    # yield WindowsConfigEntry(path=["register_tls", "content"], content=conf["content"])


register.bakery_plugin(
    name="register_tls",
    files_function=get_register_tls_files,
    windows_config_function=get_register_tls_windows_config,
)
