from collections import namedtuple

Option = namedtuple('Option', [
    'names',
    'nargs',
    'handler',
])

Options = namedtuple('Options', [
    'quiet',       # -q --quiet
    'verbose',     # -v --verbose
    'release',     # -r --release
    'developer',   # -d --developer
    'changedir',   # -c --changedir
    'command',     # new, init, clean, build, run, test, debug
    'commandargs', # <optionargs...>
    'programargs', # -- <programargs...>
])

Config = namedtuple('Config', [
    'name',                   # Project name
    'main',                   # Entry point
    'libs',                   # Libraries to link
    'cc',                     # C Compiler Configuration
    'cmd',                    # The C Compiler command
    'dbg',                    # Debugger
    'flags',                  # User compiler flags
    'options',                # The provided command line options
])

CompilerPreset = namedtuple('CompilerPreset', [
    'cc',           # the compiler config
    'cmd',          # the compiler command
    'dbg',          # the debug command
    'dbg_flags',    # the debug flags
    'release_flags' # the release flags
])

CC_CMDS = {
    'clang' : CompilerPreset(
        cc            = 'gcc/clang',
        cmd           = 'clang',
        dbg           = 'lldb',
        dbg_flags     = '[\'-g\']',
        release_flags = '[\'-O\']',
    ),
    'gcc' : CompilerPreset(
        cc            = 'gcc/clang',
        cmd           = 'gcc',
        dbg           = 'gdb',
        dbg_flags     = '[\'-g\']',
        release_flags = '[\'-O\']',
    ),
    'default' : CompilerPreset(
        cc            = 'gcc/clang',
        cmd           = 'cc',
        dbg           = 'debugger',
        dbg_flags     = '[\'-g\']',
        release_flags = '[\'-O\']',
    )
}

DEFAULT_MEKPY='''
# This is a standard configuration file for mekpie

# the name of your project
name = '{}' 
# the .c file containing `main`
main = '{}'
# any libraries to load
libs = []
# the c compiler configuration to use (gcc/clang)
cc = '{}'
# the c compiler command to use on the command line
cmd = '{}'
# the debugger to use
dbg = '{}'
# additional compiler flags
flags = ['-Wall']

if options.release:
    flags = flags + {}
else:
    flags = flags + {}
'''

MAIN = '''
#include <stdio.h>
#include <stdlib.h>

int main() {
    puts("Hello, World!");
    return EXIT_SUCCESS;
}
'''.strip()

VERSION = '0.0.1'