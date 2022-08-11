#!/usr/bin/env bash
. /etc/check_mk/register-tls.cfg
config="/etc/cmk-update-agent.state"

echo "<<<register_tls>>>"
server=$(eval cat "$config" | tr { '\n' | tr , '\n' | tr } '\n' | grep "server" | awk  -F"'" '{print $4}')
site=$(eval cat "$config" | tr { '\n' | tr , '\n' | tr } '\n' | grep "site" | awk  -F"'" '{print $4}')


if (cmk-agent-ctl status 2>&1) | grep -q -P "$server.*$site"; then
    echo "Server $server and Site: $site were found in cmk-agent-ctl status no need to register"
    
else
    echo "Need to register, Server $server and Site were not found"
    if [[ -n  "$tls_usedevicehostname" ]]
    then
        echo "\$tls_usedevicehostname is empty using hostname from updater config"
        host_name=$(eval cat "$config" | tr { '\n' | tr , '\n' | tr } '\n' | grep "host_name" | awk  -F"'" '{print $4}')
    else
        if [ "$tls_usedevicehostname" == "True" ]; then
            echo "Using device Hostname"
            host_name=`hostname`
        else
            echo "\$tls_usedevicehostname is set to $tls_usedevicehostname using hostname from updater config"
            host_name=$(eval cat "$config" | tr { '\n' | tr , '\n' | tr } '\n' | grep "host_name" | awk  -F"'" '{print $4}')
        fi
    fi
    echo "Server: $server"
    echo "Site: $site"
    echo "Hostname: $host_name"
    eval "cmk-agent-ctl register --trust-cert -H '$host_name' -s '$tls_server' -P '$tls_password' -U '$tls_username' -i '$site'"    
fi
