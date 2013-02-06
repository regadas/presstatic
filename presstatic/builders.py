# -*- coding: utf-8 -*-

import os
import shutil

from jinja2 import Environment, FileSystemLoader
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension
from webassets.loaders import YAMLLoader


class TemplateBuilder(object):

    def __init__(self, path, output,
                 static_path='static', static_url='static',
                 asset_config='config.yml'):
        self.path = path
        self.output = output
        self.output_path = os.path.join(path, output)
        self.env = Environment(loader=FileSystemLoader(path),
                               extensions=[AssetsExtension])

        try:
            config_path = os.path.join(self.path, asset_config)
            asset_config = YAMLLoader(config_path)
            self.assets_env = asset_config.load_environment()
        except IOError:
            self.assets_env = AssetsEnvironment()

        if 'directory' not in self.assets_env.config:
            self.assets_env.directory = self.output_path

        if 'url' not in self.assets_env.config:
            self.assets_env.url = static_url

        self.assets_env.load_path = [self.path]
        self.env.assets_environment = self.assets_env

    def build_template(self, template, context={}):
        tmpl = self.env.get_template(template)
        dump_path = os.path.join(self.output_path, template)
        tmpl.stream().dump(dump_path)

    def list_files(self):
        templates, other = set(), set()

        if getattr(self.assets_env, '_named_bundles', None):
            bundles = [fp for name, bundle in self.assets_env._named_bundles.iteritems()
                       for fp in bundle.contents]
        else:
            bundles = []

        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename) \
                    [len(self.path):].strip(os.path.sep).replace(os.path.sep, '/')
                if filepath[:2] == './':
                    filepath = filepath[2:]
                if self.output in filepath or filepath in bundles:
                    continue

                elif '.html' in filepath:
                    templates.add(filepath)
                else:
                    other.add(filepath)

        return sorted(templates), sorted(bundles), sorted(other)


class SiteBuilder(object):

    def __init__(self, path, output='public', tmpl_builder_class=TemplateBuilder, **kwargs):

        self.path = path
        self.output_path = os.path.join(path, output)

        self.tmpl_builder_class = tmpl_builder_class(self.path, output, **kwargs)

    def build(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        templates, bundles, others = self.tmpl_builder_class.list_files()

        for template in templates:
            # XXX: for now we are not handling contexts
            self.tmpl_builder_class.build_template(template)

        for other in others:
            dirname = os.path.join(self.output_path, os.path.dirname(other))
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            shutil.copyfile(os.path.join(self.path, other), os.path.join(self.output_path, other))
