import os
from xml.dom.minidom import parse as parse

solver_dir = 'solver/'


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


class Restriction:
    def __init__(self, sequence_str, site_num):
        self.sequence = sequence_str
        self.site_num = site_num

    def site_str(self):
        ret_str = "array[int] of -2..2: site_" + str(self.site_num) + " = [" \
                    + str_to_chars(self.sequence) + "];\n"
        return ret_str

    def constraint_str(self):
        ret_str = "constraint\n" \
                         "  forall(i in POSITION where i!= max(POSITION))\n" \
                         "      (not contains_restriction_site(\n" \
                         "          sequence[i, l1..lend],\n" \
                         "          sequence[i+1, f1..fend],\n" \
                         "          site_" + str(self.site_num) + "));\n\n"
        return ret_str


def get_data(xml_tree):
    name = xml_tree.getElementsByTagName("part_name")[0].childNodes[0].data
    type = xml_tree.getElementsByTagName("part_type")[0].childNodes[0].data
    sequence = xml_tree.getElementsByTagName("seq_data")[0].childNodes[0].data.replace("\n", "")
    allowed = True
    for site in sites:
        if site.sequence in sequence:
            allowed = False
    if allowed:
        parts.append(Part(name, type, sequence))


def get_restriction_sites():
    finished = False
    num = 0
    while not finished:
        site = input("Enter a restriction site or 'f' to finish:\n").lower()
        if site == 'f':
            finished = True
        else:
            valid = True
            for c in site:
                if c not in ('a', 't', 'g', 'c'):
                    print('Invalid: ' + c + '. Please only use a, t, g, c.')
                    valid = False
            if valid:
                num = num + 1
                sites.append(Restriction(site, num))
    return num


def get_selected_parts():
    num = 0
    finished = False
    parts_list = ""
    available_parts = []
    for part in parts:
        parts_list = parts_list + part.name + " : " + part.type + "\n"
        available_parts.append(part.name)
    while not finished:
        part = input("Enter a part name, 'f' to finish, 'list' to list:\n")
        if part == 'f':
            finished = True
        elif part == 'list':
            print(parts_list)
        else:
            if part in available_parts:
                selected.append(part)
                num = num + 1
            else:
                print("That doesn't seem to be an available part.")
    return num


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


def create_data_dzn():

    max_restrict = 0

    if site_count > 0:

        feature_first_str = ""
        feature_last_str = ""

        for site in sites:
            max_restrict = max(max_restrict, len(site.sequence))

        for i in range(1, max_restrict):
            feature_first_str = feature_first_str + ", f" + str(i)
            feature_last_str = feature_last_str + ", l" + str(i)

        feature_first_str = feature_first_str + ", fend"
        feature_last_str = feature_last_str + ", lend"

        feature_str = "FEATURE = {name, a, t, g, c %s %s };" % (feature_first_str, feature_last_str)
    else:

        feature_str = "FEATURE = {name, a, t, g, c };"

    parts_str = "PARTS = { NULL, "
    table_str = "data = [| NULL, 0, 0, 0, 0" + (", 0" * 2 * max_restrict) + "\n\t\t "
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
        file.write('max_parts = %d;\n' % max_parts)
        file.write('substring_length = %s;\n\n' % (str(max_restrict)))
        file.write(parts_str + '\n')
        file.write(feature_str + '\n\n')
        file.write('% part name, #a, #t, #g, #c, f1, ..., fend, l1, ..., lend\n')
        file.write('% a = -1, t = 1, g = -2, c = 2  MiniZinc likes numbers\n')
        file.write(table_str + '\n\n')
        file.write(reg_str + '\n')
        file.write(rbs_str + '\n')
        file.write(cod_str + '\n')
        file.write(term_str + '\n')
        file.write("% MiniZinc doesn't like variable length array - null used to pad\n")
        file.write(null_str)


def create_restriction_mzn():

    if site_count > 0:

        array_str = ""
        constraint_str = ""

        for site in sites:
            array_str = array_str + site.site_str()
            constraint_str = constraint_str + site.constraint_str()

        with open(solver_dir + 'synbio_restriction.mzn', 'w') as file:
            file.write(array_str + '\n')
            file.write(constraint_str)
    else:
        with open(solver_dir + 'synbio_restriction.mzn', 'w') as file:
            file.write("")

def create_selected_mzn():

    if selected_count > 0:
        selected_str = "set of PARTS: group_selected = { "

        for part in selected:
            selected_str = selected_str + part + ', '
        selected_str = selected_str[:-2] + ' };\n'

        constraint_str = "% All parts in group_selected in sequence \n" \
                         "constraint\n" \
                         "  forall(p in group_selected)\n" \
                         "      (exists(i in POSITION)(sequence[i,name] == p));\n"

        with open(solver_dir + 'synbio_selected.mzn', 'w') as file:
            file.write(selected_str + '\n')
            file.write(constraint_str)
    else:
        with open(solver_dir + 'synbio_selected.mzn', 'w') as file:
            file.write("")


if __name__ == "__main__":

    valid_max = False
    while not valid_max:
        max_parts = input("Input maximum parts to use:\n")
        try:
            max_parts = int(max_parts)
            valid_max = True
        except ValueError:
            print("Please input a valid integer.\n")


    sites = []
    site_count = get_restriction_sites()

    parts = []
    for filename in os.listdir('backend/parts'):
        get_data(parse('backend/parts/' + filename))

    # Add letter signifying part type before name
    # Just for verification of sequences
    for p in parts:
        p.prepend_type()

    selected = []
    selected_count = get_selected_parts()

    create_data_dzn()
    create_restriction_mzn()
    create_selected_mzn()

    os.system('minizinc -a solver/synbio.mzn')

