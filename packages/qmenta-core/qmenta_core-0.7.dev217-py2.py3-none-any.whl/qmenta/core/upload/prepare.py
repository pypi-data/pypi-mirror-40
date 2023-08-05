import os
from zipfile import ZipFile, BadZipFile
from tempfile import TemporaryDirectory

from qmenta.core import errors
from qmenta.anon.auto import anonymise

"""
Functions to prepare date for being uploaded. This includes zipping of
directories and anonymising data. These functions are not thread-safe.
"""


class FileError(errors.Error):
    """
    When a problem occurs while handling files for uploading.
    """
    pass


def get_zipfile_size(filename):
    """
    Check that the file is a zip file larger than 0 bytes and
    return the file size.

    Parameters
    ----------
    filename : str
        The path to the zip file

    Returns
    -------
    The size of the zip file

    Raises
    ------
    FileError
        When the input file has the wrong file extension, or the file cannot
        be read or is empty.
    """
    assert filename
    fname = os.path.split(filename)[1]

    if fname.split('.')[-1] != 'zip':
        raise FileError('Not a zip file: {}'.format(filename))

    try:
        fsize = os.path.getsize(filename)
    except OSError:
        raise FileError('Cannot read file: '.format(filename))

    if fsize == 0:
        raise FileError("File is empty: '{}'".format(filename))

    return fsize


def get_input_filename(dirname):
    """
    Return a filename of a file that does not exist to store the
    zipped version of input data from a directory.

    Parameters
    ----------
    dirname : str
        The input directory

    Returns
    -------
    str
        The output filename, which will be of the form qm-dirname.zip
        or qm-dirame-anon-N.zip (with positive integer N) if any of the
        previously checked files exist.
    """
    dn = os.path.normpath(dirname)  # Strip trailing '/'
    parentname = os.path.dirname(dn)
    basename = os.path.basename(dn)

    new_name = os.path.join(parentname, 'qm-{}.zip'.format(basename))
    i = 0
    while os.path.exists(new_name):
        i = i + 1
        new_name = os.path.join(
            parentname, 'qm-{}-{}.zip'.format(basename, i)
        )
    return new_name


def get_anon_filename(filename):
    """
    Return a filename of a file that does not exist to store the
    anonymised version of the input file.

    Parameters
    ----------
    filename : str
        The input filename

    Returns
    -------
    str
        The output filename, which will be of the form qm-filename-anon.zip
        or qm-filename-anon-N.zip (with positive integer N) if any of the
        previously checked files exist. If filename already starts with 'qm-',
        then no additional prefix will be added.

    Raises
    ------
    FileError
        If the input filename extension is not 'zip'.
    """
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    split = os.path.splitext(basename)
    head = split[0]
    # Don't add a second 'qm-' prefix
    if head.startswith('qm-'):
        head = head[3:]
    ext = split[1]

    if ext != '.zip':
        raise FileError("Not a zip file: '{}'".format(filename))

    new_name = os.path.join(dirname, 'qm-{}-anon.zip'.format(head))
    i = 0
    while os.path.exists(new_name):
        i = i + 1
        new_name = os.path.join(
            dirname, 'qm-{}-anon-{}.zip'.format(head, i)
        )

    return new_name


def zip_directory(in_dir, out_file):
    """
    Create a zip file that contains the contents of the directory.

    Parameters
    ----------
    in_dir : str
        The input directory
    out_file : str
        The filename of the output zip file. This file should not exist yet.

    Raises
    ------
    FileError
        If the input directory does not exist or is not a directory, if the
        output file location is inside the input directory, or if there are
        problems reading/writing input/output.
    """
    # TODO TIM: Remove this when tested with App
    print('zip_directory({}, {})'.format(in_dir, out_file))
    if not os.path.exists(in_dir):
        raise FileError("No such file or directory: '{}'".format(in_dir))
    if not os.path.isdir(in_dir):
        raise FileError("Input is not a directory: '{}'".format(in_dir))

    if os.path.abspath(in_dir) in os.path.abspath(out_file):
        raise FileError(
            "Output file: '{}' is inside input directory: '{}'".format(
                out_file, in_dir
            )
        )

    def addToZip(zf, path, zippath):
        """
        From zipfile.py, where it is used for handling the '-c' command-line
        option
        """
        if os.path.isfile(path):
            zf.write(path, zippath)
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in os.listdir(path):
                addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        # else: ignore

    try:
        with ZipFile(out_file, mode='x') as zf:
            zippath = os.path.basename(in_dir)
            if not zippath:
                # last character of in_dir was '/'
                zippath = os.path.basename(os.path.dirname(in_dir))
            if zippath in ('', os.curdir, os.pardir):
                zippath = ''
            addToZip(zf, in_dir, zippath)
    except FileNotFoundError as e:
        raise FileError(e)
    except PermissionError as e:
        raise FileError(e)
    except FileExistsError as e:
        raise FileError(e)


def anonymise_zip(in_file, out_file):
    """
    Read the files of the input zip file, anonymise them, and write them
    to the output zip file.

    Parameters
    ----------
    in_file : str
        The name of the input zip file.
    out_file : str
        The name of the output zip file that will be created.

    Raises
    ------
    FileError
        When there are problems with the reading or writing of files, or when
        the input file is not a proper zip file.
    """
    try:
        with ZipFile(in_file) as in_zip, \
                ZipFile(out_file, mode='x') as out_zip, \
                TemporaryDirectory() as tmpdir:

            n = len(in_zip.infolist())
            # Do not use os.chdir here because that is not thread-safe.
            #   Instead, use absolute paths everywhere below when referring to
            #   files in the file system.
            #   Inside the zip-files we use relative paths.
            for i, zipinfo in enumerate(in_zip.infolist()):
                in_zip.extract(zipinfo, tmpdir)
                f_rel = zipinfo.filename
                f_abs = os.path.join(tmpdir, f_rel)
                if zipinfo.is_dir():
                    print('Adding directory {}'.format(f_rel))
                    out_zip.write(f_abs, f_rel)
                    os.rmdir(f_abs)
                else:
                    try:
                        print('Anonymising file {}/{} ({})'.format(
                            i+1, n, f_abs
                        ))
                        status = anonymise(f_abs)
                    except RuntimeError as e:
                        print('Failed to anonymise {}: {}'.format(f_abs, e))
                    else:
                        if not status["OK"]:
                            print("Unknown file format. Skipping {}".format(
                                f_abs
                            ))
                    out_zip.write(f_abs, f_rel)
                    # If the file was in a subdirectory, the directory will
                    #   still exist in the temporary directory. They will be
                    #   removed all together.
                    os.remove(f_abs)

    except OSError as e:
        # May be input or output file problems.
        raise FileError(e)
    except BadZipFile:
        raise FileError('Bad zip file: {}'.format(in_file))

    print('Finished anonymisation')
