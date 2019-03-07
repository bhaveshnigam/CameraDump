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
  raw_photo_folder = photo_folder.joinpath('RAW')
  raw_video_folder = video_folder.joinpath('RAW')
  create_dir(raw_photo_folder)
  create_dir(raw_video_folder)

  for device_name in SUPPORTED_DEVICE_NAMES:
    create_dir(raw_video_folder.joinpath(device_name))
    create_dir(raw_photo_folder.joinpath(device_name))


def process_folder(
    destination_folder, backup_folder_name,
    current_datetime=datetime.datetime.now()
):
  destination_folder = pathlib.Path(destination_folder)
  destination_folder = destination_folder.expanduser()

  if not destination_folder.exists():
    print ('The destination folder does not exist, attempting to create one')
    create_dir(destination_folder)

  # Create current year folder
  working_folder = destination_folder.joinpath(
      current_datetime.strftime('%Y')
  )
  create_dir(working_folder)

  # Create a folder based on the event/target folder name
  working_folder = working_folder.joinpath(backup_folder_name)
  create_dir(working_folder)

  # Create exports folder
  exports_folder = working_folder.joinpath('Exports')
  create_dir(exports_folder)
  exports_media_types = [
    'Instagram',
    'Full size',
    'Stylised'
  ]
  for media_type in exports_media_types:
    create_dir(exports_folder.joinpath(media_type))

  # Create a folder based on current date to keep this sorted.
  working_folder = working_folder.joinpath(
      current_datetime.strftime('%B %d')
  )
  create_dir(working_folder)


  # Create photo and video backup folders
  photo_folder = working_folder.joinpath('Photo')
  video_folder = working_folder.joinpath('Video')
  create_dir(photo_folder)
  create_dir(video_folder)
  create_device_folders(photo_folder, video_folder)