import os
import sys
import platform
import subprocess
from setuptools import setup
from setuptools import find_packages
from wheel.bdist_wheel import bdist_wheel

PACKAGE_NAME = 'downward_dlr'


def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README'), 'r').read()


class BuildFastDownward(bdist_wheel):

    def run(self):
        release = 'release64' if platform.architecture()[0] == '64bit' else 'release32'
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        package_dir = os.path.join(cur_dir, PACKAGE_NAME)
        build_command = str(os.path.join(package_dir, 'build.py')) + " " + release
	print "building fast downward..."
        build_process = subprocess.Popen([build_command], cwd=package_dir,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        for c in iter(lambda: build_process.stdout.read(1), ''):
            sys.stdout.write(c)

        for c in iter(lambda: build_process.stderr.read(1), ''):
            sys.stdout.write(c)

        bdist_wheel.run(self)


setup(
    name=PACKAGE_NAME,
    packages=find_packages(),
    include_package_data=True,
    cmdclass={'bdist_wheel': BuildFastDownward},
    entry_points={'console_scripts': ['fast-downward=' + PACKAGE_NAME + '.downward_dlr:dwdlr_main']},
    version='0.0.3',
    author='Christoph Suerig',
    author_email='christoph.suerig@dlr.de',
    license='GNU General Public License Version 3',
    description=PACKAGE_NAME + ' is a fork of the Fast-Downward Planning System (www.fast-downward.org)',
    long_description=get_readme(),
    keywords='semantic planning pddl fast downward planner fast-downward domain-independent',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: C++',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering'
    ]







)
