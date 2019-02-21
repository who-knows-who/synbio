import os
from xml.dom.minidom import parse as parse


class Part:
    def __init__(self, name, type, sequence):
        self.name = name
        self.type = type
        self.sequence = sequence

        self.a = sequence.count('a')
        self.t = sequence.count('t')
        self.g = sequence.count('g')
        self.c = sequence.count('c')

    def print(self):
        print(self.name, self.type, self.a, self.t, self.g, self.c, sep=' ')

    def dzn_str(self):
        return self.name + ', ' + str(self.a) + ', ' + str(self.t) + ', ' + str(self.g) + ', ' + str(self.c)


def get_data(xml_tree):
    name = xml_tree.getElementsByTagName("part_name")[0].childNodes[0].data
    type = xml_tree.getElementsByTagName("part_type")[0].childNodes[0].data
    sequence = xml_tree.getElementsByTagName("seq_data")[0].childNodes[0].data
    parts.append(Part(name, type, sequence))


def create_dzn():
    parts_str = "PARTS = { "
    table_str = "table = ["
    reg_str = "group_regulatory = { "
    rbs_str = "group_rbs = { "
    cod_str = "group_coding = { "
    term_str = "group_terminator = { "

    for part in parts:
        parts_str = parts_str + part.name + ', '
        table_str = table_str + '| ' + part.dzn_str() + '\n\t\t '

        if part.type == 'Regulatory':
            reg_str = reg_str + part.name + ', '
        elif part.type == 'RBS':
            rbs_str = rbs_str + part.name + ', '
        elif part.type == 'Coding':
            cod_str = cod_str + part.name + ', '
        elif part.type == 'Terminator':
            term_str = term_str + part.name + ', '

    parts_str = parts_str[:-2] + ' };'
    table_str = table_str[:-4] + ' |];'
    reg_str = reg_str[:-2] + ' };'
    rbs_str = rbs_str[:-2] + ' };'
    cod_str = cod_str[:-2] + ' };'
    term_str = term_str[:-2] + ' }'

    with open('data.dzn', 'w') as file:
        file.write(parts_str + '\n\n')
        file.write('% part name, #a, #t, #g, #c\n')
        file.write(table_str + '\n\n')
        file.write(reg_str + '\n')
        file.write(rbs_str + '\n')
        file.write(cod_str + '\n')
        file.write(term_str)


if __name__ == "__main__":
    parts = []
    for filename in os.listdir('parts'):
        get_data(parse('parts/' + filename))
    create_dzn()
