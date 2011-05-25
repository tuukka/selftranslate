
Selftranslate
-------------

Selftranslate is a Django application for translating other Django
applications and projects. It provides a web interface for editing the
translation files (po files) and compiles the updated files to mo
files that Django loads for localisation of the project in various
languages.

Copyright
---------

Copyright 2011 Tuukka Hastrup <Tuukka.Hastrup@iki.fi>
Copyright 2011 Seravo Oy <tuukka@seravo.fi>

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

For more details, please see the file LICENSE.txt.

Installation
------------

0. Install translate-toolkit, e.g.

pip install translate-toolkit

1. Add selftranslate to your Python path and to the INSTALLED_APPS
setting in the settings.py file of your Django project.

2. Add the following entry to the URLconf of your Django project file
urls.py:

(r'^selftranslate/', include('selftranslate.urls'), dict(domain='django'))

3. Create symbolic links next to the settings.py file that point to the source 
code directories of those applications that you want to include in the
translation, e.g.: 

ln -s /usr/local/lib/python2.5/site-packages/booki booki-src

3. Add localisations to your project by running the following after
replacing language-code with en, es, de etc.:

django-admin.py makemessages -s language-code

3.1. If you want users to be able to start new translations, add a localisation
with the language code xx to be used as a template:

django-admin.py makemessages -s xx

4. Enable the localisations by USE_I18N=True in settings.py.

5. If the translatable texts change, make the updates available to the 
translations by running the following:

django-admin.py makemessages -s -a
