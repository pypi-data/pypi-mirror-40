#
# Copyright (c) 2016 Stefan Seefeld
# All rights reserved.
#
# This file is part of Faber. It is made available under the
# Boost Software License, Version 1.0.
# (Consult LICENSE or http://www.boost.org/LICENSE_1_0.txt)

from __future__ import absolute_import
from . import scheduler
from .feature import lazy_set
from .feature.condition import expr as fexpr
from .artefact import artefact
from .module import module
from .cache import optioncache
from .error import error_reporter
from .utils import aslist
from . import config as C
import logging
import warnings
from os.path import exists, join

builtin_formatwarning = warnings.formatwarning


def formatwarning(message, category, *args, **kwds):
    if category is UserWarning:
        # ignore everything except the message
        return 'Warning: {}\n'.format(message)
    else:
        return builtin_formatwarning(message, category, *args, **kwds)


warnings.formatwarning = formatwarning
logger = logging.getLogger(__name__)


def config(script):
    """Read in a config file and return its content."""

    logger.debug('reading config file {}'.format(script))
    if not exists(script):
        raise RuntimeError('config file "{}" not found'.format(script))
    env = {}
    with error_reporter(script), open(script) as f:
        exec(f.read(), env)
    return env


class context(object):
    def __init__(self, srcdir, builddir, goals=[], options={}, parameters={}):
        self.srcdir = srcdir
        self.builddir = builddir
        self.goals = goals
        self.options = optioncache(builddir, options)
        self.parameters = parameters

    def __enter__(self):
        module.init(self.goals, self.options, self.parameters)
        C.init(self.builddir)
        return self

    def __exit__(self, type, value, traceback):
        C.finish()
        module.finish()


def build(goals, options, parameters, srcdir, builddir):
    """build a project. Parameters:

    * goals: list of artefacts to build
    * options: any config options being passed (--with=, --without=)
    * parameters: dictionary of pre-defined parameters
    * srcdir: the source directory
    * builddir: the build directory
    """

    with context(srcdir, builddir, options, parameters):
        m = module('', srcdir, builddir)
        if goals:
            try:
                goals = [a for g in goals for a in artefact.lookup(g)]
            except KeyError as e:
                print('don\'t know how to make {}'.format(e))
                goals = []
                result = False
        else:
            goals = aslist(m.default)
            # if we pick up default goals, check their conditions first
            deps = set([d for g in goals for d in g.features.dependencies()])
            # (allow dependencies to fail)
            scheduler.update(list(deps))

            def check(a):
                if a.condition is None:
                    return True
                elif isinstance(a.condition, fexpr):
                    return a.condition(a.features.eval())
                else:
                    return a.condition

            # now filter by condition
            goals = [g for g in goals if check(g)]
            result = True
        if goals:
            result = scheduler.update(goals)
        elif result:
            print('no goals given and no "default" artefact defined - nothing to do.')
            result = True
    return result


def clean(level, options, parameters, srcdir, builddir):
    """Clean up file artefacts."""

    with context(srcdir, builddir, options, parameters) as c:
        m = module('', srcdir, builddir)  # noqa F841
        scheduler.clean(level)
        C.clean(level)
        if level > 1:
            c.options.clean()
    return True


def info(what, items, options, parameters, srcdir, builddir):
    """print project information, rather than performing a build.
    Parameters are the same as for the `build` function."""

    with context(srcdir, builddir, options, parameters):
        result = True
        if what == 'goals':
            m = module('', srcdir, builddir)
            print('known artefacts:')
            for a in sorted(artefact.iter(), key=lambda a: a.qname):
                print('  {}'.format(a.qname))
            if items:
                try:
                    goals = [a for i in items for a in artefact.lookup(i)]
                except KeyError as e:
                    print('don\'t know how to make {}'.format(e))
                    goals = []
                    result = False
            else:
                goals = aslist(m.default)
            if goals:
                scheduler.print_dependency_graph(goals)
        elif what == 'tools':
            from . import tool
            features = lazy_set(module.params.copy())
            for i in items:
                tool.info(i, features)
    return result


def shell(goals, options, parameters, srcdir, builddir):
    """load module in srcdir but rather than updating any goals,
    simply drop into an interactive shell."""

    import pydoc

    class Helper(pydoc.Helper):
        def __init__(self, env):
            self._env = env
            super(Helper, self).__init__()

        def intro(self):
            self.output.write("""
Welcome the Faber shell's help utility!

To get a list of available artefacts or features, type
"artefacts" or "features".""")

        def help(self, request):
            if isinstance(request, str):
                request = request.strip()
                if request == 'artefacts': self.listartefacts()
                elif request == 'features': self.listfeatures()
                else:
                    return super(Helper, self).help(request)
            else:
                return super(Helper, self).help(request)
            self.output.write('\n')

        def listartefacts(self):
            self.list([k for k, v in self._env.items() if isinstance(v, artefact)])

        def listfeatures(self):
            from .feature import feature
            self.list(feature._registry.keys())

    with context(srcdir, builddir, options, parameters):
        m = module('', srcdir, builddir)
        # Use the module's environment, but inject a few helper functions
        env = m._env.copy()
        env['artefacts'] = list(artefact.iter())
        pydoc.help = Helper(env)
        history = None
        import code
        try:
            import readline
        except ImportError:
            pass
        else:
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(env).complete)
            readline.parse_and_bind('tab: complete')
            history = join(builddir, '.fabhistory')
            try:
                readline.read_history_file(history)
            except IOError:
                pass

        code.interact('Faber interactive shell', local=env)
        if history:
            readline.write_history_file(history)
    return True
