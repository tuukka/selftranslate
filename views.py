
import os, time
from glob import glob

try:
    import simplejson as json
    json.dumps
except (ImportError, NameError):
    import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.importlib import import_module

from translate.storage.po import pofile
from translate.tools.pocompile import convertmo

def purge_gettext_cache():
    """remove stale translations from django's gettext cache"""
    import gettext as gettext_module
    gettext_module._translations = {}
    import django.utils.translation.trans_real as trans
    trans._translations = {}
    trans._active = {}
    trans._default = None

def view_reload(request):
    purge_cache()

    return HttpResponse("reloaded", mimetype="text/plain")

def project_path():
    if settings.SETTINGS_MODULE is not None:
        # find locale dir for project
        parts = settings.SETTINGS_MODULE.split('.')
        project = import_module(parts[0])
        projectpath = os.path.join(os.path.dirname(project.__file__), 'locale')
    else:
        projectpath = None
    return projectpath

def locale_path(language, domain):
    projectpath = project_path()
    if projectpath is not None:
        # find locate file
        localepath = os.path.join(projectpath, language, 'LC_MESSAGES', domain+".po")
    else:
        localepath = None    

    return localepath

def view_languages(request, language=None, domain="django"):
    localepath = project_path()
    languages = [os.path.basename(f) for f in glob(os.path.join(localepath, "*"))]
    if language:
        languages = [l for l in languages if l.startswith(language)]
    return render_to_response("languages.html", dict(languages=languages))

def view_editor(request, language, domain="django"):
    localepath = locale_path(language, domain)
    translation = pofile(file(localepath))
#        return HttpResponse(translation, mimetype="text/plain")        
    return render_to_response("editor.html", dict(language=language, units=translation.getunits()))

def view_catalog(request, language, domain="django"):
    localepath = locale_path(language, domain)
    translation = pofile(file(localepath))

    locations = [x for u in translation.getunits() for x in u.getlocations()]
    prefix = len(os.path.commonprefix(locations))

    catalog = [dict(key=u.getsource(), value=u.gettarget(), fuzzy=u.isfuzzy(),
                    context=u.getcontext(),
                    locations=[l[prefix:] for l in u.getlocations()],
                    notes=u.getnotes(), obsolete=u.isobsolete(),
                    allcomments=u.allcomments)
               for u in translation.getunits()]

    # application/json
    return HttpResponse(json.dumps(catalog,  sort_keys=True, indent=4),
                        "text/plain")

def view_unit(request, language, domain="django"):
    localepath = locale_path(language, domain)
    # XXX in case of POST, use file locking to avoid concurrency issues
    translation = pofile(file(localepath))
    
    if request.method == 'POST':
        msgid = request.POST['key']
        msgstr = request.POST['value']
        unit = translation.findunit(msgid)

        unit.settarget(msgstr)
        unit.markfuzzy(False) # clear fuzzy flag on save if any

        # file names
        t = time.localtime()
        # XXX no subsecond precision here
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", t)
        localepath_backup = localepath+"."+timestamp
        localepath_temp = localepath+".saved"
        mopath = localepath.replace(".po",".mo")
        mopath_temp = mopath + ".saved"

        # backup old .po
        backup = file(localepath_backup, "wb")
        backup.write(file(localepath, "rb").read())
        backup.close()
        # save .po under temp name
        translation.savefile(localepath_temp)
        # overwrite old .po atomically
        os.rename(localepath_temp, localepath)
        # compile .mo under temp name
        _not_empty = convertmo(file(localepath), file(mopath_temp, "wb"), None)
        # overwrite old mo atomically
        os.rename(mopath_temp, mopath)
        
        # deploy immediately in this Django process
        purge_gettext_cache()
    else:
        msgid = request.GET['key']
        unit = translation.findunit(msgid)

        msgstr = unit.gettarget()

    return HttpResponse(msgstr, mimetype="text/plain")        
