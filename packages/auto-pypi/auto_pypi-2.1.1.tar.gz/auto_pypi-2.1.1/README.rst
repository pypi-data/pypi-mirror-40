Auto-PyPi Command Line Tool
===========================


|PyPI Version| |PyPI Platform| |PyPI License| |PyPI Doc| 


|Mac OS| |Linux|




Why Should I Use This?
**********************

This is a Python command line tool to automatically setup your (updated version) python package onto PyPi. 

As you may know, PyPi indexes (both real and test index) do not allow you to reuse package name (considering version numner), which means you can not upload your package with the same package name together with an identical version numner. 

In another word, you have to change the version number in your ``setup.py`` file before each time you want to upload your modified package. What's more, you also need to remove the old build and egg folder before you run the setup tools. 

You'll find it not convenient at all if you are uploading and testing your package frequently. Even if you are not going to upload and test frequently, each time you remove the previous setup related folders comes with some risks and is still time-consuming. 

By using this command line tool, you will be all set after a single command ``autopypi``. The only thing you need to care about now is the package version number. 

You could chage the version number in the ``setup.py`` file as usual, but I highly recommend you to change a little bit in your ``setup.py`` file making the version number as an input value from the terminal: 

.. code-block:: python

   version_number = input("Input the new version number you are going to use: ")

   setuptools.setup(
       name="auto_pypi",
       version=version_number,
       author="Sen LEI",
       ...)


By doing this, you just need to run the command ``autopypi``, and specify a version number later when it pops up. 



Usage
*****


Use As A Command Line Tool
--------------------------


- Just run ``autopypi`` in terminal, providing *your package's location* and *new version number* later: 

.. code-block:: shell

   Usage: autopypi [OPTIONS] PKG_DIR

     Python command line tool to setup Python package automatically.  
     Example:      $ autopypi your-package-root-directory -r
     Example:      $ cd your-package-root-directory
                   $ autopypi . -r

   Options:
     -r, --real          Use the real PyPi index (instead of test PyPi).
     --help              Show this message and exit.


- Then you'll be asked to input the username and passcode of PyPi / Test-PyPi as usual. 




Documentation
*************

Check out the latest ``auto_pypi`` documentation at `Read the Docs <https://auto_pypi.readthedocs.io/en/latest/>`_


|

|



-----------------------------------

|Sen LEI Website| |Sen LEI Github|







.. |PyPI Platform| image:: https://img.shields.io/pypi/pyversions/auto_pypi.svg?logo=python&logoColor=white
   :target: https://pypi.python.org/pypi/auto_pypi

.. |PyPI License| image:: https://img.shields.io/github/license/Listen180/auto_pypi.svg
   :target: https://github.com/Listen180/auto_pypi/blob/master/LICENSE

.. |PyPI Version| image:: https://img.shields.io/pypi/v/auto_pypi.svg
   :target: https://pypi.python.org/pypi/auto_pypi

.. |PyPI download| image:: https://img.shields.io/pypi/dm/auto_pypi.svg
   :target: https://pypi.python.org/pypi/auto_pypi

.. |PyPI Doc| image:: https://readthedocs.org/projects/auto_pypi/badge
   :target: https://auto_pypi.readthedocs.io/en/latest/



.. |Sen LEI Github| image:: https://img.shields.io/badge/Github-Sen%20LEI-orange.svg?logo=github&longCache=true&style=flat&logoColor=white
   :target: https://github.com/Listen180

.. |Sen LEI Website| image:: https://img.shields.io/badge/Author-Sen%20LEI-orange.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANUAAADVCAMAAAD3nkWxAAACglBMVEUAAAD///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9xjI0NAAAA1XRSTlMAAQIDBAUGBwgJCgsMDg8REhQXGBkaGxwdHh8gIiMkJSYnKCkqKywtLi8wMTI0NTY3ODk6Ozw9Pj9AQUJDREVGR0hJSktMTU5PUFJTVVZZWltcXV5fYGFkZWZnaGlqb3BxcnN0dXZ3ent8fYCBgoOFh4iKi4yNkJGSk5SVlpeZmpydnp+hoqOmp6ipqqusra6vsbKztLW2ubu8vsDDxMXGx8jJy8zNzs/Q0dLT1NXW19jZ3N3e3+Dh4uPk5ebn6Onq6+zt7u/w8fLz9PX29/j5+vv8/f7yOdf5AAAEF0lEQVR42u3da1fVVRAG8Ocgl8BCBQtJirQwqCwIk8DMMpIuplCIXcyiUioLKcssLVMjNCrCrOhCaqGppd1LKSsijgUY4DnP9+kVbzDgv8/ZL2ZY8/sOs+dZs9bMhjHGGGOMMcYYY4wxxhhjjPElPaegeGFxfs55mBgSCh7a1t7FYV3tr67OD0G1tMq3uni2P5qXpUKr+Tv+5mhObb8OGi38lGNrXxKCMmUHOb4D10OTzMYoA2nOgBpVYQbVsxw6nPMCXTSmQYGcL+nmyEyIN6eTrk5eAeFKwnTXUwLRCnsZi37RLTmvm7EJ50OsGZ2M1fELIFRiO2O3PwkyPcd4NECk8ijjEb0ZAqX9yPj8PBnyPMt4rYc4eYOM18BsSPM247cLwsyOMH6RWZClkT7sgCjTh+jDYCYkeZR+PAxJDtOPgxCkgL7MgRx19OUxyNFGX96HGMm99KU3GVIU059CSLGS/qyAFBvoTwOk2E1/WiDFEfrzBaT4if58Dym66U8XpBigP/9CiFCE/kRCEOIf+nMKUvxKf05Aim/pzzFI8Qn9+RhSbKM/r0CKNfSnFlLcRn/KIcV0ehPNhBjf0JevIMfL9GUT5LiTvtwOOVLD9COcCkG204+tkKSMfsyHJAlf04ejIYhSTR8qIUvSDz5mFokQ5l7GrwbSJHzGeH2eAHHmRhifyDVwoCU2vQiJJh+NL9emQaS8Psau9zIIVcPY3QOx6hmrdRBsk4IZjLtJOxmLpkkQLfQ83b2UAOmeiNJNtA4KVHTTRXgpVMje6xL+cqBE8uP9DKavLgl6ZL3JIN6dCV1u+Ijj+bAU+hS3DnF0Q+8UQaep97WPNnZZmwHFLqxp7By5vvNadTb0m1q0on5LY0tbS+OWp6sLp8AYY4wxxhgjTfKVlbVPPbN+bdXV52KCuLxu/xCHDe2rz4N6iXft40gdlYlQ7aZj/D/f3QG9prVyNO+dD6VKj3N0vy+CSncPcixnHoBCj0Q5jjVQZ1mU44muhDJlgxzfmTKoMuUEg/gtE5o0M5hmKFLKoBZDjVAHgzoUghblDG4JtNjD4NqgRHaEwUWyoMMqulgNHXbTRSt06KGLcAgaZNHNDGiwiG5uhAZVdFMFDR6km1XQoJZuapW0Kzf3T8i6Wg4NSuhmHjTIoJtpUOEkXfwCHZro4nXoUOO4SqFDej+DO50OJXYxuCZocVWUgc2FGh8wqD1woOX88sClUGQDg2mAJikHGERHClTJ7eH4ui+CMkW9Dv9t6HFLP8fWtxgKzfuLY/nzWqiUvddh70qP5HWnRyupJ5Og18VvRHi2yM4c6DZrc/fI93zzJdAv5daNhweHE9KhjeXJmCgScxdULK1YkJsIY4wxxhhjjDHGGGOMMcYYY4wxxhhjjBnhP6hK+cPRlZTHAAAAAElFTkSuQmCC&longCache=true&style=flat&logoColor=white
   :target: https://listen180.github.io/LEI-Sen/



.. |org_repo| image:: https://img.shields.io/badge/-repository-green.svg?logo=github&longCache=true&style=flat&logoColor=white
   :target: https://github.com/auto_pypi/




.. |Mac OS| image:: https://img.shields.io/badge/Mac%20OS-green.svg?logo=apple&longCache=true&style=flat&logoColor=white

.. |Linux| image:: https://img.shields.io/badge/Linux-green.svg?logo=linux&longCache=true&style=flat&logoColor=white
