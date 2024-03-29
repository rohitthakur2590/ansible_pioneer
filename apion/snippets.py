#
# Some list of snippets, one for each of get, get-config & edit-config
#
snippets = {}
snippets['get'] = [
    '''<netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  <schemas/>
</netconf-state>''',
    '''<interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>''',
    '''<routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>''',
    '''<bgp-state xmlns="urn:cisco:params:xml:ns:yang:cisco-bgp-state"/>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios"/>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip/>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip><access-list/></ip>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <ip><route/></ip>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <router>
    <bgp/>
  </router>
</native>''',
    '''<native xmlns="http://cisco.com/ns/yang/ned/ios">
  <router>
    <ospf/>
  </router>
</native>''',
]

snippets['rmb'] = [
  '''---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run

  vars:
    resource: firewall_zones
    rm_dest: ~/ansible-collections/collections/ansible_collections/vyos/vyos
    docstring: ~/ansible_playbooks/collections/network/vyos/vyos/firewall_zones/docstring.yaml
    collection_org: vyos
    collection_name: vyos''',
  '''---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible_network.cli_rm_builder.run

  vars:
    resource: firewall_zones
    rm_dest: ~/ansible-collections/collections/ansible_collections/vyos/vyos
    collection_org: vyos
    collection_name: vyos''',

]


snippets['get_config'] = [
    '''<interfaces/>''',
'''<native><interface/></native>'''
]


snippets['edit_config'] = [
    '''<config>
      <netconf-yang xmlns="http://cisco.com/yang/cisco-self-mgmt">
        <cisco-ia xmlns="http://cisco.com/yang/cisco-ia">
          <snmp-trap-control>
            <trap-list>
              <trap-oid>1.3.6.1.4.1.9.9.41.2.0.1</trap-oid>
            </trap-list>
            <trap-list>
              <trap-oid>1.3.6.1.6.3.1.1.5.3</trap-oid>
            </trap-list>
            <trap-list>
              <trap-oid>1.3.6.1.6.3.1.1.5.4</trap-oid>
            </trap-list>
          </snmp-trap-control>
        </cisco-ia>
      </netconf-yang>
</config>'''
]
