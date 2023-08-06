# system modules
import logging
import warnings
import pkg_resources

# internal modules
from polt.version import POLT_PARSER_ENTRY_POINT
import polt.parser.parser
import polt.parser.numberparser
import polt.parser.csvparser

# external modules

logger = logging.getLogger(__name__)


def get_parsers():
    """
    Check entry points for parsers. Invalid entry points are
    skipped with a warning. Entry points pointing to classes not inheriting
    from :class:`polt.parser.parser.Parser` are still included but with a
    warning.

    Returns:
        dict : mapping of :class:`pkg_resources.EntryPoint` s to the respective
        classes
    """
    parsers = {}
    for entry_point in pkg_resources.iter_entry_points(
        POLT_PARSER_ENTRY_POINT
    ):
        try:
            parser_cls = entry_point.load()
        except BaseException as e:
            warnings.warn(
                _(
                    "Could not load {entry_point} entry point {name} "
                    "from {dist}: {err}"
                ).format(
                    entry_point=repr(POLT_PARSER_ENTRY_POINT),
                    name=repr(entry_point.name),
                    err=e,
                    dist=repr(entry_point.dist or _("unknown distribution")),
                )
            )
            continue
        try:
            if not issubclass(parser_cls, polt.parser.parser.Parser):
                warnings.warn(
                    _(
                        "{entry_point} entry point named {name} "
                        "from {dist} points to class "
                        "{cls} which is not a Parser subclass "
                        "and thus might not work"
                    ).format(
                        entry_point=repr(POLT_PARSER_ENTRY_POINT),
                        name=repr(entry_point.name),
                        cls=parser_cls,
                        dist=repr(
                            entry_point.dist or _("unknown distribution")
                        ),
                    )
                )
        except BaseException as e:
            warnings.warn(
                _(
                    "Skipping {entry_point} entry point named {name} "
                    "from {dist} pointing to {obj} which is "
                    "obviously not a type: {err}"
                ).format(
                    entry_point=repr(POLT_PARSER_ENTRY_POINT),
                    name=repr(entry_point.name),
                    obj=repr(parser_cls),
                    err=e,
                    dist=repr(entry_point.dist or _("unknown distribution")),
                )
            )
            continue
        matching_ep = next(
            filter(lambda ep: ep.name == entry_point.name, parsers), None
        )
        if matching_ep:
            warnings.warn(
                _(
                    "{dist1} and {dist2} both define a {entry_point} "
                    "entry point {name}."
                ).format(
                    dist1=repr(matching_ep.dist or _("unknown distribution")),
                    dist2=repr(entry_point.dist or _("unknown distribution")),
                    entry_point=repr(POLT_PARSER_ENTRY_POINT),
                    name=repr(entry_point.name),
                )
            )
        parsers[entry_point] = parser_cls
    return parsers


def parser_aliases(parsers=None):
    """
    Create mapping of aliases to parser classes.

    Args:
        parsers (dict, optional): a mapping of
            :class:`pkg_resources.EntryPoint` instances to parser classes as
            returned by :func:`get_parsers`. Defaults to the return value of
            :func:`get_parsers`.

    Returns:
        dict : mapping of tuples of unique alias strings to parser classes
    """
    if parsers is None:
        parsers = get_parsers()
    parser_aliases = {}
    for entry_point, parser_cls in sorted(
        parsers.items(),
        key=lambda x: (
            "0" if x[0].module_name.startswith("polt") else str(x[0])
        ),
    ):

        aliases = []
        full = (
            ".".join(filter(bool, (entry_point.module_name, a)))
            for a in entry_point.attrs
        )
        for alias in filter(
            bool, (entry_point.name, *entry_point.attrs, *full)
        ):
            if any(alias in a for a in parser_aliases):
                continue
            aliases.append(alias)
        parser_aliases[tuple(aliases)] = parser_cls
    return parser_aliases
