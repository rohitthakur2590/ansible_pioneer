from collections import OrderedDict

plugins = []
plugin = OrderedDict(
            {
                "type": 'action',
                "name": 'health_check',
                "docstring": "/home/rothakur/plugin.yaml"
            }
        )
plugins.append(plugin)
collection_vars =OrderedDict(
            {
                    "path": '/home/rothakur',
                    "namespace": 'cisco.iosxr',
                    "name": 'iosxr',
            }
        )
coll = OrderedDict(
    {
        'collection': collection_vars,
        'plugins': plugins
    }
)

import pyYaml
from collections import OrderedDict

def dump_ordered_yaml(ordered_data, output_filename, Dumper=yaml.Dumper):
    class OrderedDumper(Dumper):
        pass

    class UnsortableList(list):
        def sort(self, *args, **kwargs):
            pass

    class UnsortableOrderedDict(OrderedDict):
        def items(self, *args, **kwargs):
            return UnsortableList(OrderedDict.items(self, *args, **kwargs))

    OrderedDumper.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
    with open(output_filename, "w") as f:
        yaml.dump(ordered_data, f, Dumper=OrderedDumper)

dump_ordered_yaml(coll, "./ordered.yaml")
