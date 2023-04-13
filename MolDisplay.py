from molecule import molecule

radius = {}
element_name = {}
header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500

# Create an Atom class
class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z
        
    def __str__(self):
        return "Element: {} x: {} y: {} z: {}".format(self.c_atom.element, self.c_atom.x, self.c_atom.y, self.z)
    
    def svg(self):
        hundo = 100.0
        x = hundo * self.c_atom.x + offsetx
        y = hundo * self.c_atom.y + offsety
        r = radius[self.c_atom.element]
        # print(self.c_atom.element)
        color = element_name[self.c_atom.element]
        
        if color == None:
            color = 'Default'
            
        # print("Color: ", color)
        # print("Radius: ",r)
        return '<circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (x, y, r, color)
        # return '<circle cx="%.2f" cy="%.2f""/>\n' % (x, y)


# Create a Bond class
class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.z = c_bond.z

    def __str__(self):
        return "Bond between Atom: {} and {} ePairs: {} x1: {} y1: {} x2: {} y2: {} z: {}, bond_len: {}, dx: {}, dy: {}".format(self.c_bond.a1, self.c_bond.a2, self.c_bond.epairs, self.c_bond.x1,self.c_bond.y1, self.c_bond.x2, self.c_bond.y2, self.c_bond.z, self.c_bond.len, self.c_bond.dx, self.c_bond.dy)
        

    def svg(self):
        hundo = 100.0
        x1 = ((self.c_bond.x1 *hundo) + offsetx)
        y1 = ((self.c_bond.y1 *hundo) + offsety)
        x2 = ((self.c_bond.x2 *hundo) + offsetx)
        y2 = ((self.c_bond.y2 *hundo) + offsety)
        
        dx = (self.c_bond.dx )
        
        teno=10.0
        dy = (self.c_bond.dy)
        
        return '<polygon points="%.2f, %.2f %.2f, %.2f %.2f, %.2f %.2f, %.2f" fill="green"/>\n' % (
            (x1 + dy * teno), (y1 - dx * teno),
            (x1 - dy * teno), (y1 + dx * teno),
            (x2 - dy *teno), (y2 + dx *teno),
            (x2 + dy *teno), (y2 - dx *teno)
        )
        
# Create a Molecule class
class Molecule(molecule):
    
    def __str__(self):
        i=0
        atomno=self.atom_no
        for i in range(atomno-1+1):
            temp_atom=self.get_atom(i)
            atom = Atom(temp_atom)
            print(atom)
        bondno=self.bond_no
        for i in range(bondno-1+1):
            temp_bond=self.get_bond(i)
            bond = Bond(temp_bond)
            print(bond)
        return " "
    
    def svg(self):
        
        svg = header

        i, j = 0, 0
        size = self.atom_no+self.bond_no
        list_atom_z = [0]*self.atom_no
        list_z = [0]*size
        svg_return = [0]*self.atom_no
        svg_return2 = [0]*self.bond_no
        
        for i in range(self.atom_no):
            temp_atom=self.get_atom(i)
            atom = Atom(temp_atom)
            svg_return[i] = atom.svg()
            list_atom_z[i] = atom.z
            
        list_bond_z = [0]*self.bond_no
        for j in range(self.bond_no):
            temp_bond=self.get_bond(j)
            bond = Bond(temp_bond)
            svg_return2[j] = bond.svg()
            list_bond_z[j] = bond.z
        i=0
        
        # print("Atoms: ", list_atom_z)
        # print("Bonds: ", list_bond_z)
        list_z = list_atom_z + list_bond_z
        # print("Molecule: ",list_z)
        svg_return3 = svg_return +svg_return2
        i=0
        
        for i in range(self.atom_no):
            list_z, svg_return3 = zip(*sorted(zip(list_z, svg_return3)))
        
        i=0
        for i in range(size):
            svg += svg_return3[i]
        

        svg += footer
        return svg

    def parse(self, file):
        
        content = file.readlines()
        
        num_atoms, num_bonds = map(int, content[3].strip().split()[:2])
        i=0
        line1=4
        line1dup=4
        for i in range(num_atoms):
            atom_data = content[line1].strip().split()[:line1dup]
            # print(atom_data)
            x = float(atom_data[0])
            y = float(atom_data[1])
            z = float(atom_data[2])
            element = atom_data[3]
            self.append_atom(element, x,y,z)
            line1+=1
            
        line2=i+1+1+3   
        line2dup=3
        j=0   
        for j in range(num_bonds):
            bond_data = content[line2].strip().split()[:line2dup]
            # print(bond_data)
            a1 = int(bond_data[0])-1
            a2 = int(bond_data[1])-1
            ePairs = int(bond_data[2])
            self.append_bond(a1, a2, ePairs)
            line2+=1
        # self.sort()
        