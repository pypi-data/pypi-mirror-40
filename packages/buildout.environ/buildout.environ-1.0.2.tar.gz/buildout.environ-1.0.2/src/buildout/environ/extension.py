# -*- coding: utf-8 -*-
import os


def install(buildout):
    buildout["__environ__"] = dict(kv for kv in os.environ.items())
