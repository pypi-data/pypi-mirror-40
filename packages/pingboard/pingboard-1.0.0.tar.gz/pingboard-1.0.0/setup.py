from setuptools import setup

from pingboard.const import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(name='pingboard',
    version=__version__,
    description='This curses based script displays a dashboard of hosts that it sends ICMP echo request packets (i.e. ping) and their responses',
    long_description=long_description,
    url='http://bitbucket.org/go8ose/pingboard',
    author='Geoff Crompton',
    author_email='geoff+pingboard@cromp.id.au',
    license='GPL3+',
    classifiers = ['Development Status :: 5 - Production/Stable',
        'Environment :: Console :: Curses',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=['pingboard'],
    zip_safe=False,
	entry_points={
        'console_scripts': [
            "pingboard = pingboard.__init__:main",
        ]
    },
)

