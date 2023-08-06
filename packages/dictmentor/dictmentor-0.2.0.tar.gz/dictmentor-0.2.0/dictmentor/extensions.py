import os
import re
from abc import abstractmethod

from .utils import FileLocator
from .validator import Validator


class ExtensionError(Exception):
    pass


class Extension(object):
    """
    Provides a general interface for any extension.
    """
    @classmethod
    def is_valid_extension(cls, candidate):
        return hasattr(candidate, 'apply') and hasattr(candidate, 'config')

    def config(self):
        """
        Instructs the `DictMentor` scanner which nodes are relevant for this extension.
        A config consists of three configurable instruction arguments:
        * pattern -> Specifies the pattern to look for in the dictionary model (standard regex)
        * key -> If set to True, the pattern will be applied to keys; otherwise keys are ignored.
        * value -> If set to True, the pattern will be applied to values; otherwise values are ignored.
        Under the hood the config will be passed to dict_find_pattern by the mentor.

        Examples:
            >>> # Looks for the given pattern in key strings only
            >>> cfg = dict(pattern='external.*', search_in_keys=True, search_in_values=False)
            >>> from collections import OrderedDict
            >>> dic = OrderedDict((('a', 'a'), ('external12', 'abc'), ('b', dict(c='c', external56='cde'))))
            >>> from dictmentor.utils import dict_find_pattern
            >>> for _, key, value in dict_find_pattern(dic, **cfg):
            ...     print(key, value)
            external12 abc
            external56 cde

        Returns:
        """
        return self._config()

    @abstractmethod
    def _config(self):
        raise NotImplementedError()  # pragma: no cover

    def apply(self, **ctx):
        """
        This method gets called every time a configured pattern is found in the dictionary. See Args section
        for the available context that is passed.
        Args:
            ctx (dict): Context for processing. What is part of the context depends but normally it will consist of
                * mentor: The processor (DictMentor) instance.
                * document: The document as it was passed to the processor. Might be a file name, stream, string or
                    dictionary.
                * dct: The whole dictionary not just parts of it.
                * parent_node: The parent_node of node that has the configured pattern as a python dictionary.
                * node: Tuple of key and value of the node that matches the pattern.
        Returns:
            Returns a python dictionary. The dictionary will be integrated into dictionary model.
            Basically parent_node.update(result) will be called to modify the dictionarx model. This way you can modify
            even more than just the actual key / value pair. See the implementation of `ExternalResource` which
            leverages this feature.
        """
        return self._apply(**ctx)

    @abstractmethod
    def _apply(self, **ctx):
        raise NotImplementedError()  # pragma: no cover


class ExternalResource(Extension):
    """
    Loads an external resource (text) into the dictionary.
    Syntax: {{external::/path/to/external/file.txt}}

    Examples:
        >>> import tempfile
        >>> tmp = tempfile.NamedTemporaryFile()
        >>> with open(tmp.name, 'w') as fp:
        ...     print('SELECT *', file=fp); print('FROM my_table', file=fp); print("WHERE 1 = 1", file=fp)
        >>> current = '{"a": 1, "b": 2, "sql": "{{external::%s}}"}' % tmp.name
        >>> from dictmentor import DictMentor
        >>> (DictMentor().bind(ExternalResource()).load_yaml(current)
        ... == {'a': 1, 'b': 2, 'sql': 'SELECT *\\nFROM my_table\\nWHERE 1 = 1\\n'})
        True
    """
    __pattern__ = '.*({{external::(.*)}}).*'

    def __init__(self, base_path=None, locator=None):
        """
        Initializer.
        Args:
            base_path: Base path. Fast way to construct a `FileLocator` if no locator is passed.
                Will be ignored when a locator is given.
            locator:
        """
        self._base_path = str(base_path)
        if locator is None:
            self.locator = FileLocator(self._base_path)
        else:
            self.locator = locator

    def _config(self):
        """
        Tells the processor to scan for the given pattern on node values only.
        Returns: The processor scanning configuration.
        """
        return dict(pattern=self.__pattern__, search_in_keys=False, search_in_values=True)

    def _apply(self, mentor, document, node, **ctx):
        """
        Performs the actual loading of an external resource into the current model.
        Args:
            mentor (DictMentor): Current processor.
            document: The actual raw yaml model.
            node: Tuple of node key and value of the current node to process.
            **ctx: Additional (unused) context.
        Returns:
            Returns a dictionary that gets incorporated into the actual model.
        """
        def process(pattern, s):
            m = pattern.match(s)
            if m is None:
                return s  # pragma: no cover
            # We got a match
            # Group 0: Whole match; Group 1: Our placeholder; Group 2: file path to external resource
            placeholder, external_path = m.group(1), m.group(2)
            with open(self.locator(external_path, document if Validator.is_file(document=document) else None)) as fp:
                # Json does not support line breaks. We will have to mask them
                content = fp.read()
            return s.replace(placeholder, content)

        node_key, node_value = node
        p = re.compile(self.__pattern__)
        return {node_key: process(p, node_value)}


class ExternalYamlResource(ExternalResource):
    """
    Enables the integration of external/other yaml files into the actual model.
    Examples:
        current.json:
        {
            "a": 1
            "b": 2
            "external": "/path/to/other/json/file.json"
        }
        /path/to/other/json/file.json:
        {
            "b": 99,
            "c": 3
        }
        Will result into:
        {
            "a": 1,
            "b": 99,
            "c": 3
        }
        >>> import tempfile
        >>> tmp = tempfile.NamedTemporaryFile()
        >>> with open(tmp.name, 'w') as fp:
        ...     print('{"b": 99, "c": 3}', file=fp)
        >>> current = '{"a": 1, "b": 2, "external": "%s"}' % tmp.name
        >>> from dictmentor import DictMentor
        >>> (DictMentor().bind(ExternalYamlResource()).load_yaml(current)
        ... == {'a': 1, 'b': 99, 'c': 3})
        True
    """
    __pattern__ = r'^\s*external\s*$'

    def __init__(self, **kwargs):
        """
        Initializer.
        Args:
            base_path: Override the path for external resource lookups with relative links. Default path is where
                the yaml file is located. When the yaml data comes from a stream or a str (not a file)
                the default is the current working directory.
        """
        super().__init__(**kwargs)

    def _config(self):
        """
        Tells the processor to look for the specified pattern in node key only.
        Returns: The scanner configuration.
        """
        return dict(pattern=self.__pattern__, search_in_keys=True, search_in_values=False)

    def _apply(self, mentor, document, node, **ctx):
        """
        Loads a yaml fragment from an external file.

        Args:
            mentor (DictMentor): The processor. Used to delegate work on yaml fragments.
            document: Is the stream, file or string that contains the actual yaml content. Used to determine the
                content path.
            node (tuple): Tuple consisting of the node's key and value, where the pattern external resource was
                found.
            ctx: Additional (unused) context.

        Returns:
            The external resource as a python dictionary. The fragment is already send through the processor as
            well.
        """
        _, external_path = node
        return mentor.load_yaml(self.locator(external_path, document if Validator.is_file(document=document) else None))


class Environment(Extension):
    """
    Enables the replacement of any environment variables in a dictionary.
    Syntax: {{env::my_env}} -> Will be replaced by the value of the environment variable 'my_env'
    Examples:
        >>> from dictmentor import DictMentor
        >>> from dictmentor.utils import modified_environ
        >>> jstr = '{"a": 1, "file_path": "my_file.{{env::ENVIRONMENT}}.cfg"}'
        >>> with modified_environ(ENVIRONMENT='production'):
        ...     DictMentor().bind(Environment()).load_yaml(jstr) == {'a': 1, 'file_path': 'my_file.production.cfg'}
        True
        >>> # If an environment variable is not set, a default is rendered instead. You can specify the default
        >>> # via an init argument. Default of the default is 'none' ...
        >>> with modified_environ('ENVIRONMENT'):
        ...     (DictMentor().bind(Environment(default='development')).load_yaml(jstr)
        ...     == {'a': 1, 'file_path': 'my_file.development.cfg'})
        True
        >>> # ... or by specifying fail_on_unset an exception will be raised
        >>> with modified_environ('ENVIRONMENT'):
        ...     res = DictMentor().bind(
        ...         Environment(fail_on_unset=True, default='development')
        ...     ).load_yaml(jstr)
        Traceback (most recent call last):
        ...
        dictmentor.extensions.ExtensionError: Environment variable 'ENVIRONMENT' is unset.
    """
    __pattern__ = '.*({{env::(.*)}}).*'

    def __init__(self, fail_on_unset=False, default='none'):
        """
        Initializer.
        Args:
            fail_on_unset (bool): If set to True an exception will be raised when the environment variable is unset;
                otherwise the default value (see next) will be used instead.
            default (str): If a environment variable is unset, it will get this value instead.
        """
        self.fail_on_unset = bool(fail_on_unset)
        self.default = str(default)

    def _config(self):
        """
        Tells the processor to scan for the specified pattern in node keys and values.
        Returns: The scanner configuration.
        """
        # tells the scanner to look for the specified pattern in key and value strings
        return dict(pattern=self.__pattern__, search_in_keys=True, search_in_values=True)

    def _apply(self, node, **ctx):
        """
        Replaces any {{env::*}} directives with it's actual environment variable value or a default.
        Args:
            node (tuple): Key and value of the current node.
            **ctx: Additional (unused) context.
        Returns:
            Returns the altered node key and value.
        """
        node_key, node_value = node

        def process(pattern, s):
            m = pattern.match(s)
            if m is None:
                return s
            # We got a match
            # Group 0: Whole match; Group 1: Our placeholder; Group 2: The environment variable
            placeholder, envvar = m.group(1), m.group(2)
            envvalue = os.environ.get(envvar, None)
            if envvalue is None and self.fail_on_unset:
                raise ExtensionError("Environment variable '{}' is unset.".format(envvar))

            return s.replace(placeholder, envvalue or self.default)

        p = re.compile(self.__pattern__)
        node_key = process(p, node_key)
        node_value = process(p, node_value)

        return {node_key: node_value}


class Variables(Extension):
    """
    Enables the replacement of any variables in a dictionary.
    Syntax: {{var::my_env}} -> Will be replaced by the value of the variable 'my_env'
    Examples:
        >>> from dictmentor import DictMentor
        >>> jstr = '{"a": 1, "file_path": "my_file.{{var::environment}}.cfg"}'
        >>> extension = Variables(environment='production')
        >>> DictMentor().bind(extension).load_yaml(jstr) == {'a': 1, 'file_path': 'my_file.production.cfg'}
        True
        >>> extension = Variables(notenvironment="bla", default='default')
        >>> DictMentor().bind(extension).load_yaml(jstr) == {'a': 1, 'file_path': 'my_file.default.cfg'}
        True
        >>> extension = Variables(notenvironment="bla", fail_on_unset=True)
        >>> DictMentor().bind(extension).load_yaml(jstr) == {'a': 1, 'file_path': 'my_file.default.cfg'}
        Traceback (most recent call last):
        ...
        dictmentor.extensions.ExtensionError: Variable 'environment' is unset.
    """
    __pattern__ = '.*({{var::(.*)}}).*'

    def __init__(self, fail_on_unset=False, default='none', **vars):
        """
        Initializer.
        Args:
            fail_on_unset (bool): If set to True an exception will be raised when the environment variable is unset;
                otherwise the default value (see next) will be used instead.
            default (str): If a environment variable is unset, it will get this value instead.
        """
        self.fail_on_unset = bool(fail_on_unset)
        self.default = str(default)
        self.vars = vars

    def _config(self):
        """
        Tells the processor to scan for the specified pattern in node keys and values.
        Returns: The scanner configuration.
        """
        # tells the scanner to look for the specified pattern in key and value strings
        return dict(pattern=self.__pattern__, search_in_keys=True, search_in_values=True)

    def _apply(self, node, **ctx):
        """
        Replaces any {{var::*}} directives with it's actual variable value or a default.
        Args:
            node (tuple): Key and value of the current node.
            **ctx: Additional (unused) context.
        Returns:
            Returns the altered node key and value.
        """
        node_key, node_value = node

        def process(pattern, s):
            m = pattern.match(s)
            if m is None:
                return s
            # We got a match
            # Group 0: Whole match; Group 1: Our placeholder; Group 2: The environment variable
            placeholder, varname = m.group(1), m.group(2)
            varval = self.vars.get(varname, None)
            if varval is None and self.fail_on_unset:
                raise ExtensionError("Variable '{}' is unset.".format(varname))

            return s.replace(placeholder, varval or self.default)

        p = re.compile(self.__pattern__)
        node_key = process(p, node_key)
        node_value = process(p, node_value)

        return {node_key: node_value}
