#!/usr/bin/env python3

import argparse
from contextlib import contextmanager
import logging
import os
import tempfile
import urllib.request
import urllib.error
from zipfile import ZipFile


logger = logging.getLogger(__name__)

## CONSTANTS
# You can also manually download via `curl -L -O <url>`
# and provide the path to the zip file.

TECHVAR_ZIP_URL = 'https://dpel-assets.aswf.io/usd-alab/alab-techvars.v2.2.0.zip'
BAKED_PROCEDURALS_ZIP_URL = 'https://dpel-assets.aswf.io/usd-alab/alab-procedurals.v2.2.0.zip'
TEXTURE_PACK_ZIP_URL = 'https://aswf-dpel-assets.s3.amazonaws.com/usd-alab/alab-textures.v2.2.0.zip'
CAMERAS_ZIP_URL = 'https://dpel-assets.aswf.io/usd-alab/alab-cameras.v2.2.0.zip'


## UTILITY FUNCTIONS


@contextmanager
def _get_or_download(url, description, zip_file_path=None):
    """Utility function to either use provided zip file path or download from URL.
    
    Args:
        url (str): URL to download from if zip_file_path is None or empty string.
        description (str): Description of the file being downloaded, for logging.
        zip_file_path (str or None): If provided, path to zip file. If empty
            string, download from URL. If None, raise exception.
            
    Returns:
        str: Path to zip file, either provided or downloaded.
    """
    if zip_file_path:
        if not os.path.isfile(zip_file_path):
            raise Exception(f'Provided {description} zip file path does not exist: {zip_file_path}')
        logger.info(f'Using provided {description} zip file: {zip_file_path}')
        yield zip_file_path
    else:
        downloaded_tmp_zip = _download(url, description)
        try:  # delete temp file after use, even in exceptions
            yield downloaded_tmp_zip
        finally:
            os.remove(downloaded_tmp_zip)



def _download(url, description):
    """Utility function to download a file from a URL to a temporary file.

    Args:
        url (str): URL to download from.
        description (str): Description of the file being downloaded, for logging.

    Returns:
        str: Path to the temporary file containing the downloaded content.
    """
    logger.info(f'Downloading {description} from {url}...')

    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() != 200:
                raise Exception(f'Failed to download {description} from {url}. Status code: {response.getcode()}')
            
            tmpfile_path = tempfile.NamedTemporaryFile(delete=False).name
            with open(tmpfile_path, 'wb') as tmpfile:
                tmpfile.write(response.read())
    except urllib.error.URLError as e:
        raise Exception(f'Failed to download {description} from {url}: {e}')

    return tmpfile_path


def _unzip(zip_file_path, target_folder, zip_file_folder_name):
    """Utility function to unzip zip file into ALab folder.
    
    Args:
        zip_file_path (str): Path to the zip file.
        target_folder (str): Target folder to unzip into.
        zip_file_folder_name (str): Top-level folder name inside the zip file to extract.
    """

    # assert output folder exists
    os.makedirs(target_folder, exist_ok=True)

    with ZipFile(zip_file_path, 'r') as zip_file:
        for member in zip_file.namelist():
            if (zip_file_folder_name + os.sep) not in member:
                continue

            relative_path = member.split(zip_file_folder_name + os.sep, 1)[1]
            if relative_path:
                target_path = os.path.join(target_folder, relative_path)
                
                if member.endswith('/'):  # a directory
                    os.makedirs(target_path, exist_ok=True)
                else:  # a file
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(zip_file.read(member))
                    logger.debug(f'{member} >> {target_path}')


def _parse_args():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Build script for assembling ALab packages.')

    default_args = {
        'metavar': 'ZIP_FILE',
        'nargs': '?',  # allow optional .zip file
        'const': '',  # indicate download default from URL
        'default': None,  # indicate no action
    }

    parser.add_argument(
        '--output', '-o',
        help='Output folder for assembled package (defaults to working directory)',
        default=os.getcwd()
    )

    group = parser.add_argument_group('Install Options', 'Options to install asset packages into ALab repository. Provide a zip file path, or use without argument to download default online package.')
    group.add_argument(
        '--all',
        action='store_true',
        help='Install all asset packages. Individual flags can still be overridden to provide .zip files.'
    )
    group.add_argument(
        '--techvar',
        help='Install Techvar assets',
        **default_args,
    )
    group.add_argument(
        '--baked_procedurals',
        help='Install baked procedurals',
        **default_args,
    )
    group.add_argument(
        '--texture_pack',
        help='Install texture pack',
        **default_args,
    )
    group.add_argument(
        '--cameras',
        help='Install camera assets',
        **default_args,
    )

    args = parser.parse_args()
    logger.debug(f'Parsed arguments: {args}')

    if not os.path.isdir(args.output):
        parser.error(f'Output folder does not exist: {args.output}')

    # if --all is set, set all to default (download)
    # but let user override individual options with a .zip file
    if args.all:
        args.techvar = args.techvar or ''
        args.baked_procedurals = args.baked_procedurals or ''
        args.texture_pack = args.texture_pack or ''
        args.cameras = args.cameras or ''

    if not args.all and not any(arg is not None for arg in [args.techvar, args.baked_procedurals, args.texture_pack, args.cameras]):
        parser.error(
            'No action requested. '
            'Add --all to download all packages, or use individual flags: '
            '--techvar, --baked_procedurals, --texture_pack, --cameras'
        )

    return args


## MAIN FUNCTIONS


def install_techvar(zip_file, output_folder):
    logger.info('Installing Techvar assets...')
    fragment_folder = os.path.join(output_folder, 'ALab', 'fragment')
    _unzip(zip_file, fragment_folder, 'fragment')
    logger.info('Techvar assets installed successfully.')


def install_baked_procedurals(zip_file, output_folder):
    logger.info('Installing baked procedural assets...')
    fragment_folder = os.path.join(output_folder, 'ALab', 'baked_procedurals')
    _unzip(zip_file, fragment_folder, 'baked_procedurals')
    logger.info('Baked procedurals installed successfully.')


def install_texture_pack(zip_file, output_folder):
    logger.info('Installing texture pack...')
    fragment_folder = os.path.join(output_folder, 'ALab', 'fragment')
    _unzip(zip_file, fragment_folder, 'fragment')
    logger.info('Texture pack installed successfully.')


def install_cameras(zip_file, output_folder):
    logger.info('Installing camera asset package...')
    fragment_folder = os.path.join(output_folder, 'ALab')
    _unzip(zip_file, fragment_folder, 'trailer_cameras')
    logger.info('Cameras installed successfully.')


def install_all(output_folder, techvar=None, baked_procedurals=None, texture_pack=None, cameras=None):
    """Main install function to handle all requested packages.
    Args:
        
        output_folder (str): Output folder for the assembled package,
            assumed to be a local clone of the ALab GitHub repository.
        techvar (str or None): If provided, path to Techvar .zip file. If
            empty string, download default Techvar assets. If None, skip installation.
        baked_procedurals (str or None): If provided, path to Baked Procedurals
            .zip file. If empty string, download default baked procedurals assets.  If None, skip installation.
        texture_pack (str or None): If provided, path to texture pack .zip file. If
            empty string, download default Texture Pack. If None, skip installation.
        cameras (str or None): If provided, path to cameras .zip file. If
            empty string, download default camera assets. If None, skip installation.
    """

    if techvar is not None:
        with _get_or_download(TECHVAR_ZIP_URL, 'Techvar assets', techvar) as zip_file:
            install_techvar(zip_file, output_folder)

    if baked_procedurals is not None:
        with _get_or_download(BAKED_PROCEDURALS_ZIP_URL, 'baked procedurals', baked_procedurals) as zip_file:
            install_baked_procedurals(zip_file, output_folder)

    if texture_pack is not None:
        with _get_or_download(TEXTURE_PACK_ZIP_URL, 'texture pack', texture_pack) as zip_file:
            install_texture_pack(zip_file, output_folder)

    if cameras is not None:
        with _get_or_download(CAMERAS_ZIP_URL, 'cameras', cameras) as zip_file:
            install_cameras(zip_file, output_folder)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    args = _parse_args()
    install_all(
        output_folder=args.output,
        techvar=args.techvar,
        baked_procedurals=args.baked_procedurals,
        texture_pack=args.texture_pack,
        cameras=args.cameras
    )