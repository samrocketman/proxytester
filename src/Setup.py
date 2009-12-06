from distutils.core import setup
import py2exe
# Filled out required information for setup.py from http://docs.python.org/distutils/setupscript.html
setup(name="Proxy Tester",
      #Version = Major.Minor.PatchSet
      version="0.5.1",
      description="Tests proxy servers and generates wpad.dat for use. See help command for more info.",
      url="http://sourceforge.net/projects/proxytest",
      author="coreyfournier, mpvenable, sag47",
      author_email="@users.sourceforge.net",
      console=['proxytester.py'],
	  zipfile=None,
      options={
                "py2exe":{
                        "includes": ['lib'],
                        "bundle_files": 1
                }
      })