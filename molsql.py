import os
import sqlite3
import MolDisplay

class Database:
    def __init__(self, reset=False):
        if reset:
            conn = sqlite3.connect('molecules.db')
            conn.close()
            import os
            os.remove('molecules.db')
            
        self.conn = sqlite3.connect('molecules.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Elements(
                    ELEMENT_NO INTEGER NOT NULL,
                    ELEMENT_CODE VARCHAR(3) PRIMARY KEY NOT NULL,
                    ELEMENT_NAME VARCHAR(32) NOT NULL,
                    COLOUR1 CHAR(6) NOT NULL,
                    COLOUR2 CHAR(6) NOT NULL,
                    COLOUR3 CHAR(6) NOT NULL,
                    RADIUS DECIMAL(3) NOT NULL
                )""")
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Atoms (
                ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE VARCHAR(3) NOT NULL ,
                X DECIMAL(7,4) NOT NULL,
                Y DECIMAL(7,4) NOT NULL,
                Z DECIMAL(7,4) NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bonds (
                Bond_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1 INTEGER NOT NULL,
                A2 INTEGER NOT NULL,
                EPAIRS INTEGER NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Molecules (
                MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT UNIQUE NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS MoleculeAtom (
                MOLECULE_ID INTEGER NOT NULL,
                ATOM_ID INTEGER UNIQUE NOT NULL,
                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (ATOM_ID) REFERENCES Atom(ATOM_ID)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS MoleculeBond (
                MOLECULE_ID INTEGER NOT NULL,
                BOND_ID INTEGER UNIQUE NOT NULL,
                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                FOREIGN KEY (BOND_ID) REFERENCES Bond(BOND_ID)
            )
        """)
        self.conn.commit()

    def __setitem__(self, table, values):
        value=len(values)
        holderrs = ', '.join(['?'] * value)
        query = f"INSERT INTO {table} VALUES ({holderrs})"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def add_atom(self, molname, atom):
        element_code = atom.element
        values = (None, element_code, atom.x, atom.y, atom.z)
        self['Atoms'] = values
        atom_id = self.cursor.lastrowid
        mol_id = self.cursor.execute(f"""
            SELECT MOLECULE_ID FROM Molecules WHERE NAME = "{molname}"
        """).fetchone()[0]
        self.__setitem__('MoleculeAtom', (mol_id, atom_id))
        
    def add_bond(self, molname, bond):
        a1_id = bond.a1
        a2_id = bond.a2
        epairs = bond.epairs
        values = (None, a1_id, a2_id, epairs)
        self['Bonds'] = values
        bond_id = self.cursor.lastrowid
        mol_id = self.cursor.execute(f"""
            SELECT MOLECULE_ID FROM Molecules WHERE NAME = "{molname}"
        """).fetchone()[0]
        self['MoleculeBond'] = (mol_id, bond_id)
        
    def add_molecule(self, name, fp):
        molecule = MolDisplay.Molecule()
        molecule.parse(fp)
        # Add molecule to Molecules table
        self.cursor.execute(f"""
            INSERT INTO Molecules (NAME)
                VALUES ("{name}")
        """)
        # molecule_id = self.cursor.lastrowid
        # Add atoms to Atoms and MoleculeAtom tables
        for i in range(molecule.atom_no):
            atom = molecule.get_atom(i)
            self.add_atom(name, atom)
            
        # Add bonds to Bonds and MoleculeBond tables
        for i in range(molecule.bond_no):
            bond = molecule.get_bond(i)
            self.add_bond(name, bond)
            
    def get_molecule_id(self, name):
        self.cursor.execute("SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?", (name,))
        # return result

    def close(self):
        self.conn.close()
        
    def radius(self):
        query = "SELECT ELEMENT_CODE, RADIUS FROM Elements"
        eryting=self.cursor.execute(query).fetchall()
        rows = eryting
        return {code: radius for code, radius in rows}
    
    def radial_gradients(self):
        self.cursor.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")
        gradients = []
        eryting=self.cursor.fetchall()
        rows = eryting
        default = """
                <radialGradient id="Default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                    <stop offset="0%" stop-color="#FF0000"/>
                    <stop offset="50%" stop-color="#64A0BE"/>
                    <stop offset="100%" stop-color="#020202"/>
                </radialGradient>
            """
        gradients.append(default)
        for row in rows:
            gradient = """
                <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                    <stop offset="0%%" stop-color="#%s"/>
                    <stop offset="50%%" stop-color="#%s"/>
                    <stop offset="100%%" stop-color="#%s"/>
                </radialGradient>
            """ % row
            gradients.append(gradient)
        return ''.join(gradients)
    
    def load_mol(self, name):
        molecule = MolDisplay.Molecule()
        self.cursor.execute("""
            SELECT Atoms.ATOM_ID, Elements.ELEMENT_CODE, X, Y, Z
            FROM Atoms
            JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
            JOIN Elements ON Atoms.ELEMENT_CODE = Elements.ELEMENT_CODE
            WHERE MoleculeAtom.MOLECULE_ID = (
                SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?
            )
            ORDER BY Atoms.ATOM_ID
        """, (name,))
        eryting=self.cursor.fetchall()
        for row in eryting:
            molecule.append_atom(row[1], row[2], row[3], row[4])
        
        self.cursor.execute("""
            SELECT Bonds.BOND_ID, A1, A2, EPAIRS
            FROM Bonds
            JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID
            WHERE MoleculeBond.MOLECULE_ID = (
                SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?
            )
            ORDER BY Bonds.BOND_ID
        """, (name,))
        eryting=self.cursor.fetchall()
        for row in eryting:
            molecule.append_bond(row[1], row[2], row[3])
        
        return molecule
    
    def element_name(self):
        query = "SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements"
        eryting=self.cursor.execute(query).fetchall()
        rows = eryting
        return {code: name for code, name in rows}
    
    

if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    # db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    # db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    # db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    
    # fp = open( 'water-3D-structure-CT1000292221.sdf' );
    # db.add_molecule( 'Water', fp );
    # fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    # db.add_molecule( 'Caffeine', fp );
    fp = open( 'CID_31260.sdf' );
    db.add_molecule( 'molecule', fp );
    print(fp)
    
    db = Database(reset=False); # or use default
    MolDisplay.radius = db.radius();
    MolDisplay.element_name = db.element_name();
    MolDisplay.header += db.radial_gradients();
    for molecule in [ 'molecule' ]:
        mol = db.load_mol( molecule );
        mol.sort();
        fp = open( molecule + ".svg", "w" );
        fp.write( mol.svg() );
        fp.close();