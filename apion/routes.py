from flask import Markup, render_template, redirect, url_for, request, Response, escape, flash
from apion import app, db, bcrypt
from apion import snippets
from apion.utils.utils import write_to_yamlfile, write_generate_playbook, default_yml, op
from shelljob import proc
from apion.forms import RegistrationForm, LoginForm
from apion.models import User
from flask_login import login_user, current_user, logout_user


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
