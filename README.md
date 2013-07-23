# About Rewrite

The purpose of the rewrite branch is to do a complete rewrite of proxytester.  When I first wrote proxytester in 2009 I was still new to python and regularly made bad practice and rookie mistakes.  After reviewing the source code I realized a new and complete rewrite was necessary in order to facilitate a better proxy testing program.  Once this is done it will facilitate better contributions, higher quality code base, and position proxytester to the next stage of development and features.

----
## Things to do

* Reorganize the code in a more logical fashion.  Make more use of libraries, functions, and packages.
* write functional tests so that a test suite can be run on the source for quality control.
* remove "SwitchParser.py" and implement optparse or argparse.  These guys obviously did it better than my attempt.
* Integrate George Purkins' pyGeoIP once again since the last attempt on sourceforge broke the source tree.  Going to try that one again :).  It's mostly a problem with SVN development.  Now that we're on Git this won't be a problem any longer with a good workflow.

When this rewrite is completed it will be designated v0.9.  When pyGeoIP is integrated this will be v0.10.
