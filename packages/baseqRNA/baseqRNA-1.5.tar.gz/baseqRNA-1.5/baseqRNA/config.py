import os, sys
import configparser as CP

class configManager:
    """
    ConfigManager will read sections from config file.
    """
    def __init__(self, path = ""):
        if not os.path.exists(path):
            sys.exit("[ERROR] The config file does not exist. Please check weather you point a valid configuration file.")
        
        self.file = path
        self.config = CP.ConfigParser()
        self.config.optionxform = str
        self.config.read(path)

    def get_section(self, section):
        res = {}
        if section not in self.config:
            sys.exit("[error] Section [{}] not defined in config file '{}'".format(section, self.file))
        for key in self.config[section]:
            res[key] = self.config[section][key]
        return sectionManager(res, section, self)

class sectionManager:
    """
    SectionManager will read items from section.
    """
    def __init__(self, data, name, config):
        self.data = data
        self.name = name
        self.keys = self.get_keys()
        self.config = config

    def get_keys(self):
        keys = []
        for key in self.data:
            keys.append(key)
        return keys

    def get(self, key):
        if key in self.keys:
            print("[info] {}=>{}:{}".format(self.name, key, self.data[key]))
            return self.data[key]
        else:
            sys.exit("[ERROR] Item '{}' is not configured in [{}]. \n[ERROR] Please add the item in '{}'.".format(key, self.name, self.config.file))

def get_config(section, item, cfgpath = ""):
    """
    Get the configure content of a item from certain section in the config file.

    A valid sample should have a valid fastq file as read1.
    ::
        from baseqCNV.config import get_config
        get_config()
    
    """
    if cfgpath and os.path.exists(cfgpath):
        section_cfg = configManager(cfgpath).get_section(section)
    elif 'BASEQCFG' in os.environ and os.path.exists(os.environ['BASEQCFG']):
        section_cfg = configManager(os.environ['BASEQCFG']).get_section(section)
    else:
        section_cfg = configManager().get_section(section)
    cfg = section_cfg.get(item)
    return cfg