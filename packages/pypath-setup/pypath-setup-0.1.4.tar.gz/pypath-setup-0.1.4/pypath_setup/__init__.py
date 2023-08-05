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

    PYTHONPATH = 'PYTHONPATH'
    VIRTUAL_ENV = 'VIRTUAL_ENV'
    PYPATH_SETUP_EXECUTABLE = 'PYPATH_SETUP_EXECUTABLE'

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
    parser.add_argument('--override', action='store_true',
        help='completely override PYTHONPATH')
    parser.add_argument('executable', type=str,
        help='path to blenderplayer to use')
    options, arguments = parser.parse_known_args()

    def debug(*args, **kargs):
        if options.dryrun or options.debug:
            print('[ PID:', os.getpid(), ']', *args, **kargs)

    # Check if we are running in a virtualenv
    virtualenv = env.get(VIRTUAL_ENV, None)

    # Use specified parameter
    if not virtualenv:
        virtualenv = options.venv

    # Use default `.venv` location
    if not virtualenv:
        if os.path.isdir('.venv'):
            debug('Found local virtualenv .venv folder')
            virtualenv = '.venv'

    # Nothing was found
    if not virtualenv:
        raise ValueError('--venv must be specified if not in a virtualenv')

    # Get python executable in the virtualenv
    python_executable = get_python_executable(virtualenv)

    # Fetch PYTHONPATH from the `sys.path` of the Python executable inside the virtualenv
    pythonpath = subprocess.check_output([python_executable, '-c', 'import os, sys; print(os.pathsep.join(sys.path), end="")'],
        env={ **env, VIRTUAL_ENV: virtualenv }).decode()

    # Construct PYTHONPATH
    if options.override:
        path = pythonpath
    elif PYTHONPATH in env:
        pythonpath = env[PYTHONPATH] + os.pathsep + pythonpath

    # Update environment with new PYTHONPATH
    debug('PYTHONPATH: "%s"' % pythonpath)
    env.update({
        PYTHONPATH: pythonpath
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
        return os.path.join(virtualenv, 'Scripts', 'python')

    def run_in_shell(command, env):
        return subprocess.call(command, shell=True, env=env)

else:

    def get_python_executable(virtualenv):
        return os.path.join(virtualenv, 'bin', 'python')

    def run_in_shell(command, env):
        '''
        Try to handle UNIX case where user can have a custom shell with aliases.
        '''
        shell = env.get('SHELL', None)
        if shell:
            return subprocess.call([shell, '-i', '-c', command], env=env)

        return subprocess.call(command, shell=True, env=env)
