import datetime
import os
import pathlib
import time
from shutil import copy2

import magic
from tqdm import tqdm
import exifread


def create_dir(expanded_path):
  if not isinstance(expanded_path, pathlib.Path):
    path = pathlib.Path(expanded_path)
  else:
    path = expanded_path

  try:
    path.mkdir(exist_ok=True)
  except FileNotFoundError as err:
    print('Unable to create a directory, error: %s' % err)


SUPPORTED_DEVICE_NAMES = [
    'D7200',
    'SJCam',
    'MavicAir',
    'iPhoneXS',
    'ThirdPartySource',
    'A6400'
]


DEVICE_TYPE_FOLDER_MAP = {
  'D7200': 'D7200',
  'Nikon D7200': 'D7200',
  'Nikon': 'D7200',
  'iPhone': 'iPhoneXS',
  'Mavic': 'MavicAir',
  'SJCAM': 'SJCam',
  'MavicAir': 'MavicAir',
  'DJI': 'MavicAir',
  'Sony': 'A6400',
  'Sony A6400': 'A6400',
  'A6400': 'A6400'
}


universal_skip_file_type = [
  'THM', '.db'
]


def create_device_folders(photo_folder, video_folder):
  for device_name in SUPPORTED_DEVICE_NAMES:
    create_dir(photo_folder.joinpath(device_name))
    create_dir(video_folder.joinpath(device_name))


def create_premiere_folders(destination_path, backup_folder_name):
  destination_folder = pathlib.Path(destination_path).expanduser()

  if not destination_folder.exists():
    print ('The destination folder does not exist, attempting to create one')
    create_dir(destination_folder)
  video_folder = destination_folder.joinpath('Video')
  create_dir(video_folder)

  for folder in ['Premiere Projects', backup_folder_name]:
    video_folder = video_folder.joinpath(folder)
    create_dir(video_folder)

  create_dir(video_folder.joinpath('AE'))
  create_dir(video_folder.joinpath('MX'))
  raw_file_folder = video_folder.joinpath('RAW')
  create_dir(raw_file_folder)

  for device_name in SUPPORTED_DEVICE_NAMES:
    create_dir(raw_file_folder.joinpath(device_name))

  create_dir(video_folder.joinpath('SFX'))
  create_dir(video_folder.joinpath('ASSETS'))
  create_dir(video_folder.joinpath('EXPORTS'))
  create_dir(video_folder.joinpath('PROJECT'))
  return raw_file_folder


def process_folder(
    destination_folder, backup_folder_name,
    current_datetime=datetime.datetime.now(),
    video_folder=None
):
  destination_folder = pathlib.Path(destination_folder)
  destination_folder = destination_folder.expanduser()

  if not destination_folder.exists():
    print ('The destination folder does not exist, attempting to create one')
    create_dir(destination_folder)

  # Create photo and video backup folders
  photo_folder = destination_folder.joinpath('Photo')

  if not video_folder:
    video_folder = destination_folder.joinpath('Video')

  create_dir(photo_folder)
  create_dir(video_folder)

  photo_working_folder = None
  video_working_folder = None
  for index, folder in enumerate([photo_folder, video_folder]):
    # Create exports folder
    exports_folder = folder.joinpath('Exports')
    create_dir(exports_folder)
    exports_media_types = [
      'Instagram',
      'Full size',
      'Stylised'
    ]
    for media_type in exports_media_types:
      create_dir(exports_folder.joinpath(media_type))

    raw_folder = folder.joinpath('RAW')
    create_dir(raw_folder)

    raw_folder = raw_folder.joinpath(current_datetime.strftime('%Y'))
    create_dir(raw_folder)

    if index == 0:
      photo_working_folder = raw_folder
    elif index == 1:
      video_working_folder = raw_folder

  # Create a folder based on the event/target folder name
  photo_working_folder = photo_working_folder.joinpath(backup_folder_name)
  create_dir(photo_working_folder)
  # Create a folder based on the event/target folder name
  video_working_folder = video_working_folder.joinpath(backup_folder_name)
  create_dir(video_working_folder)

  create_device_folders(photo_working_folder, video_working_folder)


def get_initials(name, join_by=''):
  if len(name) == 0:
    return ''
  initials = [i[0].upper() for i in name.split()]
  return join_by.join(initials)


def dump_card(
    source_card_path, destination_path, skip_file_types, backup_folder_name,
    qt_application=None, progress_bar=None, do_create_premiere_folders=False
):

  # Argparser can provide this argument as None
  if not skip_file_types:
    skip_file_types = []

  skip_file_types.extend(universal_skip_file_type)

  source_card = pathlib.Path(source_card_path)

  processed_dates = []
  all_files = list(source_card.glob('**/*'))
  total_len = len(all_files)
  for index, file in enumerate(tqdm(all_files, unit='file')):
    if (qt_application is not None and
        progress_bar is not  None):
      percent_done = int(((index+1)/total_len) * 100)
      progress_bar.setProperty('value', percent_done)
      qt_application.processEvents()

    if file.is_file():
      if ((file.suffix in skip_file_types) or
          (file.suffix.replace('.', '') in skip_file_types)):
        continue

      metadata_string = magic.from_file(str(file))

      media_type = ''
      if (('movie' in metadata_string.lower()) or
          ('mp4' in metadata_string.lower()) or
          ('video' in metadata_string.lower())
      ):
        media_type = 'Video'
      elif 'image' in metadata_string.lower():
        media_type = 'Photo'

      if not media_type:
        continue

      time_obj = time.localtime(file.stat().st_mtime)
      created_date = datetime.datetime(
          year=time_obj.tm_year, month=time_obj.tm_mon, day=time_obj.tm_mday,
          hour=time_obj.tm_hour, minute=time_obj.tm_min, second=time_obj.tm_sec
      )

      video_folder = None
      if do_create_premiere_folders:
        video_folder = create_premiere_folders(destination_path, backup_folder_name)

      if created_date not in processed_dates:
        processed_dates.append(created_date)
        process_folder(destination_path, backup_folder_name, created_date, video_folder)

      source_device_type = 'ThirdPartySource'
      device_name_tokens = [i for i in str(file).split('/') if i]
      for device_uid in DEVICE_TYPE_FOLDER_MAP.keys():
        if device_uid.lower() in metadata_string.lower():
          source_device_type = DEVICE_TYPE_FOLDER_MAP[device_uid]
          break
        tags = exifread.process_file(open(str(file), 'rb'))
        if device_uid in str(tags):
          source_device_type = DEVICE_TYPE_FOLDER_MAP[device_uid]
          break

        for i in device_name_tokens:
          if i.lower() in device_uid.lower():
            source_device_type = DEVICE_TYPE_FOLDER_MAP[device_uid]
            break

      folder_initials = get_initials(backup_folder_name)
      target_file_path = pathlib.Path(
          destination_path
      ).joinpath(
          '%s/RAW/%s/%s/%s/%s-%s%s' % (
              media_type, created_date.year, backup_folder_name,
              source_device_type, folder_initials, file.stem, file.suffix,
          )
      )
      if media_type == 'Video' and do_create_premiere_folders:
        target_file_path = pathlib.Path(
            video_folder
        ).joinpath(
            '%s/%s-%s%s' % (
              source_device_type, folder_initials, file.stem, file.suffix,
          )
        )
      copy2(str(file), str(target_file_path))
  # clear_empty_folders('%s/%s' % (destination_path, 'Photo'))
  # clear_empty_folders('%s/%s' % (destination_path, 'Video'))
  return True


def clear_empty_folders(folder_path):
  folder_path = pathlib.Path(folder_path)
  for path in folder_path.expanduser().iterdir():
    if '.DS_Store' in str(path):
      os.remove(str(path))
      continue
    if path.is_dir():
      if list(path.iterdir()):
        clear_empty_folders(str(path))
      try:
        path.rmdir()
      except OSError:
        pass


MAX_DEPTH_LEVEL = 7

def get_child_folder_names(target_path, recursion_level=0):
  if not target_path:
    return []

  if recursion_level > MAX_DEPTH_LEVEL:
    return []

  child_folders = []
  for path in pathlib.Path(target_path).expanduser().iterdir():
    if not path.is_dir():
      continue
    path_name = path.name
    if path_name.startswith('__') and path_name.endswith('__'):
      continue
    if path_name.startswith('.'):
      continue
    if path_name.endswith('lrdata'):
      continue
    child_folders.append(path.name)

    try:
      if list(path.iterdir()):
        child_paths = get_child_folder_names(str(path),
                                             recursion_level=recursion_level+1)
        child_folders.extend(child_paths)
    except PermissionError:
      continue

  return list(set(child_folders))
