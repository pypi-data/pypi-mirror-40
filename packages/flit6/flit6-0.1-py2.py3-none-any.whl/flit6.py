import glob
import logging
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser


log = logging.getLogger(__name__)

__version__ = "0.1"


def validate_env():
    log.debug("checking flit6's python runtime")
    if sys.version_info.major != 2:
        sys.exit("flit6 itself should only be run in python2")

    try:
        import pip
    except ImportError:
        sys.exit("flit6 requires a python2 installation with pip")

    log.debug("checking for presence of a python3 runtime")
    try:
        output = subprocess.check_output(["python3", "-V"])
    except subprocess.CalledProcessError:
        sys.exit("flit6 requires python3 available to subprocess")
    else:
        log.debug("python3 seems ok %s", output)

    log.debug("checking for presence of a python3 flit installation")
    try:
        output = subprocess.check_output(["python3", "-m", "flit", "-V"])
    except subprocess.CalledProcessError:
        sys.exit("flit6 requires a python3 flit installation")
    else:
        log.debug("flit seems ok %s", output)


def clean():
    log.debug("nuking ./dist/")
    shutil.rmtree("./dist/", ignore_errors=True)


def build():
    log.debug("running flit build")
    output = subprocess.check_output(["python3", "-m", "flit", "build"])
    log.debug("flit build finished\n%s", output)
    log.debug("checking for generated wheels")
    wheels = glob.glob("./dist/*.whl")
    if len(wheels) > 1:
        log.warning("found many wheels, returning newest one %s", wheels)
        return max(wheels, key=lambda f: os.stat(f).st_mtime)
    elif len(wheels) == 1:
        [wheel] = wheels
        log.debug("found wheel %s", wheel)
        return wheel
    else:
        log.debug("no wheel")
    sdists = glob.glob("./dist/*.tar.gz")  # yeah, there are zip etc but who cares
    if len(sdists) > 1:
        log.warning("found many sdists, returning newest one %s", sdists)
        return max(sdists, key=lambda f: os.stat(f).st_mtime)
    elif len(sdists) == 1:
        [sdist] = sdists
        log.debug("found sdist %s", sdist)
        return sdist
    else:
        log.debug("no sdist")
    log.error("no dist generated")
    sys.exit(1)


def install(fname):
    subprocess.check_call([sys.executable, "-m", "pip", "install", fname])


def main():
    v = "%(prog)s v{}".format(__version__)
    if sys.version_info >= (3,):
        import flit
        return flit.main()
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser(prog="flit6", description="cross-compat flit install")
    parser.add_argument("-V", "--version", action="version", version=v)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcmd")
    subparsers.add_parser("install", help="Install the package")
    args = parser.parse_args()
    validate_env()
    if args.subcmd == "install":
        clean()
        fname = build()
        install(fname)
