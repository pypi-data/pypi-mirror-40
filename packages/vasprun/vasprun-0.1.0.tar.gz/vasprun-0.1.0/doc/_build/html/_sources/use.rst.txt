.. index:: use

.. _use:

Useage
======

Command line
------------

One can use the ``vasprun`` command from the prompt to create read the
``vasprun.xml`` and create ``vasprun.json`` file in the directory where the
``xml`` file is, and potentially plot a bandstructure.

Check options by

.. code:: bash

   vasprun -h


Plot bandstructure

.. code:: bash

   vasprun -x ./test/ref/noncollinear/bands/vasprun.xml -pb -k 'LGXU,KG'


The ``vasprun.json`` file has a very compact representation. If you
want to have a peak inside, make it human-readable (tab-formatting):

.. code:: bash

   python3 -mjson.tool path_to/vasprun.json


Library
-------

One can import the library and read ``vasprun.xml``
into a dictionary within a Python3 script or a program.


For example, to see all the keys that are currently parsed:

.. code:: python

   from vapsrun.io import parse_vasprun
   data = parse_vasprun('path_to/vasprun.xml')
   print(data.keys())

The above snipped would output:

.. code:: python

   dict_keys(['SYSTEM', 'atoms', 'atoms.basis', 'atoms.positions',
   'atoms.scaled_positions', 'atoms.ASE', 'atoms.reciprocal_basis',
   'atoms.cell_volume', 'ENMAX', 'ENAUG', 'EDIFF', 'EREF', 'NELECT', 'NBANDS',
   'ISPIN', 'LSORBIT', 'LNONCOLLINEAR', 'SAXIS', 'MAGMOM', 'IBRION', 'ISIF',
   'EDIFFG', 'GGA', 'e_fr_energy', 'e_wo_entrp', 'e_0_energy', 'efermi',
   'kmesh_division', 'kmesh_type', 'kpoints', 'eigenvalues', 'occupations'])



Adding keys
-----------

Additional keys may be parsed but these have to be added in
``VASPPARAMETERS`` dictionary in ``src/vasprun/io.py``.



