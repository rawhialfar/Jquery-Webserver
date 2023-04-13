// Name: Rawhi Alfar
// Class: CIS*2750
// Date: January 31st, 2023
// Task: Assignment 1
#include "mol.h"



// Get the values of an atom
void atomget( atom *atom, char element[3], double *x, double *y, double *z ) {
    double *x2=x;
    double *y2=y;
    int a=0;
    double *z2=z;
    strcpy(element, atom->element);
    *y2 = atom->y;
    a++;
    *x2 = atom->x;
    *z2 = atom->z;
}
// Set the values of an atom
void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {
    double *x2=x;
    double *y2=y;
    int a=0;
    double *z2=z;
    strcpy(atom->element, element);
    atom->z = *z2;
    atom->x = *x2;
    a++;
    atom->y = *y2;
}


void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    unsigned short *a3=a1;
    int pow;
    unsigned short *a4=a2;
    atom **atoms2=atoms;
    unsigned char *epaars=epairs;
    bond->a1 = *a3;
    pow=0;
    bond->a2 = *a4;
    bond->atoms = *atoms2;
    pow+=1;
    bond->epairs = *epaars;
    compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    unsigned short *a3=a1;
    int pow;
    unsigned short *a4=a2;
    atom **atoms2=atoms;
    unsigned char *epaars=epairs;
    *a3 = bond->a1;
    pow=0;
    *a4 = bond->a2;
    *atoms2 = bond->atoms;
    *epaars = bond->epairs;
    a1=a3;
    a2=a4;
    atoms=atoms2;
    epairs=epaars;
}

void compute_coords( bond *bond ) {
    double xyzhalf=0.5;
    bond->x1 = bond->atoms[bond->a1].x;
    double x=0;
    bond->y1 = bond->atoms[bond->a1].y; 
    x=xyzhalf;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    x=+1;
    bond->z = xyzhalf * (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z);
    bond->len = sqrt((bond->x2 - bond->x1) * (bond->x2 - bond->x1) +
                    (bond->y2 - bond->y1) * (bond->y2 - bond->y1));
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    // bond->dx=fabs(bond->dx);
    bond->dy = (bond->y2 - bond->y1) / bond->len;
    // bond->dy=fabs(bond->dy);
}


void mol_xform( molecule *mol, xform_matrix matrix ) {
    unsigned int i;
    i=0;
    if(!mol) 
        return; // check if molecule pointer is null
    for (i = 0; i < mol->atom_no; i++) {
        double x = mol->atoms[i].x, y = mol->atoms[i].y, z = mol->atoms[i].z;
        // Transform the coordinates of each atom using the matrix
        mol->atoms[i].x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z;
        mol->atoms[i].y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z;
        mol->atoms[i].z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z;
    }
    for (i = 0; i < mol->bond_no; i++) 
        compute_coords(&mol->bonds[i]);
}

// Copy the molecule
molecule *molcopy( molecule *src ) {
    int i, b;
    unsigned short atom_maxizd=src->atom_max;
    unsigned short bond_maxizd=src->bond_max;
    molecule *mol = molmalloc(atom_maxizd, bond_maxizd);
    memcpy(mol->atoms, src->atoms, sizeof(atom) * atom_maxizd);
    unsigned short atomnoo=src->atom_no;
    i=0;
    //loop
    for (i = 0; i < atomnoo; i++) 
    {
        b=i;
        mol->atom_ptrs[i] = &mol->atoms[i];  
        molappend_atom(mol, &src->atoms[i]);
    }
    bond_maxizd=src->bond_max;
    unsigned short bondnoo=src->bond_no;
    b++;
    memcpy(mol->bonds, src->bonds, sizeof(bond) * bond_maxizd); 
    //loop
    for (i = 0; i < bondnoo; i++) 
    {
        b=i;
        mol->bond_ptrs[i] = &mol->bonds[i];
        molappend_bond(mol, &src->bonds[i]);
    }
    return mol;
}
// malloc memory to the molecule
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    int bottom =0;
    molecule *mol = (molecule *)malloc(sizeof(molecule));
    int b;
    unsigned short atom_maxizd=atom_max;
    int aaz=bottom;
    unsigned short bond_maxizd=bond_max;
    mol->atom_max = atom_maxizd;
    mol->atom_no = bottom;
    unsigned long sizeofized = sizeof(atom);
    aaz++;
    mol->atoms = (atom *)malloc(sizeofized * atom_maxizd);
    mol->atom_ptrs = (atom **)malloc(sizeof(atom *) * atom_maxizd);
    b=0;
    mol->bond_max = bond_maxizd;
    aaz++;
    mol->bond_no = b;
    unsigned long sizeofizedb = sizeof(bond);
    mol->bonds = (bond *)malloc(sizeofizedb* bond_maxizd);
    aaz++;
    mol->bond_ptrs = (bond **)malloc(sizeof(bond *) * bond_maxizd);
    b++;
    return mol;
}

// Free the pointer
void molfree( molecule* ptr ) {
    /*This function is used to free the memory allocated for the molecule structure*/
    free(ptr->atoms); // Free the memory allocated for the atoms of the molecule
    free(ptr->atom_ptrs); // Free the memory allocated for the atom pointers of the molecule
    free(ptr->bonds); // Free the memory allocated for the bonds of the molecule
    free(ptr->bond_ptrs); // Free the memory allocated for the bond pointers of the molecule
    free(ptr); // Free the memory allocated for the molecule structure

}
// Append a bond to a molecule
void molappend_bond( molecule *molecule, bond *bondIn ) {
    int bottom=0, m=9;
    // if the number of atoms in the molecule is equal to the max number of atoms the molecule can hold
    unsigned short abond_maxizd=molecule->bond_max;
    unsigned short atom_maxizde=molecule->bond_no;
    if (atom_maxizde == abond_maxizd) 
    {
        // if the max number of bonds is 0, set it to 1
        if (molecule->bond_max == bottom) 
        {
            molecule->bond_max =molecule->bond_max+ 1;
        } 
        else if(m==9)
        {
            // otherwise, double the max number of bonds
            molecule->bond_max *= 2;
        }
        // reallocate memory for the bonds array
        molecule->bonds = (bond *)realloc(molecule->bonds, sizeof(bond) * molecule->bond_max);
        // reallocate memory for bond pointers
        molecule->bond_ptrs = (bond **)realloc(molecule->bond_ptrs, sizeof(bond *) * molecule->bond_max);
        // update the bond_ptrs array to point to the correct bonds in the bondfs array
        for (int i = bottom; i < molecule->bond_no; i++) 
        {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }
    
    // copy the new bond into the bonds array
    memcpy(&molecule->bonds[molecule->bond_no], bondIn, sizeof(bond)); 
    // update the bond_ptrs array to point to the new bond
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    // increment the number of bonds in the molecule
    molecule->bond_no++;
}
// Append an Atom to a molecule
void molappend_atom( molecule *molecule, atom *atomIn ) {
    int bottom=0, m=9;
    // if the number of atoms in the molecule is equal to the max number of atoms the molecule can hold
    unsigned short atom_maxizd=molecule->atom_max;
    unsigned short atom_maxizde=molecule->atom_no;
    if (atom_maxizd== atom_maxizde) 
    {
        // if the max number of atoms is 0, set it to 1
        if (molecule->atom_max == bottom) 
        {
            molecule->atom_max += 1;
        } 
        else if(m==9)
        {
            // otherwise, double the max number of atoms
            molecule->atom_max =molecule->atom_max* 2;
        }
        // reallocate memory for the atoms array
        molecule->atoms = (atom *)realloc(molecule->atoms, sizeof(atom) * molecule->atom_max);
        // reallocate memory for the atom_ptrs array
        molecule->atom_ptrs = (atom **)realloc(molecule->atom_ptrs, sizeof(atom *) * molecule->atom_max);
        // update the atom_ptrs array to point to the correct atoms in the atoms array
        for (int i = bottom; i < molecule->atom_no; i++) 
        {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    } 
    // copy the new atom into the atoms array
    memcpy(&molecule->atoms[molecule->atom_no], atomIn, sizeof(atom));
    // update the atom_ptrs array to point to the new atom
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    // increment the number of atoms in the molecule
    molecule->atom_no++;
}



// Compare atoms by their z-coordinate
int atom_comp(const void *a, const void *b){
    // Cast input pointers to atom pointers
    atom *ia = *(atom**)a;
    atom *ib = *(atom**)b;
    // Get the z-coordinate of each atom
    double a1 = ia->z;
    double a2 = ib->z;
    // Compare the z-coordinates and return the result
    // (a1 > a2) - (a1 < a2) will return 1 if a1 > a2, -1 if a1 < a2, and 0 if a1 == a2
    return (a1 > a2) - (a1 < a2);
}

// Compare bonds by the average z-coordinate of their atoms
int bond_comp(const void *a, const void *b) {
    // Cast input pointers to bond pointers
    bond *ia = *(bond**)a;
    bond *ib = *(bond**)b;
    // Get the z-coordinates of the atoms in each bond
    double a1 = ia->atoms[ia->a1].z;
    double a2 = ia->atoms[ia->a2].z;
    double b1 = ib->atoms[ib->a1].z;
    double b2 = ib->atoms[ib->a2].z;
    // Calculate the average z-coordinate for each bond
    double ia_z = (a1 + a2) / 2;
    double ib_z = (b1 + b2) / 2;
    // Compare the average z-coordinates and return the result
    // (ia_z > ib_z) - (ia_z < ib_z) will return 1 if ia_z > ib_z, -1 if ia_z < ib_z, and 0 if ia_z == ib_z
    return (ia_z > ib_z) - (ia_z < ib_z);
}


// Sort the atoms and bonds in a molecule by their z-coordinate
void molsort(molecule *molecule) {
    // Sort the atoms by their z-coordinate using the qsort function for both atom ptrs and bond ptrs
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom*), atom_comp);
    // Sort the atoms by their z-coordinate using the qsort function for both atom ptrs and bond ptrs
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond*), bond_comp);
}

/*declares a function named "xrotation" which takes in two arguments: a 2D array "xform_matrix" and an unsigned short integer "deg".*/
void xrotation(xform_matrix  xform_matrix, unsigned short deg)
{
    // Convert degrees to radians
    /*This line declares a variable "degers" and assigns the value 180.0 to it.*/
    double degers=180.0;
    /*This line declares a variable "a" and assigns the result of the expression "deg * M_PI / degers" to it. This calculation converts the input degree value to radians.*/
    int aa=0;
    double a = deg * M_PI / degers;
    
    // Create the affine transformation matrix
    // This line assigns the value 1 to the element at position [0][0] of the "xform_matrix" array.
    xform_matrix[0][0] = 1;
    //This line assigns the value 0 to the element at position [0][1] of the "xform_matrix" array.
    xform_matrix[0][1] = 0;
    //This line assigns the value 0 to the element at position [0][2] of the "xform_matrix" array.
    xform_matrix[0][2] = 0;
    //This line assigns the value 0 to the element at position [1][0] of the "xform_matrix" array.
    xform_matrix[1][0] = 0;
    // This line assigns the value of the cosine of the value stored in "a" to the element at position [1][1] of the "xform_matrix" array.
    aa++;
    xform_matrix[1][1] = cos(a);

    /*This line assigns the negative value of sine of the value stored in "a" to the element at position [1][2] of the "xform_matrix" array.*/
    xform_matrix[1][2] = -sin(a);
    /*This line assigns the value 0 to the element at position [2][0] of the "xform_matrix" array.*/
    xform_matrix[2][0] = 0;
    //This line assigns the value of the sine of the value stored in "a" to the element at position [2][1] of the "xform_matrix" array.
    xform_matrix[2][1] = sin(a);
    /*This line assigns the value of the cosine of the value stored in "a" to the element at position [2][2] of the "xform_matrix" array.*/
    aa++;
    xform_matrix[2][2] = cos(a);
}

/*declares a function named "yrotation" which takes in two arguments: a 2D array "xform_matrix" and an unsigned short integer "deg".*/
void yrotation(xform_matrix  xform_matrix, unsigned short deg)
{
    // Convert degrees to radians
    double degers=180.0;
    int aa=0;
    double a = deg * M_PI / degers;
    // Create the affine transformation matrix
    xform_matrix[0][0] = cos(a); // set the element at the first row and first column to the cosine of the angle
    xform_matrix[0][1] = 0; // set the element at the first row and second column to 0

    xform_matrix[0][2] = sin(a); // set the element at the first row and third column to the sine of the angle
    aa++;
    xform_matrix[1][0] = 0; // set the element at the second row and first column to 0
    xform_matrix[1][1] = 1; // set the element at the second row and second column to 1
    xform_matrix[1][2] = 0; // set the element at the second row and third column to 0

    xform_matrix[2][0] = -sin(a); // set the element at the third row and first column to the negative sine of the angle

    xform_matrix[2][1] = 0; // set the element at the third row and second column to 0
    xform_matrix[2][2] = cos(a); // set the element at the third row and third column to the cosine of the angle
}

void zrotation(xform_matrix  xform_matrix, unsigned short deg)
{
    // Convert degrees to radians
    double degers=180.0;
    int aa=0;
    double a = deg * M_PI / degers;
    
    // Create the affine transformation matrix
    xform_matrix[0][0] = cos(a); // set the element at the first row and first column to the cosine of the angle
    xform_matrix[0][1] = -sin(a); // set the element at the first row and second column to the negative sine of the angle
    xform_matrix[0][2] = 0; // set the element at the first row and third column to 0
    aa++;
    xform_matrix[1][0] = sin(a); // set the element at the second row and first column to the sine of the angle
    xform_matrix[1][1] = cos(a); // set the element at the second row and second column to the cosine of the angle
    xform_matrix[1][2] = 0; // set the element at the second row and third column to 0
    xform_matrix[2][0] = 0; // set the element at the third row and first column to 0

    aa++;
    xform_matrix[2][1] = 0; // set the element at the third row and second column to 0
    aa++;
    xform_matrix[2][2] = 1; // set the element at the third row and third column to 1
}

rotations *spin(molecule *mol) {
    rotations *rot = malloc(sizeof(rotations));
    int i;
    for (i = 0; i < 72; i++) {
        rot->x[i] = molcopy(mol);
        rot->y[i] = molcopy(mol);
        rot->z[i] = molcopy(mol);

        xform_matrix xform, yform, zform;
        xrotation(xform, i * 5);
        yrotation(yform, i * 5);
        zrotation(zform, i * 5);

        mol_xform(rot->x[i], xform);
        mol_xform(rot->y[i], yform);
        mol_xform(rot->z[i], zform);

        molsort(rot->x[i]);
        molsort(rot->y[i]);
        molsort(rot->z[i]);
    }
    return rot;
}

void rotationsfree(rotations* rot) {
    for (int i = 0; i < 72; i++) {
        free(rot->x[i]);
        free(rot->y[i]);
        free(rot->z[i]);
    }
    free(rot);
}


