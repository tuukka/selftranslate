
Selftranslate
-------------

Selftranslate is a Django application for translating other Django
applications and projects. It provides a web interface for editing the
translation files (po files) and compiles the updated files to mo
files that Django loads for localisation of the project in various
languages.

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

Installation
------------

1. Add selftranslate to your Python path and to the INSTALLED_APPS
setting in the settings.py file of your Django project.

2. Add the following entry to the urlconf of your Django project file
urls.py:
(r'^selftranslate/', include('selftranslate.urls'), dict(domain='django'))

3. Add localisations to your project by running the following after
replacing language-code with en, es, de etc. 
manage.py makemessages language-code.

4. Enable the localisations by USE_I18N=True in settings.py.
