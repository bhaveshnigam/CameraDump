import datetime
import pathlib


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
    'ThirdPartySource'
]

def create_device_folders(photo_folder, video_folder):
  for device_name in SUPPORTED_DEVICE_NAMES:
    create_dir(photo_folder.joinpath(device_name))
    create_dir(video_folder.joinpath(device_name))


def process_folder(
    destination_folder, backup_folder_name,
    current_datetime=datetime.datetime.now()
):
  destination_folder = pathlib.Path(destination_folder)
  destination_folder = destination_folder.expanduser()

  if not destination_folder.exists():
    print ('The destination folder does not exist, attempting to create one')
    create_dir(destination_folder)

  # Create photo and video backup folders
  photo_folder = destination_folder.joinpath('Photo')
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
