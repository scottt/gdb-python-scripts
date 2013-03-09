# Usage: gdb -x dump-vars-each-step.py PROGRAM

import gdb

import re
import logging

LOG_LEVEL = logging.INFO

def dump_all_vars(skip_libc_symbols=True):
    # gdb calls the source of its debug info an 'objfile'
    # libc_objfile_name. e.g. '/usr/lib/debug/lib64/libc-2.16.so.debug'
    libc_objfile_name_pattern = r'libc.*\.so'
    frame = gdb.newest_frame()
    while frame:
        symtab = frame.find_sal().symtab
        if symtab is not None:
            objfile_name = symtab.objfile.filename
        else:
            objfile_name = ''
        logging.debug('F: %s, %s' % (frame, objfile_name))
        if skip_libc_symbols and re.match(r'libc.*\.so', os.path.basename(objfile_name)):
            return
        try:
            block = frame.block()
        except RuntimeError:
            block = None
        while block:
            logging.debug('B: %s, %s' % (block, block.function))
            for symbol in block:
                try:
                    value = frame.read_var(symbol, block)
                except gdb.error:
                    # typedefs etc don't have a value
                    pass
                else:
                    sys.stdout.write('%s: %s\n' % (symbol, value))
            block = block.superblock
        frame = frame.newer()

def dump_globals(names):
    for i in names:
        s = gdb.lookup_global_symbol(i)
        if s is not None:
            sys.stdout.write('%s: %s\n' % (s, s.value()))

inferior_alive = False

def inferior_exited(e):
    global inferior_alive
    inferior_alive = False
    sys.stdout.write('inferior exited with code: %d\n' % (e.exit_code))

def run_and_dump_vars_each_step():
    # precondition: inferior not running
    # NOTE: only handles single threaded programs
    global inferior_alive
    gdb.execute('start')
    inferior_alive = True
    gdb.events.exited.connect(inferior_exited)
    while inferior_alive:
        dump_all_vars()
        gdb.execute('step')
    gdb.execute('quit')

logging.basicConfig(format='%(message)s', level=LOG_LEVEL)
gdb.execute('set pagination no')
gdb.execute('set python print-stack full')
run_and_dump_vars_each_step()
