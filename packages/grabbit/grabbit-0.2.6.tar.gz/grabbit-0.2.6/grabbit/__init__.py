from .core import File, Entity, Layout, Tag, Domain, merge_layouts
from .extensions import (replace_entities, build_path, write_contents_to_file)

__all__ = [
    'File',
    'Entity',
    'Layout',
    'Tag',
    'Domain',
    'replace_entities',
    'build_path',
    'write_contents_to_file',
    'merge_layouts'
]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
