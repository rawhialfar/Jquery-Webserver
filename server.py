from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from molsql import Database
import molecule
import urllib;  
import json
import io
import MolDisplay
import sys

public_files = [ '/index.html', '/style.css', '/script.js' ];
molname = None;
names_list = []
num_atoms = [0]*100
num_bonds = [0]*100
count=0
ifDelete=0
molCount = -1
data = []
mol_list = []
for i in range(100):
    new_molecule = MolDisplay.Molecule()
    mol_list.append(new_molecule)

class MyRequestHandler(BaseHTTPRequestHandler):
    if os.path.exists('molecules.db'):
        os.remove('molecules.db')
    
        
    def do_GET(self):
        if self.path == '/display_options':
            db = Database(reset=False);
            db.create_tables();
            newName = ''
            em = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() 
            
            # print(json.dumps(message).encode())
            # data = json.dumps(message).encode()
            
            global count
            # print(len(em))
            # print(count)
                    
                
            # print("Atoms: ", num_atoms[count], "Bonds: ", num_bonds[count])
                
            if len(em) > 0:
                for i in range(len(em)):
                    # print(i)
                    newName = em[i] + (num_atoms[i], num_bonds[i])
                    em[i] = newName
                    # print (newName)
            
            # count = len(em)
                
            data = json.dumps(em).encode()
            # print(data)
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.end_headers();
            
            self.wfile.write( data );
            
        elif self.path == '/display_elements':
            
            db = Database(reset=False);
            db.create_tables();
            
            # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
            db.cursor.execute('SELECT COUNT(*) FROM Elements')
            result = db.cursor.fetchone()[0]
            
            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
            global ifDelete
            # check if the table is empty
            if result == 0 and ifDelete==0:
                # print('The table is empty')
                db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
                db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
                db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
                db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
                # print('The table is not empty')
            
            em = db.conn.execute( "SELECT * FROM Elements;" ).fetchall() 
            
            message = em;
            # print(json.dumps(message).encode())
            data = json.dumps(message).encode()
            
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "applications/json" );
            self.end_headers();
            
            self.wfile.write(data);
        else:
            if self.path in public_files:   # make sure it's a valid file
                self.send_response( 200 );  # OK
                if self.path in '/style.css':
                    self.send_header( "Content-type", "text/css" );
                else:
                    self.send_header( "Content-type", "text/html" );

                fp = open( self.path[1:] ); 
                # [1:] to remove leading / so that file is found in current dir

                # load the specified file
                page = fp.read();
                fp.close();
                
                # create and send headers
                self.send_header( "Content-length", len(page) );
                self.end_headers();

                # send the contents
                self.wfile.write( bytes( page, "utf-8" ) );
            else:
                self.send_response( 404 );
                self.end_headers();
                self.send_error(bytes("404: Page not found", "utf-8" ))
            
    def do_POST(self):
        if self.path == "/add_element":
            
            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode("utf-8")
            
            # print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( post_data );
            db = Database(reset=False);
            db.create_tables();
                
            elementNo = postvars['elementNo'][0]
            elementCode = postvars['elementCode'][0]
            elementName = postvars['elementName'][0]
            color1 = postvars['color1'][0][1:]
            color2 = postvars['color2'][0][1:]
            color3 = postvars['color3'][0][1:]
            
            # do same for rotation one
            if int(elementNo) < 0:
                print("Error: Element Number is less than zero!")
                message = "Error: Element Number is less than zero!";
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                
            elif (elementCode.isalpha() == False): 
                print("Error: Element Code is not valid")
                message = "Error: Element Code is not valid";
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                
            if 'elementRadius' in postvars:
                elementRadius = postvars['elementRadius'][0]
            else:
                elementRadius=40
            # element =  postvars['name'][0]
            
            # self.cursor.preventdeafult()
            # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );

            # db['Elements'] = ( elementNo, elementCode, elementName, color1, color2, color3, elementRadius);
            
            db.conn.execute("INSERT INTO Elements VALUES (?, ?, ?, ?, ?, ?, ?)",
            (elementNo, elementCode, elementName, color1, color2, color3, elementRadius))
            # if ()
            
            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
            
            db.conn.commit()
            message = "Element has been added";
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );
            
        elif self.path == "/remove_element":

            # this is specific to 'multipart/form-data' encoding used by POST
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode("utf-8")
            global ifDelete
            ifDelete+=1
            # print( repr( body.decode('utf-8') ) );

            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( post_data );
            db = Database(reset=False);
            db.create_tables();
            print("Database Before:")
            print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
            # print(postvars)
            elementNo = postvars['elementNo'][0]
            
            
            rows_deleted1 = db.cursor.rowcount
            
            db.cursor.execute("DELETE FROM Elements WHERE ELEMENT_NO = ?", (elementNo,))
            rows_deleted2 = db.cursor.rowcount
            
            if rows_deleted2 > rows_deleted1:
                # print("Removed Element:", elementNo, elementCode, elementName, color1, color2, color3, elementRadius )
                db.conn.commit()
                message = "Element has been removed";
            else:
                print("No rows were deleted.")
                message = "Error: No element was removed";
                
            print("\nDatabase After:")
            print( db.cursor.execute( "SELECT * FROM Elements;" ).fetchall() );

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
            
        elif self.path == "/sdf_upload":
            # code to handle sdf_upload

            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode("utf-8")
            
            postvars = urllib.parse.parse_qs( post_data );
            db = Database(reset=False);
            db.create_tables();
            
            # Create a TextIOWrapper object from the bytes object
            lines = post_data.splitlines()[4:]
            lines = lines[:-4]
            lines = '\n'.join(lines)
            
            
            print("File Info:\n", lines);
            print("End of File Info!\n");
            
            byters = io.BytesIO(bytes(lines, "utf-8"))
            fp = io.TextIOWrapper(byters)
            
            fp2=fp
            content = fp2.readlines()
            global count
            print(count)
            num_atoms[count], num_bonds[count] = map(int, content[3].strip().split()[:2])
            print("Atoms: ", num_atoms[count], "Bonds: ", num_bonds[count])
            count+=1
            
            fp.seek(0, os.SEEK_SET)
            
            # Retrieving the molecule name
            # print("NAME: ",postvars);
            name_value = postvars[' name'][1]  # Get the second element of the list

            start_index = name_value.find('\r\n\r\n')  # Find the index of the first occurrence of '\r\n'
            end_index = name_value.find('\r\n------')  # Find the index of the first occurrence of '\r\n------'

            molname = name_value[start_index+2:end_index].strip()
            
            print("Molecule Name: ", molname, "\n" );
            # Retrieving the molecule name
            
            # self.cursor.execute("DELETE FROM Elements WHERE ELEMENT_NO = ?", (elementNo,))
            db.cursor.execute("SELECT COUNT(*) FROM Molecules");
            result = db.cursor.fetchone()
            molname_dupe=''
            row_count=result[0]
            p=0
            # print(row_count)
            if (row_count != 0):
                molname_dupe = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall();
                
            for _, name in molname_dupe:
                names_list.append(name)
                
            for name in names_list:
                if molname == name:
                    print("Duplicate Name!")
                    p=1
                    break;
            
            global molCount
            molCount+=1
            if (molname_dupe != molname and p!=1):
                mol_list[molCount].parse(fp)
            
            fp.seek(0, os.SEEK_SET)
                    
            if (molname_dupe != molname and p!=1):
                db.add_molecule( molname, fp );
        
            message = "sdf file uploaded to database";

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/plain" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();

            self.wfile.write( bytes( message, "utf-8" ) );
        
        elif self.path == "/select_molecule":
            
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode("utf-8")
            
            postvars = urllib.parse.parse_qs( post_data );
            db = Database(reset=False);
            
            em = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() 
            
            
            print("Molecule: ", postvars['name'][0])
            namePicked=postvars['name'][0]
            
            for i, tup in enumerate(em):
                if namePicked in tup:
                    index = i
                    break
            
            elementsList = [0]*mol_list[index].atom_no
            
            for molecules in [ namePicked ]:
                mol = db.load_mol(molecules)
            
            for i in range(mol_list[index].atom_no):
                temp_atom=mol_list[index].get_atom(i)
                atom = MolDisplay.Atom(temp_atom)
                elementsList[i]=atom.c_atom.element
            
            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();
            
            
            uncommon_key = set(elementsList) - set(MolDisplay.element_name.keys())
                
            # print(uncommon_key)
            for element in uncommon_key:
                if element not in MolDisplay.element_name.keys():
                    print("UNCOMMON Key: ", element)
                    MolDisplay.radius[element] = 40;
                    MolDisplay.element_name[element] = None;
                    
            svg = mol_list[index].svg()
            print(svg)
            
            self.send_response(200)
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(svg) );
            self.end_headers()
            
            self.wfile.write(bytes(svg, "utf-8") )
            
        elif self.path == "/rotate_molecule":
            
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode("utf-8")
            
            postvars = urllib.parse.parse_qs( post_data );
            db = Database(reset=False);
            
            print("Molecule: ", postvars['name'][0])
            namePicked=postvars['name'][0]
            
            em = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() 
            
            for i, tup in enumerate(em):
                if namePicked in tup:
                    index = i
                    break
            elementsList = [0]*mol_list[index].atom_no
                
            for i in range(mol_list[index].atom_no):
                temp_atom=mol_list[index].get_atom(i)
                atom = MolDisplay.Atom(temp_atom)
                elementsList[i]=atom.c_atom.element
            
            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.header += db.radial_gradients();
            
            
            uncommon_key = set(elementsList) - set(MolDisplay.element_name.keys())
                
            # print(uncommon_key)
            for element in uncommon_key:
                if element not in MolDisplay.element_name.keys():
                    print("UNCOMMON Key: ", element)
                    MolDisplay.radius[element] = 40;
                    MolDisplay.element_name[element] = None;
                    
            print(postvars)
            
            x= postvars['x'][0]
            y= postvars['y'][0]
            z= postvars['z'][0]
            x=int(x)
            y=int(y)
            z=int(z)
            namePicked=postvars['name'][0]
            
            if x > 0:
                mx = molecule.mx_wrapper(x,0,0);
                mol_list[index].xform( mx.xform_matrix );
            if y > 0:
                my = molecule.mx_wrapper(0,y,0);
                mol_list[index].xform( my.xform_matrix );
            if z > 0:
                mz = molecule.mx_wrapper(0,0,z);
                mol_list[index].xform( mz.xform_matrix );
            # print(mol)
            # for molecules in [ namePicked ]:
            svg = mol_list[index].svg()
            print(svg)
                
            self.send_response(200)
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(svg) );
            self.end_headers()
            
            self.wfile.write(bytes(svg, "utf-8") )
            
        else:
            self.send_response( 404 );
            self.end_headers();
            self.send_error(bytes("404: File not found", "utf-8" ))
            
        
# python3.7 server.py 59045
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    
    server = HTTPServer(("", port), MyRequestHandler)
    print("Server running on port", port)
    server.serve_forever()
    
    
