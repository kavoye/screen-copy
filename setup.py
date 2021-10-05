from cx_Freeze import setup, Executable

executables = [Executable('main.py', target_name = 'Screen Copy', icon = "lib/screenshot-icon.ico", base = "Win32GUI")]

excludes = ['asyncio', 'pytz', 'html', 'lib2to3',
 'concurrent', 'curses', 'setuptools', 'bs4', 'arrow',
  'unittest', 'pydoc_data', 'bz2', 'test', 'idna', 'lxml', 'xmlrpc']

include_files = ['lib/', 'post_clean-up.bat', 'config.cfg']

zip_include_packages = ['collections', 'encodings', 'importlib', 'collections', 'et_xmlfile',
 'http', 'logging', 'urllib', 'urllib3', 'xml', 'email', 'json']

options = {
    'build_exe': {
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,     
    }
}

setup(name = 'Screen Copy',
      version = '0.1',
      executables = executables,
      options = options)