#!/usr/bin/python
#

import os
import sys
import datetime
import json
import requests
import argparse

home_path = os.environ.get("HOME_PATH","/tmp")
keys_to_clean = {'version', 'versionInfo', 'fetch'}
backup_file_path = '%s' % (
  datetime.datetime.now().strftime("%Y%m%d-%H%M")
)
backup_file_names = {
  'raw'       : 'groups_raw',
  'processed' : 'groups'
}
marathon_api_call = 'v2/groups'
args=''


def remove_keys(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_keys(v) for v in d]
    return {k: remove_keys(v) for k, v in d.items()
            if k not in keys_to_clean}

def split_by(d, key_word):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [split_by(v, key_word) for v in d]
    for k, v in d.items():
        if key_word in k:
            save_keys(d,key_word)
    return {k: split_by(v, key_word) for k, v in d.items()}

def save_keys(json_data, key_word):
    # For each key_word selected generate a file.
    for item in json_data[key_word]:
       save_file('%s/%s' % (key_word, item['id']), item )

def save_file(backup_file_name, json_data):
    # Save a json structure into file.

    full_backup_file_path = os.path.dirname(os.path.abspath('%s/%s/%s/%s' % (home_path, args.environment, backup_file_path, backup_file_name)))
    backup_file_name = os.path.basename(backup_file_name)

    if not os.path.exists(full_backup_file_path):
        os.makedirs(full_backup_file_path)
    try:
        with open( os.path.abspath("%s/%s.json" % (full_backup_file_path, backup_file_name)), "wb") as file:
            file.write(json.dumps(json_data, indent=2))
    except:
        print ('ERROR: Imposible save %s file.' % (backup_file_name))
        sys.exit(2)
    else:
        print ('INFO: File %s saved.' % (backup_file_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Marathon Groups Backup.')
    parser.add_argument('--environment', required=True,
                       help='Environment name. (Prod, QA, Lab, ...)')
    parser.add_argument('--url', required=True,
                       help='Marathon url. (http://marathon.xxx.xxx:8080)')

    args = parser.parse_args()

    url = '%s/%s' % (args.url, marathon_api_call)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print ('ERROR: Status: %s on %s' % (r.status_code, url))
        sys.exit(2)

    json_raw = r.json()

    processed = remove_keys(json_raw)
    save_file(backup_file_names['raw'], json_raw)
    save_file(backup_file_names['processed'], processed)
    split_by(processed,'apps')
    split_by(processed,'groups')
