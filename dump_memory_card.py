import datetime
import argparse
import pathlib
import time
import magic
from tqdm import tqdm

from utils import process_folder

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


DEVICE_TYPE_FOLDER_MAP = {
  'D7200': 'D7200',
  'iPhone': 'iPhoneXS',
  'Mavic': 'MavicAir',
  'SJCAM': 'SJCam'
}

def dump_card(source_card_path, destination_path, backup_folder_name,
              skip_file_types):

  # Argparser can provide this argument as None
  if not skip_file_types:
    skip_file_types = []

  source_card = pathlib.Path(source_card_path)

  processed_dates = []
  for file in tqdm(list(source_card.glob('**/*'))):
    if file.is_file():
      if ((file.suffix in skip_file_types) or
          (file.suffix.replace('.', '') in skip_file_types)):
        continue

      metadata_string = magic.from_file(str(file))

      media_type = ''
      if 'movie' in metadata_string.lower():
        media_type = 'Video'
      elif 'image' in metadata_string.lower():
        media_type = 'Photo'

      if not media_type:
        continue

      time_obj = time.localtime(file.stat().st_ctime)
      created_date = datetime.datetime(
          year=time_obj.tm_year, month=time_obj.tm_mon, day=time_obj.tm_mday,
          hour=time_obj.tm_hour, minute=time_obj.tm_min, second=time_obj.tm_sec
      )
      if created_date not in processed_dates:
        processed_dates.append(created_date)
        process_folder(destination_path, backup_folder_name, created_date)

      source_device_type = 'ThirdPartySource'
      for device_uid in DEVICE_TYPE_FOLDER_MAP.keys():
        if device_uid.lower() in metadata_string.lower():
          source_device_type = DEVICE_TYPE_FOLDER_MAP[device_uid]

      target_file_path = pathlib.Path(
          destination_path
      ).joinpath(
          '%s/%s/%s/%s/RAW/%s/%s%s' % (
              created_date.year, backup_folder_name,
              created_date.strftime('%B %d'), media_type, source_device_type,
              file.stem, file.suffix,
          )
      )
      target_file_path.write_bytes(file.read_bytes())


if __name__ == '__main__':
  dump_card(args.source_memory_card, args.destination_folder,
            args.backup_folder_name, args.skip_file_type)
