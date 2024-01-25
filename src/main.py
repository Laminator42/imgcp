import argparse
import itertools
import os
from datetime import datetime
from pathlib import Path
from shutil import copy

from log import logger
from PIL import ExifTags, Image
from timing import timed
from tqdm import tqdm


@timed
def get_date_taken(path: str) -> datetime:
    try:
        with Image.open(path) as img:
            exif = {ExifTags.TAGS.get(tag): value for tag, value in img.getexif().items() if tag in ExifTags.TAGS}
            if 'DateTime' in exif:
                return datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        logger.error(f'Error reading EXIF for {path}: {e}')

    # Fallback to file system creatopn date if EXIF is unavailable
    try:
        return datetime.fromtimestamp(os.path.getctime(path))
    except Exception as e:
        logger.error(f'Error reading file system date for {path}: {e}')

    return None


@timed
def copy_image(source: Path, destination: Path):
    # Ensure destination exists
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_file():
        copy(source, destination)


@timed
def main(source: Path, destination: Path):
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
    image_extensions += [ext.upper() for ext in image_extensions]
    files = itertools.chain.from_iterable(source.glob(f'*.{extension}') for extension in image_extensions)
    for source_fpath in tqdm(files, desc='Copying files'):
        image_taken_at = get_date_taken(source_fpath)
        if image_taken_at:
            destination_fpath = destination / f'{image_taken_at.strftime(args.format)}{source_fpath.suffix.lower()}'
            logger.debug(f'Copying {source_fpath} --> {destination_fpath}')
            copy_image(source=source_fpath, destination=destination_fpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TBD')
    parser.add_argument('source', type=Path, help='TBD')
    parser.add_argument('destination', type=Path, help='TBD')
    parser.add_argument('-f', '--format', type=str, default='%Y-%m-%d %H:%M:%S', help='TBD')
    args = parser.parse_args()

    main(source=args.source, destination=args.destination)
