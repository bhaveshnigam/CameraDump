import datetime
import argparse
import pathlib
import time
from shutil import copy2

import magic
from tqdm import tqdm

from utils import process_folder, get_initials, dump_card

parser = argparse.ArgumentParser(
    description="This script enables dumping/copying of a memory card in an "
                "organized fashion"
)
parser.add_argument(
    "-s", "--source_memory_card",
    dest="source_memory_card",
    type=str,
    help="The Source memory card which needs to be copied/dumped "
         "Eg. ~/Downloads/",
    required=True
)
parser.add_argument(
    "-d", "--destination_folder",
    dest="destination_folder",
    type=str,
    help="The destination folder where the folder structure is "
         "meant to be created. Eg. ~/Downloads/",
    required=True
)
parser.add_argument(
    "-b", "--backup_folder",
    dest="backup_folder_name",
    type=str,
    help="The umbrella folder name under which the backup folders for each "
         "media device needs to be created",
    required=True
)

parser.add_argument(
    "-skip", "--skip_file_types",
    dest="skip_file_type",
    type=str,
    help="Any file types which are meant to be skipped",
    required=False,
    nargs='+'
)


args = parser.parse_args()


if __name__ == '__main__':
  dump_card(args.source_memory_card, args.destination_folder,
            args.skip_file_type, args.backup_folder_name)

