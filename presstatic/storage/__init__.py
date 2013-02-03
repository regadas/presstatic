# -*- coding: utf-8 -*-

import os
import simplejson as json
from glob import iglob

from clint.textui import colored, puts, indent

from presstatic.utils import hashfile


class Manifest(object):

    filename = 'manifest.json'

    @classmethod
    def read(self, path):
        manifest_path = os.path.join(path, self.filename)
        if not os.path.exists(manifest_path):
            try:
                open(manifest_path, "w").close()
            except IOError:
                pass
        with open(manifest_path, 'r') as f:
            try:
                return json.load(f)
            except:
                return {}

    @classmethod
    def write(self, path, data):
        manifest_path = os.path.join(path, self.filename)
        with open(manifest_path, 'w') as f:
            json.dump(data, f, indent=2)


class Storage(object):

    def _walk(self, base_path, inner_dir=''):
        for path in iglob(base_path):
            basename = os.path.basename(path)
            if os.path.isdir(path):
                for f in self._walk(base_path=os.path.join(path, '*'),
                                    inner_dir=os.path.join(inner_dir, basename)):
                    yield f
            else:
                yield self.storage_intent(path, os.path.join(inner_dir, basename))

    def store(self, base_path):
        if os.path.isdir(base_path):
            path = os.path.join(base_path, '*')
            manifest_path = base_path
        else:
            manifest_path = os.path.dirname(base_path)
            path = base_path

        manifest_data = Manifest.read(manifest_path)
        for f in self._walk(path):
            if Manifest.filename in f.from_path:
                continue

            with indent(4, quote='>>'):
                if f.hash != manifest_data.get(f.to_path, None):
                    manifest_data[f.to_path] = f.hash
                    puts(colored.yellow("uploading ... {path}".format(path=f.to_path)))
                    f.store()
                else:
                    puts(colored.green("{path} not changed! ... skipping".format(path=f.to_path)))

        Manifest.write(manifest_path, manifest_data)


class FileStorageIntent(object):

    hash_algorithm = 'md5'

    def __init__(self, from_path, to_path):
        self.from_path = from_path
        self.to_path = to_path
        self.hash = hashfile(from_path, self.hash_algorithm)

    def store(self):
        raise NotImplementedError()
