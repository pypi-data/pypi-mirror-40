# -*- coding: utf-8 -*-

from .pyjapc import PyJapc
from .rbac_dialog import PasswordEntryDialogue, getPw

__version__ = "2.0.0"

__cmmnbuild_deps__ = [
    {"product":"japc", "version":"7.0.5" },
    {"product":"japc-value", "version":"7.0.5" },
    {"product":"japc-ext-cmwrda", "version":"7.0.5" },
    {"product":"japc-ext-cmwrda3", "version":"7.0.5" },
    {"product":"japc-ext-tgm", "version":"7.0.5" },
    "japc-ext-inca",
    "japc-ext-dirservice",
    "accsoft-security-rba",
    "accsoft-security-rba-util",
    "inca-client",
    "slf4j-log4j12",
    "slf4j-api",
    "log4j"
]
