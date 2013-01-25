MAN = """"""

base_config = {
    'FLASK_IMPORTS': ['Flask', 'render_template'],
    'OTHER_IMPORTS': ['os', 'sys', 'time'],
    'SECRET_KEY': "change_me",
    'APP_VAR_NAME': "app",
    'ROOT_RESULT': "return \"It Works\""
}

SCRIPT_CONTENTS = """
from flask import {FLASK_IMPORTS}
import {OTHER_IMPORTS}

{APP_VAR_NAME} = Flask(__name__)
app.secret_key = "{SECRET_KEY}"

@app.route('/')
def routeRoot():
    {ROOT_RESULT}

if __name__ == '__main__':
    app.run(debug=True)

"""


def run(cfg):
    for key, var in cfg['opts'].items():
        if key.upper() in ['SECRET_KEY', 'APP_VAR_NAME', "ROOT_RESULT"]:
            base_config[key.upper()] = var

    base_config['FLASK_IMPORTS'] = ', '.join(base_config['FLASK_IMPORTS'])
    base_config['OTHER_IMPORTS'] = ', '.join(base_config['OTHER_IMPORTS'])

    with open('app.py', 'w') as f:
        f.write(SCRIPT_CONTENTS.format(**base_config))
