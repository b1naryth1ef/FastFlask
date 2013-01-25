#!/usr/bin/env python
import sys, os

MAN = """
FastFlask Script

Quickly setup a basic directory structure for flask-app development

USAGE:
Create a new app:
  python fastflask.py new <name>
  python fastflask.py new <name> +plugin +plugin2
Dump the config (for easy copying):
  python fastflask.py dump
"""
MODELS = {}

def loadModels():
    for i in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models')):
        if not i[0] in ['.', '_'] and i.endswith('.py'):
            i = i.split('.py')[0]
            try: __import__('models.%s' % i)
            except ImportError:
                print "Couldnt load model %s" % i
                continue
            MODELS[i.lower()] = sys.modules['models.%s' % i]

default_config = {
    'name': None,
    'models': [],
    'opts': [],
}

def newApp(args):
    cfg = default_config.copy()
    cfg['name'] = args[1]
    if len(args) > 2:
        for i in args[2:]:
            if i.lower().startswith('+') and '=' in i:
                cfg['opts'].append(i.lower()[1:].split('=', 1))
            elif i.lower() in MODELS.keys():
                cfg['models'].append(i.lower())
            else:
                print "No model named '%s'!" % i.lower()
    cfg['opts'] = dict(cfg['opts'])
    s = 's' if len(cfg['models']) == 1 else ''
    if raw_input("Ready to create app '%s' with %s model%s! (y/N)  " % (cfg['name'], len(cfg['models']), s)).lower() != 'y':
        print "App creation aborted!"
        return sys.exit()
    print '\nCreating your app!'

    # App Directory
    if os.path.exists(cfg['name']):
        print 'ABORTED: Directory "%s" exists!' % cfg['name']
        return sys.exit()
    os.mkdir(cfg['name'])
    os.chdir(cfg['name'])
    print "  Created app directory!"

    # Subdirs
    for d in ['templates', 'static']:
        os.mkdir(d)
    print "  Created app sub-directories!"

    # Models
    for item in cfg['models']:
        cfg = MODELS[item].run(cfg)
        print "  Ran model %s!" % item

    # Base app
    MODELS['base'].run(cfg)
    print "  Created the main script!"

    print "Your app is ready! Enjoy its flasky goodness!"

def dumpApp(args): pass

if __name__ == '__main__':
    loadModels()
    if len(sys.argv) == 1:
        print MAN
        print '\nMODELS HELP:'
        for name, mod in MODELS.items():
            if not len(mod.MAN): continue
            print name.upper()
            for lin in mod.MAN.split('\n'):
                print '  '+lin
    else:
        if sys.argv[1].lower() == 'new':
            newApp(sys.argv[1:])
        elif sys.argv[1].lower() == 'dump':
            dumpApp(sys.argv[1:])
        else:
            print "Unknown command %s!\n\n\n" % sys.argv[1]
            print MAN
