import os
import yaml


class _ConfigObj:

    def __init__(self, config: dict, **kwargs):
        """
        An object that given a configuration dictionary, sets its attributes
        to the given keyword arguments.

        The name of the keyword argument is the attribute name and the value is
        the key in the configuration dictionary to use.
        """
        self.config = config
        self._helper(**kwargs)

    def _helper(self, **kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                if isinstance(v, tuple):
                    if v[0] not in self.config:
                        print(k, v[0])
                        setattr(self, k, v[1])
                else:
                    if v not in self.config:
                        raise ValueError("The configuration object doesn't have a value for that!")
                    setattr(self, k, self.config[v])


class _ProcessValueConfigObj(_ConfigObj):

    def __init__(self, name: str, config_key: str, config: dict, arg_input_key: str = None, output_loc_key: str = None,
                 **kwargs):
        """
        A needless class that represents the configuration of a value through function calls.
        The name is the name of the function used to generate the value.
        The config key is the key in the configuration dictionary that is gives the config for this specific process value.
        The arg input key is the key in the config for this process value that gives the location of arguments input to the generation call.
        """
        print(name)

        self.obj_name = name
        self.config = config[config_key]
        super().__init__(config[config_key], **kwargs)

        self.arg_input = None
        if arg_input_key is not None:
            self.arg_input = self.config[arg_input_key]
            if self.arg_input == 'incall':
                self.arg_input = self.obj_name

        self.output_loc = None
        if output_loc_key is not None:
            self.output_loc = self.config[output_loc_key]
            if self.output_loc == 'incall':
                self.output_loc = self.obj_name

    def get_arg_input(self):
        return self.arg_input

    def get_output_loc(self):
        return self.output_loc


class PasswordSaltFunctionConfigObj(_ProcessValueConfigObj):

    def __init__(self, name: str, config: dict):
        super().__init__(name, 'salts', config, output_loc_key='salt_digest')


class PasswordHashFunctionConfigObj(_ProcessValueConfigObj):

    def __init__(self, name: str, config: dict):
        super().__init__(name, 'hashes', config, arg_input_key='pwinput', output_loc_key='message_digest',
                         algorithm_names='algorithm', key_len_supported=('keylen', False), iteration_supported=('iteration', False))

    def get_algorithm(self):
        return self.algorithm_names

    def is_key_len_supported(self):
        return self.key_len_supported

    def is_iteration_supported(self):
        return self.iteration_supported


class PasswordHashPackageConfigObj:

    def __init__(self, name: str, config: dict):
        self.config = config
        self.package_name = name
        self.hash_fn_config_map = {}
        self.salt_fn_config_map = {}
        self._helper()

    def _helper(self):
        if 'hashobj' in self.config:
            for k, v in self.config['hashobj'].items():
                config_obj = PasswordHashFunctionConfigObj(k, v)
                self.hash_fn_config_map[k] = config_obj

        if 'saltobj' in self.config:
            for k, v in self.config['saltobj'].items():
                config_obj = PasswordSaltFunctionConfigObj(k, v)
                self.salt_fn_config_map[k] = config_obj

    def get_configs(self):
        return self.hash_fn_config_map, self.salt_fn_config_map

    def get_hash_config(self, hashobj: str):
        return self.hash_fn_config_map[hashobj]

    def get_salt_config(self, saltobj: str):
        return self.salt_fn_config_map[saltobj]


class PasswordHashPackagesConfigObj:

    def __init__(self, config: dict):
        self.config = config
        self.hash_package_map = {}
        self._helper()

    def _helper(self):
        for k, v in self.config.items():
            config_obj = PasswordHashPackageConfigObj(k, v)
            self.hash_package_map[k] = config_obj

    def get_package_configuration(self, pkg_name: str) -> PasswordHashPackageConfigObj:
        return self.hash_package_map[pkg_name]

    def get_package_hashobj_configuration(self, pkg_name: str, hashobj_name: str):
        pkg_config = self.get_package_configuration(pkg_name)
        hashobj_config = pkg_config.get_config(hashobj_name)
        return hashobj_config

    def get_package_hashobj_configuration_by_fullname(self, fullname: str):
        sp = fullname.split('.')
        if len(sp) == 2:
            pkg_name, hashobj_name = sp[0], sp[1]
        else:
            raise ValueError("The full name given was incorrect <pkg_name>.<hashobj_name> format only.")

        return self.get_package_hashobj_configuration(pkg_name, hashobj_name)

    def print_all(self):
        for k, v in self.hash_package_map.items():
            print(k, v.get_configs())

    @classmethod
    def from_config_file(cls, filepath: str):
        fname, ext = os.path.splitext(filepath)
        if ext == '.yaml':
            with open(filepath, 'r') as f:
                config_obj = yaml.safe_load(f)['packages']
                return PasswordHashPackagesConfigObj(config_obj)


if __name__ == '__main__':
    phs = PasswordHashPackagesConfigObj.from_config_file('passenc-config.yaml')
    phs.print_all()
