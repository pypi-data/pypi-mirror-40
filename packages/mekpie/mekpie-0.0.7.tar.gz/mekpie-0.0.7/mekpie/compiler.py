from time               import time
from os.path            import join
from collections        import namedtuple
from concurrent.futures import ThreadPoolExecutor

import mekpie.messages as messages

from .util         import (
    smv,
    panic, 
    list_files, 
    list_all_dirs,
    remove_contents, 
    filename, 
)
from .runner       import lrun
from .structure    import (
    get_project_path,
    get_test_path,
    get_target_path,
    get_target_debug_path,
    get_target_release_path,
    get_main_path,
    get_src_path,
    get_includes_path,
)

max_threads = 32

def command_clean(cfg):
    remove_contents(get_target_debug_path())
    remove_contents(get_target_release_path())
    if not cfg.options.quiet:
        print(messages.clean.strip())

def command_build(cfg):
    command_clean(cfg)
    start   = time()
    sources = get_sources(cfg)
    mains   = [get_main_path(cfg.main), *list_files(get_test_path(), with_ext='.c')]
    compiler_configs[cfg.cc](cfg, sources, mains)
    if not cfg.options.quiet:
        print(messages.build_succeeded.format(time() - start).strip())

def command_run(cfg):
    command_build(cfg)
    lrun([get_bin_path(cfg, get_main_path(cfg.main))] + cfg.options.programargs, error=False)

def command_debug(cfg):
    if cfg.options.release:
        panic(messages.release_debug)
    command_build(cfg)
    lrun([cfg.dbg, get_bin_path(cfg, get_main_path(cfg.main))])

def command_test(cfg):
    command_build(cfg)
    for test in get_tests(cfg):
        lrun([get_bin_path(cfg, test)])

def get_tests(cfg):
    return list_files(get_test_path(), with_filter=lambda test : 
        test.endswith('.c')  and 
        (filename(test) in cfg.options.commandargs or len(cfg.options.commandargs) == 0)
    )

def command_dist(cfg):
    command_build(cfg)
    smv(
        get_bin_path(cfg, get_main_path(cfg.main)), 
        join(get_project_path(), cfg.name)
    )

def get_bin_path(cfg, path):
    root = get_target_release_path() if cfg.options.release else get_target_debug_path()
    return join(root, filename(path))

def get_sources(cfg):
    sources = list_files(get_src_path(), with_ext='.c')
    sources.remove(get_main_path(cfg.main))
    return sources

def get_includes_paths():
    includes = get_includes_path()
    return [includes] + list_all_dirs(includes)

# Compiler Configs
# ---------------------------------------------------------------------------- #

def gcc_clang_config(cfg, sources, mains):
    sources  = sources
    verbose  = ['-v'] if cfg.options.verbose else []
    libs     = ['-l' + lib for lib in cfg.libs]
    includes = ['-I' + inc for inc in get_includes_paths()]
    flags    = cfg.flags + verbose + includes
    objects  = [get_bin_path(cfg, source) + '.o'
        for source 
        in sources
    ]
    # Build objects
    with ThreadPoolExecutor(max_workers=max(1, min(len(sources), max_threads))) as e:
        results = e.map(lambda source: lrun([
            cfg.cmd, 
            *flags, 
            '-c', source,
            '-o', get_bin_path(cfg, source) + '.o'
        ], quiet=cfg.options.quiet, error=False), sources)

    if not all(results):
        exit(1)


    flags = flags + libs
    # Link executables
    with ThreadPoolExecutor(max_workers=max(1, min(len(mains), max_threads))) as e:
        results = e.map(lambda main : lrun([
            cfg.cmd,
            main,
            *objects,
            *flags, 
            '-o' , get_bin_path(cfg, main)
        ], quiet=True, error=False), mains)

    if not all(results):
        for main in mains:
            lrun([
                cfg.cmd,
                main,
                *objects,
                *flags,
                '-o' , get_bin_path(cfg, main)
            ], quiet=cfg.options.quiet)
        
compiler_configs = {
    'gcc/clang' : gcc_clang_config,
}