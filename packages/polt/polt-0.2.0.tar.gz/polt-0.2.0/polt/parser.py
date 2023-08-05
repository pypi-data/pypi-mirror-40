# system modules
import sys
import inspect
import re
import functools
import itertools
import csv
import logging
import collections
from abc import ABC, abstractproperty

# internal modules
from polt.streamer import Streamer
from polt.utils import str2num

# external modules


logger = logging.getLogger(__name__)


class Parser(ABC):
    """
    Abstract base class for parsers.

    Args:
        f (file-like object, optional): the connection to read from
        name (str, optional): human-readable description of the parser
    """

    def __init__(self, f=None, name=None):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def name(self):
        """
        Human-readable description of the parser

        :type: :class:`str`
        :getter: If no :attr:`name` was set yet, attempt to return a
            meaningful name based on :attr:`f`.
        """
        try:
            return self._name
        except AttributeError:
            return _("{} on {}").format(
                type(self).__name__,
                self.f.name if hasattr(self.f, "name") else repr(self.f),
            )

    @name.setter
    def name(self, new):
        self._name = str(new)

    @property
    def f(self):
        """
        The connection to read from
        """
        try:
            self._f
        except AttributeError:  # pragma: no cover
            self._f = None
        return self._f

    @f.setter
    def f(self, new):
        self._f = new

    @abstractproperty
    def data(self):
        """
        Generator yielding the next dataset. This is an
        :meth:`abc.abstractproperty`, thus subclasses have to override this.

        Yields:
            dict : dictionary like

                .. code:: python

                    {
                        quantity_spec1: value1,
                        quantity_spec2: value2,
                        quantity_spec3: value3,
                        ...
                    }

                quantity_spec
                    either a :class:`str` containing the name of the quantity
                    or a :class:`tuple` ``(name, unit)`` specifying the
                    quantity's name and unit
                value
                    either a single value or a sequence of values
        """
        pass

    @property
    def dataset(self):
        """
        Generator yielding the next :attr:`data` with metadata appended

        Yields:
            dict : dictionary like

                .. code:: python

                    {
                        "parser": parser_name,
                        "data": {
                            quantity_spec1: value1,
                            quantity_spec2: value2,
                            quantity_spec3: value3,
                            ...
                            },
                    }

                parser_name
                    The :attr:`Parser.name`
                quantity_spec
                    either a :class:`str` containing the name of the quantity
                    or a :class:`tuple` ``(name, unit)`` specifying the
                    quantity's name and unit
                value
                    either a single value or a sequence of values
        """
        for data in self.data:
            yield {"parser": self.name, "data": data}


class NumberParser(Parser):
    """
    Simple parser extracting numbers line-wise

    Args:
        f (file-like object, optional): the connection to read from
        name (str, optional): human-readable description of the parser
        quantity (str, optional): quantity of the numbers read
        unit (str, optional): unit of the numbers read
    """

    NUMBER_REGEX = re.compile(r"-?\d+(?:\.\d+)?")
    """
    Regular expression to detect numbers
    """

    def __init__(self, f=None, name=None, quantity=None, unit=None):
        Parser.__init__(self, f=f, name=name)
        if quantity is not None:
            self.quantity = quantity
        if unit is not None:
            self.unit = unit

    @property
    def quantity(self):
        try:
            self._quantity
        except AttributeError:
            self._quantity = _("number")
        return self._quantity

    @quantity.setter
    def quantity(self, new):
        self._quantity = new

    @property
    def unit(self):
        try:
            self._unit
        except AttributeError:
            self._unit = None
        return self._unit

    @unit.setter
    def unit(self, new):
        self._unit = new

    @property
    def data(self):
        logger.debug(
            _("Reading from {}...").format(
                self.f.name if hasattr(self.f, "name") else repr(self.f)
            )
        )
        for line in self.f:
            if not line.strip():
                continue
            logger.debug(
                _("Received {} from {}").format(
                    repr(line),
                    self.f.name if hasattr(self.f, "name") else repr(self.f),
                )
            )
            numbers = (
                float(m.group())
                for m in self.NUMBER_REGEX.finditer(
                    line.decode(errors="ignore")
                    if hasattr(line, "decode")
                    else line
                )
            )
            numbers_list = list(numbers)
            logger.debug(_("Numbers extracted: {}").format(numbers_list))
            yield {(self.quantity, self.unit): numbers_list}


class CsvParser(Parser):
    """
    Parser for CSV input

    Args:
        f (file-like object, optional): the connection to read from
        name (str, optional): human-readable description of the parser
        header_regex (re.compile, optional): regular expression applied to the
            header to extract quantity and unit. See :attr:`header_regex` and
            :meth:`parse_header` for further information.
        only_columns (set of str, optional): only return columns in this
            set. The default is to use all columns without restriction.
    """

    HEADER_REGEX_MATCHALL = re.compile(".*")
    """
    Default regular expression for :attr:`header_regex` matching everything.
    """

    HEADER_REGEX_UNIT_LAST = re.compile(
        pattern=r"(?P<quantity>.*?)(?:[^a-zA-Z0-9]+(?P<unit>[a-zA-Z0-9]+))?"
    )
    """
    Regular expression for use in :attr:`header_regex` or :meth:`parse_header`
    which extracts the unit as the last part of the header separated by a
    non-word character.
    """

    def __init__(
        self,
        f=None,
        name=None,
        header_regex=None,
        only_columns=None,
        **dictreader_kwargs
    ):
        Parser.__init__(self, f=f, name=name)
        if header_regex is not None:
            self.header_regex = header_regex
        if only_columns is not None:
            self.only_columns = only_columns
        self.dictreader_kwargs = dictreader_kwargs

    @property
    def header_regex(self):
        """
        Regular expression applied used as default in :meth:`parse_header`.
        Defaults to :attr:`HEADER_REGEX_MATCHALL`.

        :type: regular expression created with :meth:`re.compile`
        """
        try:
            self._header_regex
        except AttributeError:
            self._header_regex = self.HEADER_REGEX_MATCHALL
        return self._header_regex

    @header_regex.setter
    def header_regex(self, new):
        self._header_regex = re.compile(pattern=new)

    def modifies_csvreader(decorated_function):
        """
        Decorator for methods that require a reset of the :attr:`csvreader`
        """

        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_csvreader"):
                logger.debug(
                    _("Resetting csvreader before {}").format(
                        decorated_function
                    )
                )
                del self._csvreader  # pragma: no cover
            return decorated_function(self, *args, **kwargs)

        return wrapper

    @property
    def csvreader(self):
        """
        The underlying csv parser

        :type: :class:`csv.DictReader`
        """
        try:
            self._csvreader
        except AttributeError:
            self._csvreader = csv.DictReader(self.f, **self.dictreader_kwargs)
        return self._csvreader

    @property
    def dictreader_kwargs(self):
        """
        Further keyword arguments for the underlying :attr:`csvreader`

        :type: :class:`dict`
        :setter: resets the :attr:`csvreader`
        """
        try:
            self._dictreader_kwargs
        except AttributeError:  # pragma: no cover
            self._dictreader_kwargs = {}
        return self._dictreader_kwargs

    @dictreader_kwargs.setter
    @modifies_csvreader
    def dictreader_kwargs(self, new):
        self._dictreader_kwargs = new

    @Parser.f.setter
    @modifies_csvreader
    def f(self, new):
        self._f = new

    @property
    def only_columns(self):
        """
        Only yield these columns in :attr:`data`. The default is to use all
        columns.

        :type: :class:`set`
        :setter: splits string inputs by commas and converts input to
            :class:`set`
        """
        try:
            self._only_columns
        except AttributeError:
            self._only_columns = None
        return self._only_columns

    @only_columns.setter
    def only_columns(self, new):
        self._only_columns = set(
            new.split(",") if hasattr(new, "split") else new
        )

    def str2num(self, s):
        """
        Convert a string or a sequence of strings to numbers with
        :meth:`polt.utils.str2num`.

        Args:
            s (str or sequence of str): the string(s) to convert

        Returns:
            (sequence of) str or int or float: the result of
                :meth:`polt.utils.str2num`
        """
        if isinstance(s, str):
            return str2num(s)
        elif isinstance(s, collections.Sequence):
            return [self.str2num(x) for x in s]
        else:
            return s

    def parse_header(self, header, regex=None):
        """
        Parse a header field name based on :attr:`header_regex` to determine
        its quantity name and unit. The quantity is extracted as either the
        content of the ``quantity`` named captured group or the first captured
        group with a fallback to the given header name itself. The unit is
        extracted similarly as either the content of the ``unit`` named
        captured group or the next captured group. By default, the unit is
        ``None``.

        Args:
            header (str): the header field name
            regex (re.compile, optional): the regular expression to use.
                Default is :attr:`header_regex`.

        Returns:
            quantity, unit: quantity and unit
        """
        m = (regex if regex is not None else self.header_regex).fullmatch(
            header
        )
        quantity = header
        unit = None
        if m:
            groups_iter = iter(m.groups())
            quantity_sources = itertools.chain(
                [m.groupdict().get("quantity")], groups_iter, [header]
            )
            unit_sources = itertools.chain(
                [m.groupdict().get("unit")], groups_iter
            )
            quantity = next(filter(bool, quantity_sources), header)
            unit = next(
                filter(bool, filter(lambda x: x != quantity, unit_sources)),
                None,
            )
        return quantity, unit

    @property
    def data(self):
        for row in self.csvreader:
            d = {
                self.parse_header(k): self.str2num(v)
                for k, v in row.items()
                if (
                    k is not None
                    and k
                    in (
                        self.only_columns
                        if self.only_columns is not None
                        else row
                    )
                )
            }
            if d:
                yield d
