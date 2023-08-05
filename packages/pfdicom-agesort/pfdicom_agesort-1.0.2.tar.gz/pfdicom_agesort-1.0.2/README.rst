pfdicom_agesort
==================

.. image:: https://badge.fury.io/py/pfdicom_agesort.svg
    :target: https://badge.fury.io/py/pfdicom_agesort

.. image:: https://travis-ci.org/FNNDSC/pfdicom_agesort.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdicom_agesort

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pfdicom_agesort

.. contents:: Table of Contents


Quick Overview
--------------

-  ``pfdicom_agesort`` processes ChRIS conformant PACS pull trees and reorders
    content according to an explicit <year>/<month>/<exanmple> structure.

Overview
--------

``pfdicom_agesort`` repacks a ChRIS-default tree of MRI/DICOM data to an explicit age-reflecting organization. The program performs a mulit-pass loop over the file tree space as defined in the [--stage <stage>] flag below.

NOTE:

* ``pfdicom_agesort`` is dervied from ``pfdicom_tagExtract``. Please consult the documentation for ``pfdicom_tagExtract`` for additional information.

Installation
------------

Dependencies
~~~~~~~~~~~~

The following dependencies are installed on your host system/python3 virtual env (they will also be automatically installed if pulled from pypi):

-  ``pfmisc`` (various misc modules and classes for the pf* family of objects)
-  ``pftree`` (create a dictionary representation of a filesystem hierarchy)
-  ``pfdicom`` (handle underlying DICOM file reading)

Using ``PyPI``
~~~~~~~~~~~~~~

The best method of installing this script and all of its dependencies is
by fetching it from PyPI

.. code:: bash

        pip3 install pfdicom_agesort

Command line arguments
----------------------

.. code:: html

        -I|--inputDir <inputDir>
        Input DICOM directory to examine. By default, the first file in this
        directory is examined for its tag information. There is an implicit
        assumption that each <inputDir> contains a single DICOM series.

        [-e|--extension <DICOMextension>]
        An optional extension to filter the DICOM files of interest from the 
        <inputDir>.

        -O|--outputDir <outputDir>
        The output root directory that will contain a tree structure identical
        to the input directory, and each "leaf" node will contain the analysis
        results.

        In the case of `pfdicom_agesort`, this <outputDir> is the root of the
        age sorted tree.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as 
        'anon' or 'preview'. 

        This is a formatting spec, so 

            --outputLeafDir 'preview-%s'

        where %s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [-F|--tagFile <tagFile>]
        Read the tags, one-per-line in <tagFile>, and print the
        corresponding tag information in the DICOM <inputFile>.

        [-T|--tagList <tagList>]
        Read the list of comma-separated tags in <tagList>, and print the
        corresponding tag information parsed from the DICOM <inputFile>.

        [-S|--symlinkDCMdata]
        If true/specified, perform a symlink of the original DICOM data to
        the final output directory tree. If false, a copy of the original
        DICOM data is performed.

        [-D|--doNotCleanUp]
        If true, do not cleanup the original tag data tree created when
        analysing the original DICOM tree structure.

        [-m|--image <[<index>:]imageFile>]
        If specified, also convert the <inputFile> to <imageFile>. If the
        name is preceded by an index and colon, then convert this indexed 
        file in the particular <inputDir>.

        [-s|--imageScale <factor>[:<interpolation>]]
        If an image conversion is specified, this flag will scale the image
        by <factor> and use an interpolation <order>. This is useful in 
        increasing the size of images for the html output.

        Note that certain interpolation choices can result in a significant
        slowdown!

            interpolation order:
            
            'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
            'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
            'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'

        -o|--outputFileStem <outputFileStem>
        The output file stem to store data. This should *not* have a file
        extension, or rather, any "." in the name are considered part of 
        the stem and are *not* considered extensions.

        [-t|--outputFileType <outputFileType>]
        A comma specified list of output types. These can be:

            o <type>    <ext>       <desc>
            o raw       -raw.txt    the raw internal dcm structure to string
            o json      .json       a json representation
            o html      .html       an html representation with optional image
            o dict      -dict.txt   a python dictionary
            o col       -col.txt    a two-column text representation (tab sep)
            o csv       .csv        a csv representation

        Note that if not specified, a default type of 'raw' is assigned.

        [--stage <stage>]
        Stage to execute -- mostly for debugging purposes and useful if running a 
        particular stage repeatedly.

        [--infoJSON <infoJSONfile>]
        The name of the study JSON file. 

        Defaults to 'info.json'.

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--json]
        If specified, output a JSON dump of final return.

        [--followLinks]
        If specified, follow symbolic links.

        [-v|--verbosity <level>]
        Set the app verbosity level. 

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write
            
Examples
--------

Process a ChRIS tree containing DICOM:

.. code:: bash

        pfdicom_agesort                                             \\
                    -I /neuro/users/chris/data/mrn                  \\
                    -O /neuro/users/chris/data/age                  \\
                    --threads 0 --printElapsedTime                  \\
                    -e dcm                                          \\
                    -o '%_md5|6_PatientID-%PatientAge'              \\
                    -m 'm:%_nospc|-_ProtocolName.jpg'               \\
                    -s 3:none                                       \\
                    --useIndexhtml                                  \\
                    -t raw,json,html,dict,col,csv                   \\
                    --followLinks                                   \\
                    --symlinkDCMdata                                \\
                    -v 3                                            \\
                    --threads 0

which will reorganize the file trees as shown, printing the final elapsed processing time.
