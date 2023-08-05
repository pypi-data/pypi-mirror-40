from setuptools import setup

setup(
    name = 'pyXBEE_tne',
    packages = ['xbee_tne'],
    install_requires=['pyserial>=2.7'],
    version = '0.3.8',
    description = 'a library to communicate with the XBEE',
    author='Ruud van der Horst',
    author_email='ik@ruudvdhorst.nl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)