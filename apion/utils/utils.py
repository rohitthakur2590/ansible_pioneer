
default_xml = '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>'''

default_yml = '''---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run

  vars:
    resource: firewall_zones
    rm_dest: ~/ansible-collections/collections/ansible_collections/vyos/vyos
    docstring: ~/ansible_playbooks/collections/network/vyos/vyos/firewall_zones/docstring.yaml
    collection_org: vyos
    collection_name: vyos
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
      namespace: ''' + kw['namespace'] + '''
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