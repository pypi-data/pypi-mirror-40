#! /usr/bin/env python3
# -*- coding: utf-8 -*

# Homepage: https://github.org/rpuntaie/stpl
# License: See LICENSE file

# The SimpleTemplate code is taken from bottle (www.bottlepy.org)

import sys
import os
import re
import functools
import shutil

DEBUG = False

py3k = sys.version_info.major > 2
if py3k:
    unicode = str
    from collections.abc import MutableMapping as DictMixin
else:  # 2.x
    unicode = unicode
    from collections import MutableMapping as DictMixin

TEMPLATE_PATH = ['./', './views/']
TEMPLATES = {}

def view(tpl_name, **defaults):
    """ Decorator: renders a template for a handler.
        The handler can control its behavior like that:

          - return a dict of template vars to fill out the template
          - return something other than a dict and the view decorator will not
            process the template, but return the handler result as is.
            This includes returning a HTTPResponse(dict) to get,
            for instance, JSON with autojson or other castfilters.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (dict, DictMixin)):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)
            elif result is None:
                return template(tpl_name, defaults)
            return result

        return wrapper

    return decorator

# Some helpers for string/byte handling
def tob(s, enc='utf8'):
    if isinstance(s, unicode):
        return s.encode(enc)
    return b'' if s is None else bytes(s)

def touni(s, enc='utf8', err='strict'):
    if isinstance(s, bytes):
        return s.decode(enc, err)
    return unicode("" if s is None else s)

class TemplateError(Exception):
    pass

# A bug in functools causes it to break if the wrapper is an instance method
def update_wrapper(wrapper, wrapped, *a, **ka):
    try:
        functools.update_wrapper(wrapper, wrapped, *a, **ka)
    except AttributeError:
        pass

class cached_property(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property. """

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, cls):
        if obj is None: return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

def html_escape(string):
    """ Escape HTML special characters ``&<>`` and quotes ``'"``. """
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')\
                 .replace('"', '&quot;').replace("'", '&#039;')

def html_quote(string):
    """ Escape and quote a string to be used as an HTTP attribute."""
    return '"%s"' % html_escape(string).replace('\n', '&#10;')\
                    .replace('\r', '&#13;').replace('\t', '&#9;')

class BaseTemplate(object):
    """ Base class and minimal API for template adapters """
    extensions = ['tpl', 'html', 'thtml', 'stpl']
    settings = {}  #used in prepare()
    defaults = {}  #used in render()

    def __init__(self,
                 source=None,
                 name=None,
                 lookup=None,
                 encoding='utf8', **settings):
        """ Create a new template.
        If the source parameter (str or buffer) is missing, the name argument
        is used to guess a template filename. Subclasses can assume that
        self.source and/or self.filename are set. Both are strings.
        The lookup, encoding and settings parameters are stored as instance
        variables.
        The lookup parameter stores a list containing directory paths.
        The encoding parameter should be used to decode byte strings or files.
        The settings parameter contains a dict for engine-specific settings.
        """
        self.name = name
        self.source = source.read() if hasattr(source, 'read') else source
        self.filename = source.filename if hasattr(source, 'filename') else None
        self.lookup = [os.path.abspath(x) for x in lookup] if lookup else []
        self.encoding = encoding
        self.settings = self.settings.copy()  # Copy from class variable
        self.settings.update(settings)  # Apply
        if not self.source and self.name:
            self.filename = self.search(self.name, self.lookup)
            if not self.filename:
                raise TemplateError('Template %s not found.' % repr(name))
        if not self.source and not self.filename:
            raise TemplateError('No template specified.')
        self.prepare(**self.settings)

    @classmethod
    def search(cls, name, lookup=None):
        """ Search name in all directories specified in lookup.
        First without, then with common extensions. Return first hit. """

        for spath in lookup:
            spath = os.path.abspath(spath) + os.sep
            fname = os.path.abspath(os.path.join(spath, name))
            if not fname.startswith(spath): continue
            if os.path.isfile(fname): return fname
            for ext in cls.extensions:
                if os.path.isfile('%s.%s' % (fname, ext)):
                    return '%s.%s' % (fname, ext)

    @classmethod
    def global_config(cls, key, *args):
        """ This reads or sets the global settings stored in class.settings. """
        if args:
            cls.settings = cls.settings.copy()  # Make settings local to class
            cls.settings[key] = args[0]
        else:
            return cls.settings[key]

    def prepare(self, **options):
        """ Run preparations (parsing, caching, ...).
        It should be possible to call this again to refresh a template or to
        update settings.
        """
        raise NotImplementedError

    def render(self, *args, **kwargs):
        """ Render the template with the specified local variables and return
        a single byte or unicode string. If it is a byte string, the encoding
        must match self.encoding. This method must be thread-safe!
        Local variables may be provided in dictionaries (args)
        or directly, as keywords (kwargs).
        """
        raise NotImplementedError

class SimpleTemplate(BaseTemplate):
    def prepare(self,
                escape_func=html_escape,
                noescape=False,
                syntax=None, **ka):
        self.cache = {}
        enc = self.encoding
        self._str = lambda x: touni(x, enc)
        self._escape = lambda x: escape_func(touni(x, enc))
        self.syntax = syntax
        if noescape:
            self._str, self._escape = self._escape, self._str

    @cached_property
    def co(self):
        return compile(self.code, self.filename or '<string>', 'exec')

    @cached_property
    def code(self):
        source = self.source
        if not source:
            with open(self.filename, 'rb') as f:
                source = f.read()

        source, encoding = touni(source), 'utf8'

        parser = StplParser(source, encoding=encoding, syntax=self.syntax)
        code = parser.translate()
        self.encoding = parser.encoding
        return code

    def _rebase(self, _env, _name=None, **kwargs):
        _env['_rebase'] = (_name, kwargs)

    def _include(self, _env, _name=None, **kwargs):
        env = _env.copy()
        env.update(kwargs)
        if _name not in self.cache:
            self.cache[_name] = self.__class__(name=_name, lookup=self.lookup, syntax=self.syntax)
        return self.cache[_name].execute(env['_stdout'], env)

    def execute(self, _stdout, kwargs):
        env = self.defaults.copy()
        env.update(kwargs)
        env.update({
            '_stdout': _stdout,
            '_printlist': _stdout.extend,
            'include': functools.partial(self._include, env),
            'rebase': functools.partial(self._rebase, env),
            '_rebase': None,
            '_str': self._str,
            '_escape': self._escape,
            'get': env.get,
            'setdefault': env.setdefault,
            'defined': env.__contains__
        })
        exec(self.co, env)
        if env.get('_rebase'):
            subtpl, rargs = env.pop('_rebase')
            rargs['base'] = ''.join(_stdout)  #copy stdout
            del _stdout[:]  # clear stdout
            return self._include(env, subtpl, **rargs)
        return env

    def render(self, *args, **kwargs):
        """ Render the template using keyword arguments as local variables. """
        env = {}
        stdout = []
        for dictarg in args:
            env.update(dictarg)
        env.update(kwargs)
        self.execute(stdout, env)
        return ''.join(stdout)


class StplSyntaxError(TemplateError):

    pass


class StplParser(object):
    """ Parser for stpl templates. """
    _re_cache = {}  #: Cache for compiled re patterns

    # This huge pile of voodoo magic splits python code into 8 different tokens.
    # We use the verbose (?x) regex mode to make this more manageable

    _re_tok = _re_inl = r'''(
        [urbURB]*
        (?:  ''(?!')
            |""(?!")
            |'{6}
            |"{6}
            |'(?:[^\\']|\\.)+?'
            |"(?:[^\\"]|\\.)+?"
            |'{3}(?:[^\\]|\\.|\n)+?'{3}
            |"{3}(?:[^\\]|\\.|\n)+?"{3}
        )
    )'''

    _re_inl = _re_tok.replace(r'|\n', '')  # We re-use this string pattern later

    _re_tok += r'''
        # 2: Comments (until end of line, but not the newline itself)
        |(\#.*)

        # 3: Open and close (4) grouping tokens
        |([\[\{\(])
        |([\]\}\)])

        # 5,6: Keywords that start or continue a python block (only start of line)
        |^([\ \t]*(?:if|for|while|with|try|def|class)\b)
        |^([\ \t]*(?:elif|else|except|finally)\b)

        # 7: Our special 'end' keyword (but only if it stands alone)
        |((?:^|;)[\ \t]*end[\ \t]*(?=(?:%(block_close)s[\ \t]*)?\r?$|;|\#))

        # 8: A customizable end-of-code-block template token (only end of line)
        |(%(block_close)s[\ \t]*(?=\r?$))

        # 9: And finally, a single newline. The 10th token is 'everything else'
        |(\r?\n)
    '''

    # Match the start tokens of code areas in a template
    _re_split = r'''(?m)^[ \t]*(\\?)((%(line_start)s)|(%(block_start)s))'''
    # Match inline statements (may contain python strings)
    _re_inl = r'''%%(inline_start)s((?:%s|[^'"\n]+?)*?)%%(inline_end)s''' % _re_inl

    # add the flag in front of the regexp to avoid Deprecation warning (see Issue #949)
    # verbose and dot-matches-newline mode
    _re_tok = '(?mx)' + _re_tok
    _re_inl = '(?mx)' + _re_inl


    default_syntax = '<% %> % {{ }}'

    def __init__(self, source, syntax=None, encoding='utf8'):
        self.source, self.encoding = touni(source, encoding), encoding
        self.set_syntax(syntax or self.default_syntax)
        self.code_buffer, self.text_buffer = [], []
        self.lineno, self.offset = 1, 0
        self.indent, self.indent_mod = 0, 0
        self.paren_depth = 0

    def get_syntax(self):
        """ Tokens as a space separated string (default: <% %> % {{ }}) """
        return self._syntax

    def set_syntax(self, syntax):
        self._syntax = syntax
        self._tokens = syntax.split()
        if syntax not in self._re_cache:
            names = 'block_start block_close line_start inline_start inline_end'
            etokens = map(re.escape, self._tokens)
            pattern_vars = dict(zip(names.split(), etokens))
            patterns = (self._re_split, self._re_tok, self._re_inl)
            patterns = [re.compile(p % pattern_vars) for p in patterns]
            self._re_cache[syntax] = patterns
        self.re_split, self.re_tok, self.re_inl = self._re_cache[syntax]

    syntax = property(get_syntax, set_syntax)

    def translate(self):
        if self.offset: raise RuntimeError('Parser is a one time instance.')
        while True:
            m = self.re_split.search(self.source, pos=self.offset)
            if m:
                text = self.source[self.offset:m.start()]
                self.text_buffer.append(text)
                self.offset = m.end()
                if m.group(1):  # Escape syntax
                    line, sep, _ = self.source[self.offset:].partition('\n')
                    self.text_buffer.append(self.source[m.start():m.start(1)] +
                                            m.group(2) + line + sep)
                    self.offset += len(line + sep)
                    continue
                self.flush_text()
                self.offset += self.read_code(self.source[self.offset:],
                                              multiline=bool(m.group(4)))
            else:
                break
        self.text_buffer.append(self.source[self.offset:])
        self.flush_text()
        return ''.join(self.code_buffer)

    def read_code(self, pysource, multiline):
        code_line, comment = '', ''
        offset = 0
        while True:
            m = self.re_tok.search(pysource, pos=offset)
            if not m:
                code_line += pysource[offset:]
                offset = len(pysource)
                self.write_code(code_line.strip(), comment)
                break
            code_line += pysource[offset:m.start()]
            offset = m.end()
            _str, _com, _po, _pc, _blk1, _blk2, _end, _cend, _nl = m.groups()
            if self.paren_depth > 0 and (_blk1 or _blk2):  # a if b else c
                code_line += _blk1 or _blk2
                continue
            if _str:  # Python string
                code_line += _str
            elif _com:  # Python comment (up to EOL)
                comment = _com
                if multiline and _com.strip().endswith(self._tokens[1]):
                    multiline = False  # Allow end-of-block in comments
            elif _po:  # open parenthesis
                self.paren_depth += 1
                code_line += _po
            elif _pc:  # close parenthesis
                if self.paren_depth > 0:
                    # we could check for matching parentheses here, but it's
                    # easier to leave that to python - just check counts
                    self.paren_depth -= 1
                code_line += _pc
            elif _blk1:  # Start-block keyword (if/for/while/def/try/...)
                code_line, self.indent_mod = _blk1, -1
                self.indent += 1
            elif _blk2:  # Continue-block keyword (else/elif/except/...)
                code_line, self.indent_mod = _blk2, -1
            elif _end:  # The non-standard 'end'-keyword (ends a block)
                self.indent -= 1
            elif _cend:  # The end-code-block template token (usually '%>')
                if multiline: multiline = False
                else: code_line += _cend
            else:  # \n
                self.write_code(code_line.strip(), comment)
                self.lineno += 1
                code_line, comment, self.indent_mod = '', '', 0
                if not multiline:
                    break

        return offset

    def flush_text(self):
        text = ''.join(self.text_buffer)
        del self.text_buffer[:]
        if not text: return
        parts, pos, nl = [], 0, '\\\n' + '  ' * self.indent
        for m in self.re_inl.finditer(text):
            prefix, pos = text[pos:m.start()], m.end()
            if prefix:
                parts.append(nl.join(map(repr, prefix.splitlines(True))))
            if prefix.endswith('\n'): parts[-1] += nl
            parts.append(self.process_inline(m.group(1).strip()))
        if pos < len(text):
            prefix = text[pos:]
            lines = prefix.splitlines(True)
            if lines[-1].endswith('\\\\\n'): lines[-1] = lines[-1][:-3]
            elif lines[-1].endswith('\\\\\r\n'): lines[-1] = lines[-1][:-4]
            parts.append(nl.join(map(repr, lines)))
        code = '_printlist((%s,))' % ', '.join(parts)
        self.lineno += code.count('\n') + 1
        self.write_code(code)

    @staticmethod
    def process_inline(chunk):
        if chunk[0] == '!': return '_str(%s)' % chunk[1:]
        return '_escape(%s)' % chunk

    def write_code(self, line, comment=''):
        code = '  ' * (self.indent + self.indent_mod)
        code += line.lstrip() + comment + '\n'
        self.code_buffer.append(code)


def template(*args, **kwargs):
    """
    Get a rendered template as a string iterator.
    You can use a name, a filename or a template string as first parameter.
    Template rendering arguments can be passed as dictionaries
    or directly (as keyword arguments).
    """
    tpl = args[0] if args else None
    for dictarg in args[1:]:
        kwargs.update(dictarg)
    adapter = kwargs.pop('template_adapter', SimpleTemplate)
    lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    tplid = (id(lookup), tpl)
    if tplid not in TEMPLATES or DEBUG:
        settings = kwargs.pop('template_settings', {})
        if isinstance(tpl, adapter):
            TEMPLATES[tplid] = tpl
            if settings: TEMPLATES[tplid].prepare(**settings)
        elif "\n" in tpl or "{" in tpl or "%" in tpl or '$' in tpl:
            TEMPLATES[tplid] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tplid] = adapter(name=tpl, lookup=lookup, **settings)
    if not TEMPLATES[tplid]:
        abort(500, 'Template (%s) not found' % tpl)
    return TEMPLATES[tplid].render(kwargs)


g_include = []

def stpl(file_or_string,**kw):
    return template(file_or_string
            ,template_lookup = [os.getcwd(),os.path.dirname(os.getcwd())]+g_include
            ,**kw
            )


def main(**args):
    import codecs
    import sys
    import argparse

    if not args:
        parser = argparse.ArgumentParser(description=
                '''Expands bottle SimpleTemplate. See https://bottlepy.org/docs/dev/stpl.html.
                - stands for stdin. If not a file, then the string is expanded.
                ''')
        parser.add_argument( '-I', action='append', metavar='folder', nargs=1,
                help='Add folders to look for templates')
        parser.add_argument('file_or_string',
                help='If the input file ends in .stpl this is automatically dropped when a directory is given')
        parser.add_argument('directory', nargs='?',
                help='If no directory, the result is printed to stdout.')
        parser.add_argument('code', nargs='*',
                help='Further parameters are python code, to define variables that can be used during template expansion.')
        args = parser.parse_args().__dict__

    if 'I' in args and args['I']:
        g_include[:] = functools.reduce(lambda x,y:x+y,args['I'],[])

    if 'code' in args and args['code'] is not None:
        code = '\n'.join(args['code'])
        eval(compile(code,'<string>','exec'),globals())

    filename = file_or_string = args['file_or_string']
    directory = args['directory']

    htmlout = False
    file = None
    isfile = os.path.isfile(file_or_string)
    if not isfile and file_or_string == '-':
        try:
            sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
        except: pass
        file_or_string = sys.stdin.read()
    elif isfile:
        file = file_or_string.replace('\\','/')
        htmlout = '.html' in file #file = 'x.html.stpl'
        with open(file,'r',encoding='utf-8') as f:
            file_or_string = f.read()

    g = globals()
    g['__file__'] = file

    outfile = None
    opnwrite = lambda x: open(x,'w',encoding='utf-8')
    try:
        if directory is None or directory=='-':
            try:
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            except: pass
            outfile = sys.stdout
        else:
            if directory.endswith('/') or directory.endswith('\\'):
                tmpdir = directory
            else:
                tmpdir = os.path.dirname(directory)
            try:
                os.makedirs(tmpdir)
            except:
                pass
            if os.path.isdir(directory):
                if isfile:
                    if filename.endswith('.stpl'):
                        outfilename = os.path.join(directory,filename[:-5])
                    else:
                        outfilename = os.path.join(directory,filename)
                else:
                    raise ValueError("Either no input file or no output file was given")
            else:
                outfilename = directory
            outfile  = opnwrite(outfilename)
        if htmlout:
            result = stpl(file_or_string,**g)
        else:
            result = stpl(file_or_string,template_settings = {'escape_func':lambda x:x},**g)
        outfile.write(result)
    finally:
        if outfile is not None and outfile != sys.stdout:
            outfile.close()

if __name__ == '__main__':
    main() #pragma: no cover

