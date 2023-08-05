import subprocess
import platform
import os.path


__all__ = [
    'run',
    'main',
]


def run() -> int:
    import argparse
    import sys

    # Copying the environment variables
    env = os.environ.copy()

    # Setting up the launcher's ArgumentParser
    parser = argparse.ArgumentParser(
        prog='pypath-setup')
    parser.add_argument('--dry-run', dest='dryrun', action='store_true',
        help='only show debug information')
    parser.add_argument('--debug', action='store_true',
        help='display debug messages')
    parser.add_argument('--venv', type=str,
        help='set the virtualenv to use')
    parser.add_argument('executable', type=str,
        help='path to blenderplayer to use')
    options, arguments = parser.parse_known_args()

    def debug(*args, **kargs):
        if options.dryrun or options.debug:
            print('[ PID:', os.getpid(), ']', *args, **kargs)

    # Check if we are running in a virtualenv
    virtualenv = env.get('VIRTUAL_ENV', None)
    if not virtualenv:
        virtualenv = options.venv

        if not virtualenv:
            if os.path.isdir('.venv'):
                debug('Found local virtualenv .venv folder')
                virtualenv = '.venv'

        if not virtualenv:
            raise ValueError('--venv must be specified if not in a virtualenv')

        return subprocess.call(
            [get_python_executable(virtualenv), *sys.argv],
            env={ **env, 'VIRTUAL_ENV': virtualenv })

    # Update PYTHONPATH
    pypath = ' '.join(sys.path)
    debug('PYTHONPATH: "%s"' % pypath)
    env.update({
        'PYTHONPATH': pypath
    })

    # Reconstructing the command the user wants to run in the patched environment
    command = '%s %s' % (options.executable, ' '.join(arguments))
    debug('Command:', command)

    if options.dryrun:
        return 0

    return run_in_shell(command, env=env)


def main():
    exit(run())


if platform.system() == 'Windows':

    def get_python_executable(virtualenv):
        return os.path.join(virtualenv, 'Script', 'python')

    def run_in_shell(command, env):
        return subprocess.call(
            command, shell=True, env=env)

else:

    def get_python_executable(virtualenv):
        return os.path.join(virtualenv, 'bin', 'python')

    def run_in_shell(command, env):
        '''
        Try to handle UNIX case where user can have a custom shell with aliases.
        '''
        shell = env.get('SHELL', None)
        if shell:
            return subprocess.call(
                [shell, '-i', '-c', command], env=env)

        return subprocess.call(
            command, shell=True, env=env)
