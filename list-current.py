# Usage: gdb -x list-current.py
# (gdb) list-current

import gdb

def _list_current_source_line(n_lines):
    try:
        frame = gdb.selected_frame()
    except gdb.error, e:
        raise gdb.GdbError(e.message)
    sal = frame.find_sal()
    (filename, line) = (sal.symtab.fullname(), sal.line)
    if n_lines < 0:
        (start, end) = (line + n_lines + 1, line)
    else:
        (start, end) = (line, line + n_lines - 1)
    gdb.execute('list %s:%d, %s:%d' %
                (filename, start, filename, end))

class _ListCurrentSourceLine(gdb.Command):
    '''Usage: list-current [N_LINES], e.g.
    list-current     -- lists current source line
    list-current 10  -- lists 10 lines starting from current source line
    list-current -10 -- lists 10 lines before current source line'''

    def __init__(self):
        gdb.Command.__init__(self, 'list-current', gdb.COMMAND_FILES, gdb.COMPLETE_NONE)

    def invoke(self, arg, from_tty):
        n_lines = 1
        if arg:
            try:
                n_lines = int(arg)
            except ValueError:
                raise gdb.GdbError('argument must be a number, not "%s"' % (arg,))
        _list_current_source_line(n_lines)

_ListCurrentSourceLine()
