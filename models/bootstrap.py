import os, requests

MAN = """Bootstrap allows you to easily setup a base directory structure that includes
css/js/img for bootstrap development. You can choose between downloading bootstrap content
and using the bootstrap cdn. It requires requests to be installed to download content.
  bscdn = (1/0): If set too 1, we will setup a base template using the bootstrap cdn
"""

SCRIPTS = {
    os.path.join('static', 'css', 'bootstrap.css'): "http://twitter.github.com/bootstrap/assets/css/bootstrap.css",
    os.path.join('static', 'css', 'bootstrap-responsive.css'): "http://twitter.github.com/bootstrap/assets/css/bootstrap-responsive.css",
    os.path.join('static', 'js', 'jquery.js'): "http://twitter.github.com/bootstrap/assets/js/jquery.js",
    os.path.join('static', 'js', 'bootstrap.js'): "http://twitter.github.com/bootstrap/assets/js/bootstrap.js",
    os.path.join('static', 'img', 'glyphicons-halflings.png'): "http://twitter.github.com/bootstrap/assets/img/glyphicons-halflings.png",
    os.path.join('static', 'img', 'glyphicons-halflings.png-white'): "http://twitter.github.com/bootstrap/assets/img/glyphicons-halflings-white.png"
}

TITLE = "Base Template"
ADD_STYLE = """body {
        padding-top: 60px;
        padding-bottom: 40px;
      }"""

URL_PATHS = {
    False: {
        'js': '/static/js/',
        'css': '/static/css/'
    },
    True: {
        'js': "//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js//",
        'css': "//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/css/"
    }
}

USE_CDN = False

TEMPLATE = '\n'.join(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bootstrap_template.html'), 'r').readlines())

def download():
    p("Adding static-content directories")
    os.mkdir(os.path.join('static', 'css'))
    os.mkdir(os.path.join('static', 'js'))
    os.mkdir(os.path.join('static', 'font'))
    os.mkdir(os.path.join('static', 'img'))
    p("Downloading bootstrap components")
    max_len = max([len(i) for i in SCRIPTS.values()])
    for key, val in SCRIPTS.items():
        with open(key, 'w') as f:
            p("  DOWNLOADING %s%s" % (val, ' '*(max_len-len(val))), True)
            r = requests.get(val)
            if r.status_code == 200:
                f.write(r.content)
            else:
                p(" FAILED" % val)
        p(" DONE")


def p(c, v=False):
    if v: print "    "+str(c),
    else: print "    "+str(c)

def run(cfg):
    global USE_CDN, TITLE
    if 'bscdn' in cfg['opts'].keys():
        if int(cfg['opts']['bscdn']):
            USE_CDN = True

    if USE_CDN:
        p("Using bootstrap-cdn, not downloading anything!")
    else:
        download()

    if 'title' in cfg['opts'].keys():
        TITLE = cfg['opts']['title']

    pas = {}
    pas['CSS_PATH'] = URL_PATHS[USE_CDN]['css']
    pas['JS_PATH'] = URL_PATHS[USE_CDN]['js']
    pas['TITLE'] = TITLE
    pas['ADD_STYLE'] = ADD_STYLE

    with open(os.path.join('templates', 'index.html'), 'w') as f:
        f.write(TEMPLATE.format(**pas))

    cfg['opts']['ROOT_RESULT'] = "return render_template('index.html')"
    return cfg
