#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import sys
# import os
import platform

from PyInstaller.utils.win32.versioninfo import (
    VarStruct, VarFileInfo, StringStruct, StringTable,
    StringFileInfo, FixedFileInfo, VSVersionInfo, SetVersion,
)
import PyInstaller.__main__

arch = sys.argv[1] if len(sys.argv) > 1 else platform.architecture()[0][:2]
assert arch in ('32', '64')
print('Building %sbit version' % arch)
_x86 = '_x86' if arch == '32' else ''

FILE_DESCRIPTION = 'Media Downloader%s' % (' (32 Bit)' if _x86 else '')

# root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print('Changing working directory to %s' % root_dir)
# os.chdir(root_dir)

exec(compile(open('youtube_dlc/version.py').read(), 'youtube_dlc/version.py', 'exec'))
VERSION = locals()['__version__']

VERSION_LIST = VERSION.split('.')
VERSION_LIST = list(map(int, VERSION_LIST)) + [0] * (4 - len(VERSION_LIST))

print('Version: %s%s' % (VERSION, _x86))
print('Remember to update the version using devscipts\\update-version.py')

VERSION_FILE = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=VERSION_LIST,
        prodvers=VERSION_LIST,
        mask=0x3F,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '040904B0', [
                    StringStruct('Comments', 'Youtube-dlc%s Command Line Interface.' % _x86),
                    StringStruct('CompanyName', 'https://github.com/pukkandan/yt-dlp'),
                    StringStruct('FileDescription', FILE_DESCRIPTION),
                    StringStruct('FileVersion', VERSION),
                    StringStruct('InternalName', 'youtube-dlc%s' % _x86),
                    StringStruct(
                        'LegalCopyright',
                        'pukkandan@gmail.com | UNLICENSE',
                    ),
                    StringStruct('OriginalFilename', 'youtube-dlc%s.exe' % _x86),
                    StringStruct('ProductName', 'Youtube-dlc%s' % _x86),
                    StringStruct('ProductVersion', '%s%s' % (VERSION, _x86)),
                ])]),
        VarFileInfo([VarStruct('Translation', [0, 1200])])
    ]
)

PyInstaller.__main__.run([
    '--name=youtube-dlc%s' % _x86,
    '--onefile',
    '--icon=devscripts/cloud.ico',
    '--exclude-module=youtube_dl',
    '--exclude-module=test',
    '--exclude-module=ytdlp_plugins',
    '--hidden-import=mutagen',
    '--hidden-import=Crypto',
    'youtube_dlc/__main__.py',
])
SetVersion('dist/youtube-dlc%s.exe' % _x86, VERSION_FILE)
