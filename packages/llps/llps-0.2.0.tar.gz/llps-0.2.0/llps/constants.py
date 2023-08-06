
REQUIRED_KEYS = set([
    'project_name',
    'project_description',
    'version',
    'sources',
    'files',
    'spec_version'
])
OPTIONAL_KEYS = set([
    'project_long_description',
    'author',
    'author_email',
    'project_website',
])
CHARACTERS = set('abcdefghijklmnopqrstuvwxyz_-')
RESERVED_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS | set([
    'path',
    'bucket_name',
    'endpoint_url',
    'remote_path',
    's3',
    'file',
    'hostname',
    'root_dir',
    'md5',
])
