from os.path import isfile, dirname
import yaml
from yamlinclude import YamlIncludeConstructor
from zope import interface
from zope.interface.exceptions import BrokenImplementation
from jinja2 import Template

from sparc.config.container import SparcConfigContainer
from .interfaces import ISparcYamlConfigContainers


@interface.implementer(ISparcYamlConfigContainers)
class SparcYamlConfigContainers(object):

    def containers(self, yaml_config, render_context=None, base_dir=None):
        if isfile(u"{}".format(yaml_config)):
            if base_dir:
                YamlIncludeConstructor.add_to_loader_class(base_dir=base_dir)
            else:
                YamlIncludeConstructor.add_to_loader_class(
                    base_dir=u"{}".format(dirname(yaml_config)))
            config = open(yaml_config).read()
        else:
            YamlIncludeConstructor.add_to_loader_class(base_dir=base_dir)
            config = yaml_config
        
        if render_context:
            config = Template(config).render(render_context)
        for doc in yaml.load_all(config):
            try:
                yield SparcConfigContainer(doc)
            except BrokenImplementation:
                raise ValueError("expected yaml_config to contain valid yaml file path or string: {}".format(yaml_config))

    def first(self, yaml_config, render_context=None, base_dir=None):
        return next(self.containers(yaml_config, render_context, base_dir))