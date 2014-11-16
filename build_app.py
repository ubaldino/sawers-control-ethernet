# coding=utf-8
import sys
import os

if sys.platform.startswith('darwin'):
    from setuptools import setup

    version = os.environ[ 'BUILD_NAME' ]

    APP = [ 'Control/main.py' ]
    DATA_FILES = [ 'Control/LICENSE', 'Control/resources' ]
    PLIST = {
        u'CFBundleName': u'Sawers Control',
        u'CFBundleShortVersionString': version,
        u'CFBundleVersion': version,
        u'CFBundleIdentifier': u'com.sawers.Control-'+version,
        u'LSMinimumSystemVersion': u'1.0',
        u'LSApplicationCategoryType': u'public.app-category.control',
    }
    OPTIONS = {
        'argv_emulation': True,
        'iconfile': 'Control/resources/sawers.ico',
        'includes': ['ino', 'Foundation'],
        'resources': DATA_FILES,
        'optimize': '2',
        'plist': PLIST,
        'bdist_base': 'scripts/darwin/build',
        'dist_dir': 'scripts/darwin/dist'
    }

    setup(
        name="Control-Sawers",
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app']
    )
else:
   print 'No build_app implementation for your system.'
