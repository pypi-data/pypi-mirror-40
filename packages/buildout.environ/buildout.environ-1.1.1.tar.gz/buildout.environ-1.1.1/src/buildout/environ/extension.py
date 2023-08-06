# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger("buildout.environ")


def install(buildout):
    buildout["__environ__"] = {}
    for key, value in os.environ.items():
        value = os.path.expandvars(value)
        buildout["__environ__"][key] = value.replace('$', '__dollar__')
    for key in buildout["buildout"].get("environ-output", '').split():
        logger.info(
            "{0}={1}".format(key, buildout["__environ__"].get(key, "(unset)"))
        )
