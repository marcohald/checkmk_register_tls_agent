#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import \
    RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.i18n import _
from cmk.gui.plugins.wato import HostRulespec, rulespec_registry
from cmk.gui.valuespec import (Age, Alternative, Checkbox, Dictionary,
                               FixedValue, ListOfStrings, TextAscii)


def _valuespec_agent_config_register_tls():
    return Dictionary(
        title=_("Agent TLS Registration"),
        elements=[
            ("interval", Age(
                title=_("Run asynchronously"),
                label=_("Interval for collecting data"),
                default_value=3600
            )),


            ("tls_server", TextAscii(
                title=_("Server that should be added."),
                help=_("Enter only the hostname or  add :Port to use a specific Port. "
                        "You need to specify the Port if the System does not trust the checkmk Cert"
                ),
                allow_empty=False
            )),

            (
                "tls_usedevicehostname",
                Checkbox(
                    title=_("Device Hostname"),
                    default_value=False,
                    label=_(
                        "Use the device name instead of the value from Agent Updater")),
            ),
            ("tls_username", TextAscii(
                title=_("Username for Registration"),
                help=_(
                    "The User should have the Privilige to Pair an Agent, Read all hosts, write all hosts "),
                allow_empty=False
            )),
            ("tls_password", Password(
                title=_("Password / Secret for Registration User"),
                allow_empty=False
            )),
            ("tls_site", TextAscii(
                title=_("Use different Site than in Agent Updater"),
                help=_(
                    "If this is set, this value will be used instead the one of the registered Site in the Agent Updater."),
                allow_empty=False
            )),
        ],
        help=_(
            "This will deploy the agent plugin <tt>register_tls</tt> "
            "for registering the Agent via TLS."
        ),
        optional_keys=["tls_site"],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:register_tls",
        valuespec=_valuespec_agent_config_register_tls,
        # valuespec=_valuespec_agent_config_win_eventlog,
    ))
