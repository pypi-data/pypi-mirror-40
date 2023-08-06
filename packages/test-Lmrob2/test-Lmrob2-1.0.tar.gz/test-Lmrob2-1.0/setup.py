import subprocess
import os
import sys
import argparse, shlex, subprocess
from setuptools import setup, Extension
from distutils.command.build_py import build_py as _build_py
import re
class build_py(_build_py):
    """Specialized Python source builder."""
    def run(self):
        command = "./tools/lmrob_lib_so/compile_lmrob_so.sh"
        p = subprocess.Popen(command, shell=True)
        p.wait()
        if not os.path.exists("lmrob/liblmrob.so"):
            raise Exception("liblmrob.so not found. Verify the requirements")
        super().run()
    
def cmp_version(x, y):
    if (x[0] < y[0]):
        return -1
    if (x[0] > y[0]):
        return 1
    if (x[0] == y[0]):
        if len(x) == 1 or len(y) == 1:
            return 0
        return cmp_version(x[1:], y[1:])

# def getRinterface_ext():
#     rinterface_ext = Extension(
#             name = 'lmrob._rinterface',
#             sources = [os.path.join('tools', 'rinterface', '_rinterface.c')],
#             depends = [os.path.join('tools', 'rinterface', 'embeddedr.h'), 
#                        os.path.join('tools', 'rinterface', 'r_utils.h'),
#                        os.path.join('tools', 'rinterface', 'buffer.h'),
#                        os.path.join('tools', 'rinterface', 'sequence.h'),
#                        os.path.join('tools', 'rinterface', 'sexp.h'),
#                        os.path.join('tools', 'rinterface', '_rinterface.h'),
#                        os.path.join('tools', 'rinterface', 'rpy_device.h')
#                        ],
#             include_dirs=[os.path.join('tools', 'rinterface'), '/usr/include/R'],
#             libraries=['R'],
#             library_dirs=['/usr/lib64/R/lib'])
#     return [rinterface_ext]


def _get_r_home(r_bin = "R"):
    
    if (os.getenv('R_ENVIRON') is not None) or (os.getenv('R_ENVIRON_USER') is not None):
        warnings.warn("The environment variable R_ENVIRON or R_ENVIRON_USER is set. Differences between their settings during build time and run time may lead to issues when using rpy2.")

    try:
        r_home = subprocess.check_output((r_bin, "RHOME"),
                                         universal_newlines=True)
    except:
        msg = "Error: Tried to guess R's HOME but no command '%s' in the PATH." % r_bin
        print(msg)
        sys.exit(1)

    r_home = r_home.split(os.linesep)

    #Twist if 'R RHOME' spits out a warning
    if r_home[0].startswith("WARNING"):
        warnings.warn("R emitting a warning: %s" % r_home[0])
        r_home = r_home[1].rstrip()
    else:
        r_home = r_home[0].rstrip()

    if os.path.exists(os.path.join(r_home, 'Renviron.site')):
        warnings.warn("The optional file '%s' is defined. Modifying it between build time and run time may lead to issues when using rpy2." % os.path.join(r_home, 'Renviron.site'))

    return r_home


class RExec(object):
    """ Compilation-related configuration parameters used by R. """

    def __init__(self, r_home):
        if sys.platform == "win32" and "64 bit" in sys.version:
            r_exec = os.path.join(r_home, 'bin', 'x64', 'R')
        else:
            r_exec = os.path.join(r_home, 'bin', 'R')
        self._r_exec = r_exec
        self._version = None

    @property
    def version(self):
        if self._version is not None:
            return self._version
        output = subprocess.check_output((self._r_exec, '--version'), 
                                         universal_newlines = True)
        if not output:
            # sometimes R output goes to stderr
            output = subprocess.check_output((self._r_exec, '--version'), 
                                         stderr = subprocess.STDOUT,
                                         universal_newlines = True)
        output = iter(output.split('\n'))
        rversion = next(output)
        #Twist if 'R --version' spits out a warning
        if rversion.startswith("WARNING"):
            warnings.warn("R emitting a warning: %s" % rversion)
            rversion = next(output)
        print(rversion)
        m = re.match('^R ([^ ]+) ([^ ]+) .+$', rversion)
        if m is None:
            warnings.warn("Unable to extract R's version number from the string: '%s'" % rversion)
            # return dummy version 0.0
            rversion = [0, 0]
        else:
            rversion = m.groups()[1]
            if m.groups()[0] == 'version':
                rversion = [int(x) for x in rversion.split('.')]
            else:
                rversion = ['development', '']
        self._version = rversion
        return self._version

    def cmd_config(self, about, allow_empty=False):
        cmd = (self._r_exec, 'CMD', 'config', about)
        print(subprocess.list2cmdline(cmd))
        output = subprocess.check_output(cmd,
                                         universal_newlines = True)
        output = output.split(os.linesep)
        #Twist if 'R RHOME' spits out a warning
        if output[0].startswith("WARNING"):
            warnings.warn("R emitting a warning: %s" % output[0])
            output = output[1:]
        return output


def getRinterface_ext():
    extra_link_args = []
    extra_compile_args = []
    include_dirs = []
    libraries = []
    library_dirs = []

    #FIXME: crude way (will break in many cases)
    #check how to get how to have a configure step
    define_macros = []

    if sys.platform == 'win32':
        define_macros.append(('Win32', 1))
        if "64 bit" in sys.version:
            define_macros.append(('Win64', 1))
            extra_link_args.append('-m64')
            extra_compile_args.append('-m64')
            # MS_WIN64 only defined by pyconfig.h for MSVC. 
            # See http://bugs.python.org/issue4709
            define_macros.append(('MS_WIN64', 1))
    else:
        define_macros.append(('R_INTERFACE_PTRS', 1))
        define_macros.append(('HAVE_POSIX_SIGJMP', 1))
        define_macros.append(('RIF_HAS_RSIGHAND', 1))
        define_macros.append(('CSTACK_DEFNS', 1))
        define_macros.append(('HAS_READLINE', 1))


    if sys.byteorder == 'big':
        define_macros.append(('RPY_BIGENDIAN', 1))
    else:
        pass

    r_home = _get_r_home()
    rexec = RExec(r_home)
    if rexec.version[0] == 'development' or \
       cmp_version(rexec.version[:2], [3, 2]) == -1:
        warnings.warn("R did not seem to have the minimum required version number")

    ldf = shlex.split(' '.join(rexec.cmd_config('--ldflags')))
    cppf = shlex.split(' '.join(rexec.cmd_config('--cppflags')))
    #lapacklibs = rexec.cmd_config('LAPACK_LIBS', True)
    #blaslibs = rexec.cmd_config('BLAS_LIBS', True)

    parser = argparse.ArgumentParser()
    parser.add_argument('-I', action='append')
    parser.add_argument('-L', action='append')
    parser.add_argument('-l', action='append')

    # compile
    args, unknown = parser.parse_known_args(cppf)
    if args.I is None:
        warnings.warn('No include specified')
    else:
        include_dirs.extend(args.I)
    extra_compile_args.extend(unknown)
    # link
    args, unknown = parser.parse_known_args(ldf)
    # OS X's frameworks need special attention
    if args.L is None:
        # presumably OS X and framework:
        if args.l is None:
            # hmmm... no libraries at all
            warnings.warn('No libraries as -l arguments to the compiler.')
        else:
            libraries.extend([x for x in args.l if x != 'R'])
    else:
        library_dirs.extend(args.L)
        libraries.extend(args.l)
    extra_link_args.extend(unknown)
    
    print("""
    Compilation parameters for lmrob C components:
        include_dirs    = %s
        library_dirs    = %s
        libraries       = %s
        extra_link_args = %s
    """ % (str(include_dirs),
           str(library_dirs), 
           str(libraries), 
           str(extra_link_args)))
    
    rinterface_ext = Extension(
            name = 'lmrob._rinterface',
            sources = [os.path.join('tools', 'rinterface', '_rinterface.c')
                       ],
            depends = [os.path.join('tools', 'rinterface', 'embeddedr.h'), 
                       os.path.join('tools', 'rinterface', 'r_utils.h'),
                       os.path.join('tools', 'rinterface', 'buffer.h'),
                       os.path.join('tools', 'rinterface', 'sequence.h'),
                       os.path.join('tools', 'rinterface', 'sexp.h'),
                       os.path.join('tools', 'rinterface', '_rinterface.h'),
                       os.path.join('tools', 'rinterface', 'rpy_device.h')
                       ],
            include_dirs = [os.path.join('tools', 'rinterface'),] + include_dirs,
            libraries = libraries,
            library_dirs = library_dirs,
            define_macros = define_macros,
            runtime_library_dirs = library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args = extra_link_args
            )

    rpy_device_ext = Extension(
        'lmrob._rpy_device',
        [
            os.path.join('tools', 'rinterface', '_rpy_device.c'),
            ],
        include_dirs = include_dirs + 
        [os.path.join('tools', 'rinterface'), ],
        libraries = libraries,
        library_dirs = library_dirs,
        define_macros = define_macros,
        runtime_library_dirs = library_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args = extra_link_args
        )

    return [rinterface_ext, rpy_device_ext]


if __name__ == '__main__':
    ri_ext = getRinterface_ext()
    libraries = list()
    libraries.append(('r_utils',
                      dict(sources = [os.path.join('tools/rinterface', 'r_utils.c')],
                           include_dirs = ri_ext[0].include_dirs,
                           language = 'c')))
    setup(
        name='test-Lmrob2',
        packages=['lmrob','nlrob'],
        package_dir={
            'lmrob': 'lmrob'},
        package_data={
            'lmrob': ['liblmrob.so']},
        version='1.0',
        author='',
        cmdclass={'build_py': build_py},
        install_requires=[package for package in open("requirements.txt")],
        ext_modules=ri_ext,
        libraries = libraries
    )
