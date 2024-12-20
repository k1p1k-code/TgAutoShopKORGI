from utils import plugins as loader
import sys

plugins=loader.load()
on_startup=list()
for n in plugins.plagins_object:
    if plugins.plagins_object[n].on_startup != str:
        on_startup.append(plugins.plagins_object[n].on_startup)

def plugin_reload():
    global plugins
    plugins=loader.load()
    on_startup=list()
    for n in plugins.plagins_object:
        if plugins.plagins_object[n].on_startup != str:
            on_startup.append(plugins.plagins_object[n].on_startup)
    return [plugins, on_startup]