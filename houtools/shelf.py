import os
import re

import yaml

import hou

from . import utils


def dispatch(entrypoint, args=(), kwargs={}, reload=None):
    func = utils.resolve_entrypoint(entrypoint, reload=reload)
    return func(*args, **kwargs)


def load(path=None):

    if path is None:
        path = os.environ.get('HOUTOOLS_SHELVES', '').split(':')
    for root in path:
        for dir_path, dir_names, file_names in os.walk(root):
            for file_name in file_names:
                if file_name.endswith('.yml') and not file_name.startswith('.'):
                    load_one(os.path.join(dir_path, file_name))


def load_one(path):

    label = os.path.basename(os.path.splitext(path)[0])
    name = 'houtools_' + re.sub(r'\W+', '_', label).lower()

    # Make the shelf.
    shelves = hou.shelves.shelves()
    shelf = shelves.get(name)
    if not shelf:
        shelf = hou.shelves.newShelf(name=name, label=label)

    # Add the shelf to the current desktop.
    desktop = hou.ui.curDesktop()
    dock = desktop.shelfDock()
    shelfSets = dock.shelfSets()
    shelfSet = shelfSets[0]
    if shelf not in shelfSet.shelves():
        shelfSet.setShelves(shelfSet.shelves() + (shelf, ))

    shelf.setTools(())

    # Load the buttons.
    serialized = open(path).read()
    buttons = yaml.load_all(serialized)
    for button in buttons:
        load_button(shelf, button)


def load_button(shelf, spec):

    label = spec['label']
    name = spec.get('name') or ('%s_%s' % (shelf.name(), re.sub(r'\W+', '_', label))).lower()

    # Make sure the tool exists.
    tools = hou.shelves.tools()
    tool = tools.get(name)
    if not tool:
        tool = hou.shelves.newTool(name=name)

    # Make sure the tools is on the shelf.
    shelf.setTools(shelf.tools() + (tool, ))

    # Set up the tool.
    tool.setLabel(label)
    if 'python' in spec:
        tool.setScript(spec['python'])
    elif 'entrypoint' in spec:
        tool.setScript('from houtools.shelf import dispatch; dispatch(%r)' % spec['entrypoint'])


