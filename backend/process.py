import os
from xml.dom.minidom import parse as parse

solver_dir = '../solver/'


class Part:
    def __init__(self, name, type, sequence):
        self.name = name
        self.type = type
        self.sequence = sequence.replace("\n","")

        self.a = sequence.count('a')
        self.t = sequence.count('t')
        self.g = sequence.count('g')
        self.c = sequence.count('c')

    def print(self):
        print(self.name, self.type, self.a, self.t, self.g, self.c, sep=' ')

    def dzn_str(self, sub_length):
        return self.name + ',' + str(self.a) + ',' + str(self.t) + ',' \
               + str(self.g) + ',' + str(self.c) + ',' + self.start_end_str(sub_length)

    def start_end_str(self, sub_length):
        ret_str = ""
        seq_len = len(self.sequence)
        for i in range(0, sub_length):
            if i >= seq_len:
                ret_str = ret_str + str(base_to_int('n')) + ','
            else:
                ret_str = ret_str + str(base_to_int(self.sequence[i])) + ','

        for i in range(seq_len - sub_length, seq_len):
            if i < 0:
                ret_str = ret_str + str(base_to_int('n')) + ','
            else:
                ret_str = ret_str + str(base_to_int(self.sequence[i])) + ','
        return ret_str[0:-1]

    def prepend_type(self):
        if self.type == 'Regulatory':
            # promotor
            self.name = 'p' + self.name
        elif self.type == 'RBS':
            self.name = 'r' + self.name
        elif self.type == 'Coding':
            self.name = 'c' + self.name
        elif self.type == 'Terminator':
            self.name = 't' + self.name


def get_data(xml_tree):
    name = xml_tree.getElementsByTagName("part_name")[0].childNodes[0].data
    type = xml_tree.getElementsByTagName("part_type")[0].childNodes[0].data
    sequence = xml_tree.getElementsByTagName("seq_data")[0].childNodes[0].data
    parts.append(Part(name, type, sequence))


def str_to_chars(input_str):
    ret_str = ""
    for c in input_str:
        ret_str = ret_str + str(base_to_int(c)) + ','
    return ret_str[0:-1]


def base_to_int(base):

    if base == "a":
        return -1
    elif base == "t":
        return 1
    elif base == "g":
        return -2
    elif base == "c":
        return 2
    elif base == "n":
        return 0
    else:
        print("Error: base" + base)


def create_dzn():

    for p in parts:
        p.prepend_type()

    restriction_sites = ["atgc", "gcc"]
    max_restrict = 0
    restrict_str = ""
    i = 1
    for site in restriction_sites:
        max_restrict = max(max_restrict, len(site))
        restrict_str = restrict_str + "array[int] of bases: site_" + str(i) + " = " \
                       + str_to_chars(site) + ";\n"
        i = i+1

    enum_first_str = ""
    enum_last_str = ""
    for i in range(1, max_restrict):
        enum_first_str = enum_first_str + ", f" + str(i)
        enum_last_str = enum_last_str + ", l" + str(i)

    enum_first_str = enum_first_str + ", fend"
    enum_last_str = enum_last_str + ", lend };"
    enum_str = "enum FEATURE = {name, a, t, g, c" + enum_first_str + enum_last_str

    parts_str = "enum PARTS = { NULL, "
    table_str = "data = [| NULL, 0, 0, 0, 0" + ", 0" * 2 * max_restrict + "\n\t\t "
    reg_str = "group_regulatory = { "
    rbs_str = "group_rbs = { "
    cod_str = "group_coding = { "
    term_str = "group_terminator = { "
    null_str = "null = { NULL };"

    for part in parts:
        parts_str = parts_str + part.name + ', '
        table_str = table_str + '| ' + part.dzn_str(max_restrict) + '\n\t\t '

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
    term_str = term_str[:-2] + ' };'

    if os.path.exists(solver_dir + 'data.dzn'):
        os.rename(solver_dir + 'data.dzn', solver_dir + 'old_data.dzn')

    with open(solver_dir + 'data.dzn', 'w') as file:
        file.write('int: max_parts = 10;' + '\n')
        file.write('int: substring_length = ' + str(max_restrict) + ";\n")
        file.write('set of int: combined_index = 1..2*substring_length;\n\n')
        file.write(restrict_str + '\n')
        file.write(parts_str + '\n')
        file.write(enum_str + '\n\n')
        file.write('% part name, #a, #t, #g, #c, f1, ..., fend, l1, ..., lend\n')
        file.write(table_str + '\n\n')
        file.write(reg_str + '\n')
        file.write(rbs_str + '\n')
        file.write(cod_str + '\n')
        file.write(term_str + '\n')
        file.write(null_str)


if __name__ == "__main__":
    parts = []
    for filename in os.listdir('parts'):
        get_data(parse('parts/' + filename))
    create_dzn()
