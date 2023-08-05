.. _working_with_catalogues:

***********************************************************
Downloading and caching Galaxy- and Group-galaxy catalogues
***********************************************************

This section of the documentation describes how to get up
and running with the galaxy and group-galaxy catalogues
provided by ``SDSS_Catl_Utils``. To see if ``SDSS_Catl_Utils``
provides the catalogues that you need, check Calderon et al. (2018).

``SDSS_Catl_Utils`` provides a handful of homogeneously processed
galaxy and group galaxy catalogues and associated group membership
data. These catalogues have been prepared into a standard form,
and so once they are downloaded they will be directly added to your
cache and can immediately be used for your science applications.

The class responsible for downloading and caching these catalogues
is `~sdss_catl_utils.models.catl_models.DownloadManager`.