import sys
from get_direct import get_direct
from lattice_length import get_lattice_length
from element_info import get_sort_element

args = sys.argv

e_name = get_sort_element('POSCAR.xyz')[0]
e_number = get_sort_element('POSCAR.xyz')[1]
sorted_list = get_sort_element('POSCAR.xyz')[2]
lattice_length = get_lattice_length('POSCAR')
directs = get_direct(sorted_list, lattice_length)

with open('POSCAR_test','w') as f2:
    with open('POSCAR','r') as f_poscar:
        fr_pos = f_poscar.readlines()
        for l in fr_pos[:5]:
            f2.write(l)          #copy 1~5
        names = "   "+"   ".join(e_name)+"\n"
        f2.write(names)
        numbers = "   "+"   ".join(e_number)+"\n"
        f2.write(numbers)
        f2.write('Direct'+"\n")
        for direct in directs:
            f2.write("      "+"      ".join(direct)+"\n")


