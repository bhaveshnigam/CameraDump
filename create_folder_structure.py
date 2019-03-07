import argparse

from utils import process_folder

parser = argparse.ArgumentParser(
    description="This script enables to create a dummy folder structure for "
                "backing up media content at a desired location"
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

args = parser.parse_args()

if __name__ == '__main__':
  process_folder(args.destination_folder, args.backup_folder_name)
