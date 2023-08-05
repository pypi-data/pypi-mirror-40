:orphan:

.. _installing_sdss_catl_utils_with_virtualenv:

******************************************************
Installing SDSS_Catl_Utils using a virtual environment
******************************************************

If you use `conda <https://www.continuum.io/downloads>`_ to manage
your python distribution and package dependencies, it is easy
to create a virtual environment that will authomatically
have compatible versions of the necessary depedencies required
by ``SDSS_Catl_Utils``. By installing into a virtual environment,
you will not change any of the packages that are already installed
system-wide on your machine. In the example below, we will use conda
to create a virtual environment with all the dependencies handled
automatically::

    conda create -n sdss_catl_utils_env astropy numpy scipy h5py requests cython python=3.6

In order to activate this environment::

    source activate sdss_catl_utils_env

Then install ``sdss_catl_utils`` into this environment::

    pip install sdss_catl_utils

Any additional packages you install in the ``sdss_catl_utils`` virtual
environment will not impact your system-wide environment. Whenever
you want to do science involving ``SDSS_Catl_Utils``, just activate
the environment and import the code. When you are done and wish to return
to your normal system environment::

    source deactivate
