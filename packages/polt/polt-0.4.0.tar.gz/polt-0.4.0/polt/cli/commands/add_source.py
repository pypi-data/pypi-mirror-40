# system modules
import logging
import re
import itertools
import importlib
import shlex
import shutil

# internal modules
import polt
from polt.cli.commands.main import cli

# external modules
import click

logger = logging.getLogger(__name__)

parser_aliases = polt.parser.parser_aliases()
short_parser_aliases = tuple(
    map(
        repr,
        sorted(filter(bool, (next(iter(a), None) for a in parser_aliases))),
    )
)


def parser_spec(ctx, param, value):
    if value is None:
        return value
    matching_alias_cls = next(
        (cls for aliases, cls in parser_aliases.items() if value in aliases),
        None,
    )
    if matching_alias_cls:
        parser_cls = matching_alias_cls
    else:
        parts = value.split(".")
        try:
            package, classname = ".".join(parts[:-1]), parts[-1]
            if package:
                module = importlib.import_module(package)
                parser_cls = getattr(module, classname)
            else:
                parser_cls = parser_aliases[classname]
        except (
            IndexError,
            ImportError,
            AttributeError,
            ValueError,
            KeyError,
        ) as e:
            raise click.BadParameter(
                _(
                    "parser specification {spec} "
                    "is neither a native parser (like {native_parsers}) "
                    "nor an importable class specification ({error})"
                    ""
                ).format(
                    spec=repr(value),
                    native_parsers=polt.l10n.join(
                        short_parser_aliases, last_sep=" {} ".format(_("or"))
                    ),
                    error=e,
                ),
                ctx=ctx,
                param=param,
            )
    path = ".".join((parser_cls.__module__, parser_cls.__name__))
    return path


def cmd_spec(ctx, param, value):
    if value in ("-", "stdin", None):
        return value
    executable = next(iter(shlex.split(value)), None)
    if shutil.which(executable or ""):
        return value
    else:
        raise click.BadParameter(
            _(
                "could not find executable {executable} "
                "from given command {value}"
            ).format(executable=repr(executable), value=repr(value)),
            param=param,
            ctx=ctx,
        )


def option_spec(ctx, param, value):
    part = iter(value.split("=", maxsplit=1))
    attr, value = next(part, ""), next(part, "")
    if attr:
        return re.sub(r"\W+", "_", attr), value
    else:
        raise click.BadParameter(
            _(
                "specify an option like {option}={value}, not like {given}"
            ).format(
                option=_("option").upper(),
                value=_("value").upper(),
                given=repr(value),
            ),
            param=param,
            ctx=ctx,
        )


def options_spec(ctx, param, value):
    return dict(map(lambda x: option_spec(ctx, param, x), value))


@cli.command(help=_("add a new data source"))
@click.option(
    "-p",
    "--parser",
    metavar=_("class").upper(),
    callback=parser_spec,
    help=_(
        "parser class to use. "
        "This can be a built-in parser ({native_parsers}) "
        "or a class specification to a subclass of Parser "
        "(like 'mypackage.MyParser')"
    ).format(
        native_parsers=polt.l10n.join(
            short_parser_aliases, last_sep=" {} ".format(_("or"))
        )
    ),
)
@click.option("-n", "--name", help=_("human-readable name for this parser"))
@click.option(
    "-c",
    "--cmd",
    metavar=_("command").upper(),
    callback=cmd_spec,
    help=_(
        "the command to use as source for the parser. "
        "The default is to use data from stdin."
    ),
)
@click.option(
    "-e",
    "--encoding",
    metavar=_("encoding").upper(),
    help=_(
        "the encoding to use to decode the data. "
        "The default is no encoding which means to pass raw bytes to "
        "the parser."
    ),
)
@click.option(
    "-o",
    "--option",
    "options",
    metavar="{option}={value}".format(
        option=_("option"), value=_("value")
    ).upper(),
    multiple=True,
    callback=options_spec,
    help=_(
        "further options for the parser. "
        "Multiple specifications of this option are possible. "
        "The parser's attribute {option} "
        "will be set to the string {value}."
    ).format(option=_("option").upper(), value=_("value").upper()),
)
@click.pass_context
def add_source(ctx, parser, cmd, options, name, encoding):
    if not (parser or cmd):
        raise click.UsageError(
            _("Specify at least either --parser or --cmd"), ctx=ctx
        )
    if parser is None:
        parser = polt.parser.numberparser.NumberParser
        parser = ".".join((parser.__module__, parser.__name__))
    if cmd is None:
        cmd = "-"
    config = ctx.obj["config"]
    matching_sections = list(config.matching_source_section(command=cmd))
    for section in matching_sections:
        logger.warning(
            _(
                "Removing previously existing configuration section {section} "
                "because it matches the given command-line source command "
                "{clicmd}."
            ).format(
                clicmd=repr(cmd),
                section=_("{section} (parsing {cmd} with {parser})").format(
                    section=repr(section.name),
                    parser=section.get("parser"),
                    cmd=repr(section.get("command")),
                ),
            )
        )
        config.remove_section(section.name)
    section_name = "{}:{}".format(
        config.SOURCE_SECTION_PREFIX,
        "stdin" if cmd == "-" else polt.utils.normalize_cmd(cmd),
    )
    config.add_section(section_name)
    config.update_option(section_name, "command", cmd)
    config.update_option(section_name, "parser", parser)
    config.update_option(section_name, "name", name)
    config.update_option(section_name, "encoding", encoding)
    for option, value in options.items():
        config[section_name]["parser.{}".format(option)] = value
