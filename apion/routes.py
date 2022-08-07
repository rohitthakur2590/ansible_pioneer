from flask import Markup, render_template, redirect, url_for, request, Response, escape, flash
from apion import app, db, bcrypt
from apion import snippets
from apion.utils.utils import write_to_yamlfile, write_generate_playbook, default_yml, format_network_triage,\
    op, write_manifest_file, get_shell_script_output_using_communicate
from shelljob import proc
from apion.forms import RegistrationForm, LoginForm, PluginBuilderForm
from apion.models import User
from flask_login import login_user, current_user, logout_user
from apion.plugins.playbook_builder import PlaybookBuilder
from apion.plugins.inventory_builder import InventoryBuilder
from apion.plugins.playbook_runner import PlaybookRunner
from apion.plugins.event_filter import EventFilter
import queue
from datetime import date


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/ansible_builder')
def ansible_builder():
    return render_template('builder.html')


@app.route('/rmb', methods=['GET', 'POST'])
async def rmb():
    eventq = queue.Queue()
    kw = {
        "snippets": snippets.snippets,
    }
    import q
    q(kw["snippets"])
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
            print(kw['docstring'])
            apb = PlaybookBuilder(content=kw)
            playbook = apb.rmbp()

            aib = InventoryBuilder('localhost', 'rothakur', 'redcosmos', 'local')
            inventory = aib.generate()

            pbr = PlaybookRunner(inventory=inventory, playbook=playbook)
            events = await pbr.run(eventq)
            print(events)
            res = EventFilter(events=events, playbook_name="rmbp").filter()
            # return render_template('rmb_code_generator.html', res=res, **kw)
            return Response(res, mimetype='text/event-stream')

    else:
        kw['xml'] = default_yml
        kw[op['get']] = 'checked'

    return render_template('rmb_code_generator.html', **kw)



@app.route('/plugin_builder', methods=['GET', 'POST'])
async def plugin_builder():
    import q
    eventq = queue.Queue()
    kw = {
        "snippets": snippets.snippets,
    }
    if request.method == 'POST':

        for k, v in request.form.items():
            kw[k] = v

        q(kw)

        if kw['submit'] == 'reset':
            kw = {
                "snippets": snippets.snippets,
            }
            return render_template('plugin_generator.html', **kw)

        elif kw['submit'] == 'generate':
            eventq = queue.Queue()


            if True:
                q("Content", kw)
                write_manifest_file(kw)

                apb = PlaybookBuilder(content=kw)

                playbook = apb.pbp()

                aib = InventoryBuilder('localhost', 'rothakur', 'redcosmos', 'local')

                inventory = aib.generate()

                pbr = PlaybookRunner(inventory=inventory, playbook=playbook)

                events = await pbr.run(eventq)

                print(events)

                kw['res'] = EventFilter(events=events, playbook_name="rmbp").filter()

                return render_template('plugin_generator.html', **kw)

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
            p = g.run(['ansible-playbook', '../../ansible_network/sample.yaml'])

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


@app.route('/validated_content')
def validated_content():
    return render_template('validated_content.html')


@app.route('/network_bgp', methods=['GET', 'POST'])
async def network_bgp():
    eventq = queue.Queue()
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
            return render_template('network_bgp.html', **kw)

        elif kw['submit'] == 'generate':
            print(kw['docstring'])
            apb = PlaybookBuilder(content=kw)
            playbook = apb.rmbp()

            aib = InventoryBuilder('localhost', 'rothakur', 'redcosmos', 'local')
            inventory = aib.generate()

            pbr = PlaybookRunner(inventory=inventory, playbook=playbook)
            events = await pbr.run(eventq)
            print(events)
            res = EventFilter(events=events, playbook_name="rmbp").filter()
            # return render_template('rmb_code_generator.html', res=res, **kw)
            return Response(res, mimetype='text/event-stream')

    else:
        kw['xml'] = default_yml
        kw[op['get']] = 'checked'

    return render_template('network_bgp.html', **kw)


@app.route('/testing')
def testing():
    return render_template('testing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created Successfully','success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/triager", methods=['GET', 'POST'])
def triager():
    output = get_shell_script_output_using_communicate()
    today = date.today()
    data = format_network_triage(output)
    return render_template('triager.html', data=data, date=today)
