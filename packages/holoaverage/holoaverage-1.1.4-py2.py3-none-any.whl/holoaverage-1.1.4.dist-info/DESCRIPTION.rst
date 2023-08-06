
Holoaverage is a Python script for the reconstruction and averaging of series of off-axis electron holograms, 
typically recorded in transmission electron holograms. The averaging is performed iteratively, such that instabilities 
of the microscope, like specimen and biprism drifts, can be tracked and corrected between consecutive exposures.

The averaging process is speed up, when also the `pyFFTW <http://hgomersall.github.com/pyFFTW/>`_ package is installed. 
However, is not a requirement for holoaverage and thus not automatically installed by ``pip``.

The source for holoaverage can be found on `GitHub <https://github.com/niermann/holoaverage>`_. The documentation can
be found on `ReadTheDocs <https://holoaverage.readthedocs.io>`_.


