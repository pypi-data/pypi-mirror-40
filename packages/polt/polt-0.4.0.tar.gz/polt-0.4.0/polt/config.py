# system modules
import configparser
import shlex
import os

# internal modules
from polt.utils import normalize_cmd

# external modules
import xdgspec

USER_CONFIG_FILE = os.path.join(
    xdgspec.XDGPackageDirectory("XDG_CONFIG_HOME", "polt").path, "polt.conf"
)
LOCAL_CONFIG_FILE = ".polt.conf"

DEFAULT_CONFIG_FILES = (USER_CONFIG_FILE, LOCAL_CONFIG_FILE)


class Configuration(configparser.ConfigParser):
    """
    Class for configurations.
    """

    SOURCE_SECTION_PREFIX = "source"
    """
    Prefix for sections specifying a source
    """

    @property
    def source_section(self):
        """
        Generator yielding source sections

        Yields:
            configparser.SectionProxy: the next source section
        """
        for name, section in self.items():
            if name.startswith(self.SOURCE_SECTION_PREFIX):
                yield section

    def matching_source_section(self, command=None, parser=None):
        """
        Generator yielding source sections with a similar specification

        Args:
            cmd (str, optional): the command to check for
            parser (str, optional): the parser to check for

        Yields:
            configparser.SectionProxy: the next matching source section
        """
        for section in self.source_section:
            command_matches = False
            if command is not None:
                this_cmd = section.get("command")
                if not this_cmd:  # pragma: no cover
                    continue
                if normalize_cmd(this_cmd) == normalize_cmd(command):
                    command_matches = True
            else:
                command_matches = True
            parser_matches = False
            if parser is not None:
                this_parser = section.get("parser")
                parser_matches = this_parser == parser
            else:
                parser_matches = True
            if command_matches and parser_matches:
                yield section

    @staticmethod
    def to_string(value):
        """
        Convert a value to a sensible configuration string. :class:`bool`
        objects are converted to ``"yes"`` and ``"no"``, :class:`str` objects
        are left as they are and the rest is converted to :class:`str`.

        Args:
            value (object): the value to convert

        Returns:
            str : the converted string value
        """
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return "yes" if value else "no"
        return str(value)

    def update_option(self, section, key, value=None, default=None):
        """
        Update an option value

        Args:
            section (str): the name of the section
            key (str): the key
            value (object, optional): the new value. If ``None`` (the default)
                the value is left untouched or set to the value of ``default``
                if it is defined and the ``key`` doesn't exist.
                Is converted with :meth:`to_string`.
            default (object, optional): default fallback value if ``value`` is
                ``None``. Is converted with :meth:`to_string`.
        """
        if section not in self:
            self.add_section(section)
        sec = self[section]
        if value is None:
            if default is not None:
                if key not in sec:
                    sec[key] = self.to_string(default)
        else:
            sec[key] = self.to_string(value)
