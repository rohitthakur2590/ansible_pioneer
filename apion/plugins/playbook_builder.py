from collections import OrderedDict


class PlaybookBuilder(object):
    def __init__(self, content):
        self.content = content


    def rmbp(self):
        roles = []
        print(self.content)

        roles.append('ansible_network.cli_rm_builder.run')
        vars = OrderedDict(
            {
                "rm_dest": self.content['rm_dest'],
                "collection_org": self.content['collection_org'],
                "collection_name": self.content['collection_name'],
                "resource": self.content['resource'],
                "docstring": self.content['docstring']
            }
        )
        # build tasks
        playbook = [
            OrderedDict(
                {"hosts": "localhost", "gather_facts": 'yes', "roles": roles, "vars": vars}
            )
        ]
        import q
        q("Playbook -----", playbook)
        return playbook

    def pbp(self):
        roles = []
        print(self.content)


        roles.append('ansible.plugin_builder.run')
        plugins_lst = []
        plugins = OrderedDict(
            {
                "type": self.content['plugin_type'],
                "name": self.content['plugin_name'],
                "docstring": self.content['docstring'],

            }
        )
        collection_vars =OrderedDict(
            {
                    "path": self.content['dest_path'],
                    "namespace": self.content['name_space'],
                    "name": self.content['collection_name'],
            }
        )
        plugins_lst.append(plugins)
        # vars = OrderedDict({
        #     "collection": collection_vars,
        #     "plugins": plugins_lst
        # }

        # )
        vars = OrderedDict(
            {
                "manifest_file": "/home/rothakur/.ansible/collections/ansible_collections/ansible/plugin_builder/MANIFEST.yaml"
            }
        )


        # build tasks
        playbook = [
            OrderedDict(
                {"hosts": "localhost", "gather_facts": 'yes', "roles": roles, "vars": vars}
            )
        ]
        import q
        q("Playbook -----", playbook)
        return playbook

    def generate(self, playbook_name):
        playbook = getattr(self, playbook_name)()
        return playbook