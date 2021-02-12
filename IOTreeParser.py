import xml.etree.ElementTree as ET


def xml_to_json(etree):
    element = dict()
    element['attrib'] = etree.attrib
    element['text'] = etree.text
    if len(list(etree)) == 1:
        element[list(etree)[0].tag] = xml_to_json(list(etree)[0])
    elif len(list(etree)) > 1:
        for child in etree:
            if child.tag in element.keys():
                if type(element[child.tag]) != list:
                    element[child.tag] = [element[child.tag]]
                element[child.tag].append(xml_to_json(child))
            else:
                element[child.tag] = xml_to_json(child)
    return element


devices_to_skip = ['1734-IB4/C', '1734-IB8/C', '1734-IE8C/C', '1734-OB8E/C', '1734-OW4/C', '1734sc-IF4U/A',
                   '1756-HSC/A', '1756-IA16', '1756-IA32/A', '1756-IB16', '1756-IB16I', '1756-IB32/B',
                   '1756-IF16', '1756-IF6I', '1756-IF8', '1756-IF8I/A', '1756-IT6I', '1756-MODULE', '1756-OA16',
                   '1756-OB16D', '1756-OB16I', '1756-OF4', '1756-OF6CI', '1756-OF8', '1756-OW16I', '1756-OX8I',
                   '1769-IF4I/A', '1769-IQ32/A', '1769-OW16/A', '1794-IA16/A', '1794-IB16/A',
                   '1794-IE4XOE2/B', '1794-IF4I/A', '1794-OA16/A', '1794-OB8/A', '1734-OE4C/C', '1794-OE4/B',
                   '1734-OB8/C', '1756-OB16E', 'DPI-DRIVE-PERIPHERAL-MODULE', 'RHINOBP-DRIVE-PERIPHERAL-MODULE',
                   '1794-OB16P/A', '1794-OW8/A', '1794-OE4/B', '1794-IE8XOE4/A', '1794-OB16P/A', '1794-OB16P/A',
                   '1794-IE8XOE4/A', '1794-IE8XOE4/A', '1794-IE8XOE4/A', '1794-VHSC/A']


def list_devices(node):
    return_dict = {node.name: {}}
    if node.parent is not None:
        return_dict[node.name]['parent'] = node.parent.name
    for attr, val in node.__dict__.items():
        if attr not in ['_NodeMixin__children', '_NodeMixin__parent', 'name']:
            return_dict[node.name][attr] = val
    return_dict[node.name]['children'] = list()
    for child in node.children:
        if child.device not in devices_to_skip:
            return_dict[node.name]['children'].append(list_devices(child))
        else:
            return_dict[node.name]['children'].append(child.name)
    return return_dict


# def asdf(temp):
#     if type(temp) == dict:
#         for k, v in temp.items():
#             try:
#                 print(str(v['plc']) + ',' + str(v['parent']) + ',' + str(k) + ',' + str(v['device']) + ',' + str(v['address']) + ',' + str(v['new_ip']) + ',' + str(v['comments']))
#             except:
#                 import traceback
#                 print(traceback.format_exc())
#             for child in v['children']:
#                 asdf(child)


if __name__ == '__main__':
    import yamlarg, os, anytree
    #args = yamlarg.parse('arguments.yaml')

    args = {'l5x-dir': './input'}
    outputs = dict()
    for plc_l5x in os.scandir(args['l5x-dir']):
        if plc_l5x.name.endswith(".L5X"):
            with open(plc_l5x, 'r') as f:
                element_tree = ET.fromstring(f.read())
            plc = xml_to_json(element_tree)
            #tree = list()
            a_tree = list()
            first = True
            for module in plc['Controller']['Modules']['Module']:
                if first:
                   a_tree.append(anytree.Node(module['attrib']['Name']))
                   first = False
                else:
                    if 'Name' in module['attrib'].keys():
                        a_tree.append(anytree.Node(module['attrib']['Name'], parent=
                        anytree.findall(a_tree[0], lambda node: node.name == module['attrib']['ParentModule'])[0]))
                    else:
                        a_tree.append(anytree.Node(module['attrib']['CatalogNumber'], parent=
                        anytree.findall(a_tree[0], lambda node: node.name == module['attrib']['ParentModule'])[0]))
                a_tree[-1].plc = plc_l5x.name
                if 'CatalogNumber' in module['attrib'].keys():
                    a_tree[-1].device = module['attrib']['CatalogNumber']
                else:
                    a_tree[-1].device = None
                if 'Description' in module['attrib'].keys():
                    a_tree[-1].text = module['attrib']['Description']['text']
                    print(module['attrib']['Name'], a_tree[-1].text)
                try:
                    a_tree[-1].address = module['Ports']['Port']['attrib']['Address']
                except TypeError:
                    try:
                        a_tree[-1].address = module['Ports']['Port'][1]['attrib']['Address']
                    except KeyError:
                        a_tree[-1].address = None
                a_tree[-1].new_ip = None
                a_tree[-1].checked = None
                a_tree[-1].comments = None
            import yaml
            print(yaml.dump([list_devices(a_tree[0])], sort_keys=False))

