import argparse
import inspect
import yaml
import sys
import six

from cpbox.tool import logger as cplogger
from distutils import util

import logging
logger = logging.getLogger('functocli')
support_types = ('str', 'int', 'bool', 'float')

keep_class_set = set([])
def keep_class(cls):
    keep_class_set.add(cls)
    return cls

class AppSepc(object):

    def __init__(self, app, log_level, common_args_option=None):

        self.common_args_option = common_args_option

        stream_handler = logging.StreamHandler()
        cplogger.setup_logger_handler('functocli', stream_handler, log_level)
        logger.setLevel(stream_handler.level)
        logger.addHandler(stream_handler)

        self.app = app
        self.public_methods = get_app_public_methods(app)
        self.method_spec_map = self._get_app_method_spec()
        self.num_to_name_map = {str(index): name for index, name in enumerate(self.public_methods)}

        self.method_will_call = None

    def find_method_name(self, num_or_name):
        if num_or_name in self.num_to_name_map:
            return self.num_to_name_map[num_or_name]
        if num_or_name in self.method_spec_map:
            return num_or_name
        return None

    def resolve(self, default_method=None, enable_method_index=False):

        method_will_call = None
        if len(sys.argv) > 1:
            method_will_call = sys.argv[1].replace('--', '').replace('-', '')
        if method_will_call is None and default_method is not None:
            method_will_call =  default_method
        method_will_call = self.find_method_name(method_will_call)

        if not method_will_call:
            self.show_help_then_exit(enable_method_index)

        self.method_will_call = method_will_call
        self._parse_args()

    def _parse_args(self):
        method_will_call = self.method_will_call
        method_spec = self.method_spec_map[method_will_call]
        kwargs = build_argparser_for_func(method_will_call, method_spec)

        self.common_kwargs = {}
        if self.common_args_option:
            common_args_keys = set(self.common_args_option.get('args'))
            methods_args_keys = set(method_spec['method_args'])
            method_kwargs = {}
            for key, value in kwargs.items():
                if key in common_args_keys:
                    self.common_kwargs[key] = value
                if key in methods_args_keys:
                    method_kwargs[key] = value
            self.kwargs = method_kwargs
        else:
            self.kwargs = kwargs

    def run(self):
        kwargs = self.kwargs
        _app = self.app()
        func = getattr(_app, self.method_will_call)
        func(**kwargs)

    def _get_app_method_spec(self):
        method_spec_map = {}
        for method_name in self.public_methods:
            method_spec_map[method_name] = self.get_method_spec(method_name)
        return method_spec_map

    def get_method_spec(self, method_name):
        method_attr = getattr(self.app, method_name)
        func_spec = inspect.getargspec(method_attr)
        default_values = None
        if func_spec.defaults:
            default_values = dict(zip(func_spec.args[-len(func_spec.defaults):], func_spec.defaults))
        args = filter(lambda x: x != 'self', func_spec.args)

        method_spec = {}
        method_spec['method_args'] = list(args)
        if self.common_args_option != None:
            args.extend(self.common_args_option.get('args', []))
            args = list(set(args))
            default_values_from_common_args = self.common_args_option.get('default_values', [])
            if default_values is None:
                default_values = default_values_from_common_args
            else:
                default_values.update(default_values_from_common_args)

        method_spec['args'] = args
        method_spec['default_values'] = default_values
        method_spec['parameters'] = _check_parameters_spec(method_name, args, default_values)
        return method_spec

    def show_help_then_exit(self, enable_method_index):
        parser = argparse.ArgumentParser(add_help=False)
        parser.allow_abbrev = False
        parser.add_argument('-h', '--help', action='store_true', help='show this help message and exit')
        for index, method_name in enumerate(self.public_methods):
            if enable_method_index:
                parser.add_argument('-' + str(index), '--' + method_name, action='store_true')
            else:
                parser.add_argument('--' + method_name, action='store_true')
        parser.print_help()

        method_will_call = self.method_will_call
        if method_will_call and (method_will_call == 'h' or method_will_call == 'help'):
            sys.exit(0)
        else:
            sys.exit(1)

def _get_func_comments(method_attr):
    comments = inspect.getdoc(method_attr)
    if comments is None:
        return None
    else:
        return yaml.load(comments)

def _is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def _check_parameter_item_default_value(arg_name, parameter_item, default_values):
    if default_values is None or arg_name not in default_values:
        return parameter_item

    value = default_values[arg_name]
    type = _determine_type(value)

    if type is None:
        raise Error('Can not determine type for parameter: %s, parameter_item: %s' %s (arg_name, parameter_item))

    parameter_item['type'] = type
    parameter_item['des'] = 'type: %s, default value is: %s' % (type, value)
    return parameter_item

def _determine_type(value):
    type = None
    if value is None:
        type = 'str'
    elif isinstance(value, bool):
        type = 'bool'
    elif isinstance(value, six.integer_types):
        type = 'int'
    elif isinstance(value, six.string_types):
        type = 'str'
    elif _is_float(value):
        type = 'float'
    return type

def _convert_value_for_type(value, type):
    if value is None:
        return value
    elif type == 'bool':
        if isinstance(value, six.string_types):
            try:
                return bool(util.strtobool(value))
            except:
                return False
        return bool(value)
    elif type == 'int':
        return int(value)
    elif type == 'str':
        return str(value)
    elif type == 'float':
        return float(value)
    return value

def _check_parameters_spec(method_name, args, default_values):
    parameters = {}
    for arg_name in args:
        parameter_item = {}
        if isinstance(parameter_item, six.string_types):
            parameter_item = {
                    'type': 'str',
                    'des': parameter_item
                    }
        parameter_item = _check_parameter_item_default_value(arg_name, parameter_item, default_values)
        if 'type' not in parameter_item:
            parameter_item['type'] = 'str'
        if 'des' not in parameter_item:
            parameter_item['des'] = arg_name

        parameters[arg_name] = parameter_item
        _check_parameter_item(arg_name, parameter_item)

    return parameters

def _check_parameter_item(arg_name, parameter_item):
    if 'type' not in parameter_item:
        logger.warn('Missing type in parameter item: %s', parameter_item)
    if parameter_item['type'] not in support_types:
        logger.warn('The type: %s is not in support types: %s', parameter_item['type'], support_types)
    if not parameter_item['des']:
        logger.warn('Missing parameter descripion(`des`): %s', parameter_item)

def get_app_public_methods(app):
    parent_members = {}
    for base_class in app.__bases__:
        if base_class in keep_class_set:
            continue
        parent_members_list = inspect.getmembers(base_class, predicate=inspect.ismethod)
        parent_members.update(dict((item[0], item[1]) for item in parent_members_list))
    public_method_names = inspect.getmembers(app, predicate=inspect.ismethod)
    ret = filter(lambda x: x[0].startswith('_') == False and x[0] not in parent_members, public_method_names)
    ret = [item[0] for item in ret]
    return ret

def build_argparser_for_func(method_name, method_spec):

    args = method_spec['args']
    default_values = method_spec['default_values']

    parser = argparse.ArgumentParser()
    parser.add_argument('--' + method_name, action='store_true')

    parameters = method_spec.get('parameters', {})
    for arg_name in args:
        parameter = parameters.get(arg_name)
        help = parameter.get('des', '')
        metavar = ''

        if default_values is not None and arg_name in default_values:
            if len(arg_name) == 1:
                parser.add_argument('-' + arg_name, metavar=metavar, help=help, default=default_values[arg_name], nargs=1, required=False)
            else:
                parser.add_argument('--' + arg_name, metavar=metavar, help=help, default=default_values[arg_name], nargs=1, required=False)
        else:
            if len(arg_name) == 1:
                parser.add_argument('-' + arg_name, metavar=metavar, help=help, nargs=1, required=True)
            else:
                parser.add_argument('--' + arg_name, metavar=metavar, help=help, nargs=1, required=True)
    args_input, _ = parser.parse_known_args()
    kwargs = {}
    for arg_name in args:
        parameter = parameters.get(arg_name)
        attr = getattr(args_input, arg_name)
        if default_values is not None and arg_name in default_values and attr == default_values[arg_name]:
            kwargs[arg_name] = attr
        else:
            kwargs[arg_name] = _convert_value_for_type(
                    _get_first_from_list_or_item_self(attr), parameter['type'])
    return kwargs

def _get_first_from_list_or_item_self(attr):
    try:
        return next(iter(attr), None)
    except Typeerror:
        return attr

def _check_args_has(args, option):
    ret = getattr(args, option)
    return ret

def run_app(app, log_level='critical', default_method=None):
    app_spec = AppSepc(app, log_level)
    app_spec.resolve(default_method)
    app_spec.run()
