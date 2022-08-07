from subprocess import Popen, PIPE
from subprocess import check_output

default_xml = '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>'''

default_yml = '''---
- hosts: <hosts>
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run

  vars:
    resource: <resource>
    rm_dest: <destination path>
    docstring: <docstring>
    collection_org: <collection org>
    collection_name: <collection name>
'''
op = {'get' : 'OPER_GET',
      'get_config' : 'OPER_GETCONFIG',
      'edit_config' : 'OPER_EDITCONFIG'}


def validate_form():
    pass


def write_to_yamlfile(playbook):
    """

    :param playbook:
    :return:
    """
    text_file = open("/home/rothakur/ansible-collections/collections/ansible_collections/ansible_network/sample.yaml", "w")
    n = text_file.write(playbook)


def write_manifest_file(kw):
    playbook = '''---
    collection:
      path: ''' + kw['dest_path'] + '''
      namespace: ''' + kw['name_space'] + '''
      name: ''' + kw['collection_name'] + '''
    plugins:
      - type: ''' + kw['plugin_type'] + '''
        name: ''' + kw['plugin_name'] + '''
        docstring: ''' + kw['docstring']

    text_file = open("/home/rothakur/.ansible/collections/ansible_collections/ansible/plugin_builder/MANIFEST.yaml", "w")
    n = text_file.write(playbook)


def write_generate_playbook(**kw):
    """

    :param kw:
    :return:
    """
    if kw['docstring'] != '':
            playbook = '''
---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run
  vars:
    resource: ''' + kw['resource'] + '''
    rm_dest: ''' + kw['rm_dest'] + '''
    docstring: ''' + kw['docstring'] + '''
    collection_org: ''' + kw['collection_org'] + '''
    collection_name: ''' + kw['collection_name']
    else:
        playbook = '''
---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run
  vars:
    resource: ''' + kw['resource'] + '''
    rm_dest: ''' + kw['rm_dest'] + '''
    collection_org: ''' + kw['collection_org'] + '''
    collection_name: ''' + kw['collection_name']


    text_file = open("/home/rothakur/ansible-collections/collections/ansible_collections/ansible_network/sample.yaml", "w")
    n = text_file.write(playbook)


def format_network_triage(data):
    """

    :param data:
    :return:
    """
    data = data.splitlines()
    triag_facts = []
    for line in data:
        temp = line.split(' |')
        dict1 = {}
        if len(temp) >= 3:
            temp[0] = temp[0].replace('| ', '  ')
            dict1["col1"] = temp[0]
            dict1["col2"] = temp[1]
            dict1["col3"] = temp[2]
            dict1["col4"] = temp[3]

            triag_facts.append(dict1)
    triag_facts.remove(triag_facts[0])
    return triag_facts


def get_shell_script_output_using_communicate():
    session = Popen(['/home/rothakur/triager.sh'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception("Error "+str(stderr))
    return stdout.decode('utf-8')


def get_shell_script_output_using_check_output():
    stdout = check_output(['/home/rothakur/triager.sh']).decode('utf-8')
    return stdout
