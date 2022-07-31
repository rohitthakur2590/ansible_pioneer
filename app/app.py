from flask import Flask, Markup, render_template, redirect, url_for, request, Response, escape
import snippets
from ansible_pioneer.utils.utils import write_to_yamlfile, write_generate_playbook, default_yml, op
from shelljob import proc


# create the application object
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ansible_builder')
def ansible_builder():
    return render_template('builder.html')


@app.route('/rmb', methods=['GET', 'POST'])
def rmb():
    kw = {
        "snippets": snippets.snippets,
    }

    if request.method == 'POST':

        for k, v in request.form.items():
            print(k, v)
            kw[k] = v

        if kw['submit'] == 'reset':
            kw = {
                "snippets": snippets.snippets,
            }
            return render_template('rmb_code_generator.html', **kw)

        elif kw['submit'] == 'generate':

            if 'junos' in kw['collection_org']:
                yaml_playbook = str(kw['xml'])
                print(yaml_playbook)
                write_to_yamlfile(yaml_playbook)
            else:

                write_generate_playbook(**kw)

                # import time
                # # time.sleep(2.4)

            g = proc.Group()
            p = g.run(['ansible-playbook', '../../../ansible_network/sample.yaml'])

            def read_process():
                while g.is_pending():
                    lines = g.readlines()
                    for proc, line in lines:
                        yield line

            return Response(read_process(), mimetype='text/plain')
    else:
        kw['xml'] = default_yml
        kw[op['get']] = 'checked'

    return render_template('rmb_code_generator.html', **kw)


@app.route('/plugin_builder', methods=['GET', 'POST'])
def plugin_builder():
    kw = {
        "snippets": snippets.snippets,
    }

    if request.method == 'POST':

        for k, v in request.form.items():
            print(k, v)
            kw[k] = v

        if kw['submit'] == 'reset':
            kw = {
                "snippets": snippets.snippets,
            }
            return render_template('plugin_generator.html', **kw)

        elif kw['submit'] == 'generate':

            if 'vyos' in kw['collection_org']:
                write_generate_playbook(**kw)

            else:

                yaml_playbook = str(kw['xml'])
                print(yaml_playbook)
                write_to_yamlfile(yaml_playbook)

                import time
                time.sleep(2.4)

            g = proc.Group()
            p = g.run(['ansible-playbook', '../../../ansible_network/sample.yaml'])

            def read_process():
                while g.is_pending():
                    lines = g.readlines()
                    for proc, line in lines:
                        yield line

            return Response(read_process(), mimetype='text/plain')
    else:
        kw['xml'] = default_yml
        kw[op['get']] = 'checked'

    return render_template('plugin_generator.html', **kw)


@app.route('/smb', methods=['GET', 'POST'])
def smb():
    kw = {
        "snippets": snippets.snippets,
    }

    if request.method == 'POST':

        for k, v in request.form.items():
            print(k, v)
            kw[k] = v

        if kw['submit'] == 'reset':
            kw = {
                "snippets": snippets.snippets,
            }
            return render_template('smb_generator.html', **kw)

        elif kw['submit'] == 'generate':

            if 'vyos' in kw['collection_org']:
                write_generate_playbook(**kw)

            else:

                yaml_playbook = str(kw['xml'])
                print(yaml_playbook)
                write_to_yamlfile(yaml_playbook)

                import time
                time.sleep(2.4)

            g = proc.Group()
            p = g.run(['ansible-playbook', '../../../ansible_network/sample.yaml'])

            def read_process():
                while g.is_pending():
                    lines = g.readlines()
                    for proc, line in lines:
                        yield line

            return Response(read_process(), mimetype='text/plain')
    else:
        kw['xml'] = default_yml
        kw[op['get']] = 'checked'

    return render_template('smb_generator.html', **kw)

if __name__ == '__main__':
    # start the server with the 'run()' method
    app.run(host="0.0.0.0", port=8000)

