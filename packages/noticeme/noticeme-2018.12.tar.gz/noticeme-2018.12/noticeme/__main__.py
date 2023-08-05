# MIT License

# Copyright (c) 2018 Bobby

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import os
import re
import shlex
import sys
from configparser import (ConfigParser, DuplicateOptionError,
                          DuplicateSectionError, NoOptionError, NoSectionError,
                          ParsingError)
from datetime import datetime, timedelta
from importlib import import_module
from pathlib import PurePath

from . import noticeme

repo_url = 'https://github.com/bobbytrapz/noticeme'


def die(msg):
    print('\n\nerror:', msg)
    print('get help at ->', repo_url)
    sys.exit(1)


defaults = {
    'should': {
        'clear_screen': 'no',
        'clear_after': 0,
    },
    'imports': {},
}


def show_events():
    # gather all known events
    events = list(noticeme.EVENTS.keys())
    events.extend(noticeme.VEVENTS.keys())

    def evdoc(name):
        # given the name of an event return its docstring
        if name == 'all':
            return 'Handle all known events besides virtual.'
        elif name == 'all_virtual':
            return 'Handle all known virtual events.'
        else:
            try:
                return getattr(noticeme.Event, name).__doc__
            except AttributeError:
                return 'No documentation found.'

    # display all known events and docstrings
    docs = {ev: evdoc(ev) for ev in events}
    for ev, doc in sorted(docs.items()):
        print(ev, '-', doc)
    return 0


config_parser = None
should = None
imports = None
last_proc_at = datetime.min


def read_config():
    global config_parser, should, imports
    # read configuration
    config_path = 'noticeme.cfg'
    config_parser = ConfigParser()
    config_parser.read_dict(defaults)
    try:
        config_parser.read(config_path)
    except ParsingError as e:
        die(e)
    except FileNotFoundError:
        die('You need a noticeme.cfg first.')

    # parse configuration
    should = config_parser['should']
    try:
        int(should['clear_after'])
    except ValueError:
        die("'clear_after' should be an integer.")

    if should['clear_screen'] == 'yes':
        os.system('clear')

    imports = config_parser['imports']

    for name, desc in imports.items():
        # import module
        try:
            mod = import_module(name)
        except ImportError:
            die("'import {}'".format(name))
        print("import", name, '-', desc)

    for name in config_parser.sections():
        if name == 'should' or name == 'imports':
            continue
        section = config_parser[name]
        try:
            add_watcher_from_section(section)
        except Exception as e:
            die(e)


async def create_shell_proc(name, command):
    global last_proc_at
    if should["clear_screen"] == 'yes':
        since_proc = (datetime.now() - last_proc_at)
        delay = timedelta(seconds=int(should['clear_after']))
        if since_proc > delay:
            os.system('clear')
    proc = await asyncio.create_subprocess_shell(command)
    last_proc_at = datetime.now()
    return proc


def make_shell_handler(name, command, regex_patterns, glob_patterns):
    "Handle a event by executing a command on the shell"
    async def handler(event):
        proc = None

        if len(regex_patterns) == 0 and len(glob_patterns) == 0:
            # there are no patterns to match against so just run
            proc = await create_shell_proc(name, command)
        elif any(rep.match(str(event.path)) for rep in regex_patterns):
            # path matches a regex pattern
            proc = await create_shell_proc(name, command)
        elif any(event.path.match(gp) for gp in glob_patterns):
            # path matches a glob pattern
            proc = await create_shell_proc(name, command)

        if proc:
            await proc.wait()

    return handler


def add_watcher_from_section(section):
    "Given a configparser.Section we build a new watcher"
    name = section._name

    # watcher description
    try:
        description = section['description']
        print(name, '-', description)
    except:
        raise Exception(
            "'{}' must have a 'description'".format(name))

    # watchers paths to watch
    try:
        paths = section['paths'].split()
    except KeyError:
        raise Exception(
            "'{}' must have 'paths' to watch.".format(name))

    # watcher events to listen for
    try:
        events = section['events'].split()
    except KeyError:
        raise Exception(
            "'{}' must have 'events' to track.".format(name))

    # watcher regex patterns to match against paths
    try:
        regex_patterns = list(re.compile(pat)
                              for pat in section['regex'].split())
    except KeyError:
        regex_patterns = list()
    except re.error as e:
        die(e)

    # watcher glob pattern to match against paths
    try:
        glob_patterns = section['glob'].split()
    except KeyError:
        glob_patterns = list()

    # watcher shell command to execute when conditions are satisfied
    try:
        command = section['shell']
    except KeyError:
        raise Exception(
            "'{}' must have a 'shell' to run a command.".format(name))

    noticeme.add_watcher(paths, events, make_shell_handler(
        name, command, regex_patterns, glob_patterns))


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'events':
            show_events()
            sys.exit(0)

    # configure
    read_config()
    # event loop
    noticeme.run()


if __name__ == '__main__':
    main()
