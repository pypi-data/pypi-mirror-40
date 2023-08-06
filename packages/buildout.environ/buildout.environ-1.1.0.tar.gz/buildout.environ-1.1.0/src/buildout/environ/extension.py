# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger("buildout.environ")


def install(buildout):
    buildout["__environ__"] = dict(kv for kv in os.environ.items())
    for key in buildout["buildout"].get("environ-output", '').split():
        logger.info(
            "{0}={1}".format(key, buildout["__environ__"].get(key, "(unset)"))
        )
