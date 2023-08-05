"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import distutils.cmd
from contextlib import contextmanager
import os
import subprocess


@contextmanager
def cd(new_dir):
    prev_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)


class BuildAngularAppCommand(distutils.cmd.Command):
    description = 'Build the angular application'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        with cd(f"front"):
            command = ['ng', 'build', '--prod=true', '--outputPath=../www']
            self.announce(
                'Running command: %s' % str(command),
                level=distutils.log.INFO)
            subprocess.check_call(command)


setup(
    name='MeowApp',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='2.0.0',

    description='Application Manager For Gnome Desktop',
    long_description="""Allows to edit desktop files""",

    # The project's main homepage.
    url='https://gitlab.com/pnmougel/meow2',

    # Author details
    author='Pierre-Nicolas Mougel',
    author_email='pnmougel@gmail.com',

    # Choose your license
    license='MIT',

    cmdclass={
        'build_angular': BuildAngularAppCommand,
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='applications desktop',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'pyxdg==0.26',
        'cefpython3==66.0',
        'pygobject==3.30.4',
        'requests==2.21.0',
        'flask==1.0.2',
        'flask-json==0.3.3',
        'flask-cors==3.0.7',
    ],

    # package_data={'': ['www/*', 'www/*/*', 'www/*/*/*']},
    # Include the content of MANIFEST.in
    include_package_data=True,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file.txt'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'meow=meow.app:run_all',
            'meow_server=meow.meow_server:start_server',
            'meow_gui=meow.front:start_gui',
        ],
    },
)