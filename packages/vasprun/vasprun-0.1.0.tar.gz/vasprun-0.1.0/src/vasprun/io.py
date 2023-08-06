"""
This is a my first cut at parsing xml, and it is very rough.
"""
import os
import numpy as np
from lxml import etree
from ase import Atoms
from ase.dft.kpoints import bandpath

VASPPARAMETERS = [
    'ENMAX', 'ENAUG', 'EDIFF', 'EREF',
    'NELECT', 'NBANDS',
    'ISPIN', 'LSORBIT', 'LNONCOLLINEAR', 'SAXIS', 'MAGMOM',
    'IBRION', 'ISIF', 'EDIFFG',
    'GGA',
]

# dictionary with {attribute: element} pairs in the 'calculation' section
VASP_CALCULATED_ENERGIES = {
    'e_fr_energy': 'energy/i',
    'e_wo_entrp': 'energy/i',
    'e_0_energy': 'energy/i',
    'efermi': 'dos/i',
}


def boolean(s):
    if s.strip() == 'T':
        return True
    else:
        return False

CAST = {'int': int, 'logical': boolean, 'float': float, 'string': str}

def get_text_from_section(stem, path, key):
    """get leaf text from section"""
    subsec = path.split('/')
    for sub in subsec[:-1]:
        stem = stem.find('./{}'.format(sub))
    leaf = stem.find('./{}[@name="{}"]'.format(subsec[-1], key))
    return leaf.text.strip()

def get_text_from_named_subsection(stem, path, key, sep='separator'):
    """get leaf text from named subsection"""
    subsec = path.split('/')
    for sub in subsec[:-1]:
        stem = stem.find('./{}[@name="{}"]'.format(sep, sub))
    leaf = stem.find('./{}[@name="{}"]'.format(subsec[-1], key))
    return leaf.text.strip()

def get_vasp_parameters(stem, data=None):
    """Get runtime parameters from vasp"""
    stem = stem.find('parameters')
    if data is None:
        data = {}
    for par in VASPPARAMETERS:
        path = './/*[@name="{}"]'.format(par)
        leaf = stem.xpath(path)[0]
        partype = leaf.attrib.get('type', 'float')
        if leaf.tag == 'i':
            data[par] = CAST[partype](leaf.text.strip())
        else:
            assert leaf.tag == 'v'
            data[par] = np.fromstring(leaf.text, sep=' ', dtype=partype)
    return data

def get_vasp_parameters_old(stem, data=None):
    """Get parameters for vasp"""
    stem = stem.find('parameters')
    if data is None:
        data = {}
    for key, path in VASPPAR_FLOATS.items():
        text = get_text_from_named_subsection(stem, path, key)
        data[key] = float(text.split()[0])
    for key, path in VASPPAR_INT.items():
        text = get_text_from_named_subsection(stem, path, key)
        data[key] = int(text.split()[0])
    return data

def get_calculated_energies(stem, data=None):
    """Return the energies from the calculation"""
    if data is None:
        data = {}
    stem = stem.find('calculation')
    for key, path in VASP_CALCULATED_ENERGIES.items():
        text = get_text_from_section(stem, path, key)
        data[key] = float(text.split()[0])
    return data

def get_kpoints(stem, data=None):
    """return the kpoints"""
    if data is None:
        data = {}
    stem = stem.find("kpoints")
    try:
        kmesh_type = stem.find("generation").attrib["param"]
    except AttributeError:
        kmesh_type = None
        division = None
    if kmesh_type is not None:
        if kmesh_type == "listgenerated":
            text = get_text_from_section(stem, 'generation/i', 'divisions')
            division = int(text.split()[0])
        else:
            text = get_text_from_section(stem, 'generation/v', 'divisions')
            division = np.fromstring(text, sep=' ', dtype=int).tolist()
    kpoints = []
    for i in stem.find("varray[@name='kpointlist']"):
        kpoints.append(np.fromstring(i.text, sep=' '))
    kpoints = np.array(kpoints)
    #
    data['kmesh_division'] = division
    data['kmesh_type'] = kmesh_type
    data['kpoints'] = kpoints
    #
    return data

def get_atomic_structure(stem, data=None):
    """Return the atomic structure info"""
    if data is None:
        data = {}
    # atoms
    atoms = []
    for elem in stem.find('./atominfo/array[@name="atoms"]/set'):
        atoms.append(elem.find('./c').text.strip())
    #
    # Changing the stem
    #
    stem = stem.find('./structure[@name="finalpos"]')
    #
    basis = np.zeros(shape=(3,3))
    for i, elem in enumerate(stem.find('./crystal/varray[@name="basis"]')):
        basis[i,:] = np.fromstring(elem.text, sep=' ')
    #
    positions = []
    for i, elem in enumerate(stem.find('./varray[@name="positions"]')):
        positions.append(np.fromstring(elem.text, sep=' '))
    # Atoms object
    data['atoms'] = atoms
    data['atoms.basis'] = basis
    atoms_ase = Atoms(atoms, pbc=True, cell=basis, scaled_positions=positions)
    data['atoms.positions'] = atoms_ase.get_positions()
    data['atoms.scaled_positions'] = positions
    data['atoms.ASE'] = atoms_ase
    #
    rec_basis = np.zeros(shape=(3,3))
    for i, elem in enumerate(stem.find('./crystal/varray[@name="rec_basis"]')):
        rec_basis[i,:] = np.fromstring(elem.text, sep=' ')
    data['atoms.reciprocal_basis'] = rec_basis
    #
    text = get_text_from_section(stem, 'crystal/i', 'volume')
    data['atoms.cell_volume'] = float(text)
    return data

def get_eigenvalues(stem, data=None):
    """Return a dictionary with eigenvalues and their occupancy"""
    if data is None:
        data = {}
        ispin = 1
    else:
        text = get_text_from_named_subsection(
                    stem.find('./calculation'),
                    VASPPAR_INT['ISPIN'][0], 'ISPIN')
        ispin = int(text.split()[0])
        # avoid reliance on the contents of data
        #ispin = data.get('ISPIN', 1)
    occupations = []
    eigenvalues = []
    for i in stem.find(".//set[@comment='spin 1']"):
        _eig = []
        _occ = []
        for k in i:
            e, o = k.text.split()
            _eig.append(float(e))
            _occ.append(float(o))
        eigenvalues.append(_eig)
        occupations.append(_occ)
    eigenvalues = np.array(eigenvalues).T
    occupations = np.array(occupations).T
    data['eigenvalues'] = eigenvalues
    data['occupations'] = occupations
    return data
    # what do we do if ispin != 1?

def parse_vasprun(xmlfile, data=None):
    """Parse vasprun.xml and return a dictionary w/ standardised keys
    """
    tree = etree.parse(xmlfile)

    if data is None:
        data = {}

    # system either is in incar, or is not available; no default
    data['SYSTEM'] = get_text_from_named_subsection(
                        tree.find('parameters'), 'general/i', 'SYSTEM')
    data.update(get_atomic_structure(tree))
    data.update(get_vasp_parameters(tree))
    data.update(get_calculated_energies(tree))
    data.update(get_kpoints(tree))
    data.update(get_eigenvalues(tree))
    return data

def kpathstr_to_xticks(path):
    """Split path into individual labels"""
    tick_labels = []
    combine_labels = False
    for i, char in enumerate(path):
        if char not in [',', '|', ' ']:
            if combine_labels:
                tick_labels[-1] = tick_labels[-1] + '|' + char
                combine_labels = False
                tick_labels.append('')
            else:
                tick_labels.append(char)
        else:
            combine_labels = True
    return tick_labels

def update_bands_xplotinfo(data, kpath):
    """Return a dictionary with info for the x-axis of bandstructure plot"""
    nkpts = len(data['kpoints'])
    if data['kmesh_type'] is None and data['kmesh_division'] is None:
        _kpt, x_val, x_tic = bandpath(kpath, data['atoms.basis'], npoints=nkpts)
        assert(np.allclose(_kpt, data['kpoints'], atol=1.e-5))
        assert(nkpts == len(x_val))
        data['bands.kpath'] = kpath
        data['bands.kspecial'] = kpath.replace(',','')
        data['bands.plot_xval'] = x_val
        data['bands.plot_xticks'] = x_tic
        data['bands.plot_xlabels'] = kpathstr_to_xticks(kpath)
