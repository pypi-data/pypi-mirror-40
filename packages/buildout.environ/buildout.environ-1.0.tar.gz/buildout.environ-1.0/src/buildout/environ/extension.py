# -*- coding: utf-8 -*-
from zc.buildout.buildout import Options

import os


def install(buildout):
    buildout._data["__environ__"] = Options(buildout, '__environ__', {})
    for key in os.environ:
        buildout["__environ__"][key] = os.environ[key]
