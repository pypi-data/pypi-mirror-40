import os
import yaml

from banal import is_listish, is_mapping, ensure_list


def load_collection(api, foreign_id, config):
    collections = api.filter_collections(filters=[('foreign_id', foreign_id)])
    for collection in collections:
        casefile = collection.get('casefile')
        collection['casefile'] = config.get('casefile', casefile)
        languages = config.get('languages', [])
        if len(languages):
            collection['languages'] = languages
        api.update_collection(collection.get('id'), collection)
        return collection.get('id')

    data = {
        'foreign_id': foreign_id,
        'label': config.get('label', foreign_id),
        'casefile': config.get('casefile', False),
        'category': config.get('category', 'other'),
        'languages': config.get('languages', []),
        'summary': config.get('summary', ''),
    }
    collection = api.create_collection(data)
    return collection.get('id')


def load_config_file(file_path):
    """Load a YAML (or JSON) bulk load mapping file."""
    file_path = os.path.abspath(file_path)
    with open(file_path, 'r') as fh:
        data = yaml.load(fh) or {}
    return resolve_includes(file_path, data)


def resolve_includes(file_path, data):
    """Handle include statements in the graph configuration file.

    This allows the YAML graph configuration to be broken into
    multiple smaller fragments that are easier to maintain."""
    if is_listish(data):
        return [resolve_includes(file_path, i) for i in data]
    if is_mapping(data):
        include_paths = ensure_list(data.pop('include', []))
        for include_path in include_paths:
            dir_prefix = os.path.dirname(file_path)
            include_path = os.path.join(dir_prefix, include_path)
            data.update(load_config_file(include_path))
        for key, value in data.items():
            data[key] = resolve_includes(file_path, value)
    return data
