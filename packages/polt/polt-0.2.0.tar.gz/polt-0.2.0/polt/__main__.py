#!/usr/bin/env python3
# system modules
import argparse
import logging
import os
import sys
import itertools
import select
import datetime
import multiprocessing
import subprocess
import shlex
import configparser
import time
import re
import importlib

# internal modules
import polt

# external modules
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import xdgspec


def existing_file(arg):
    if os.path.isfile(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError(
            "File {} does not exist".format(repr(arg))
        )


def yes(arg):
    return arg if arg.lower().strip() == "no" else "yes"


available_parsers = {
    cls.__name__: cls for cls in polt.parser.Parser.__subclasses__()
}


def source_spec(arg):
    parts = arg.split(":")
    if len(parts) == 1:
        cmd = parts[0]
        parser_spec = "NumberParser"
    elif len(parts) >= 2:
        parser_spec, cmd = parts[0], ":".join(parts[1:])
    else:
        raise argparse.ArgumentTypeError(_("You should never see this..."))
    if not polt.utils.normalize_cmd(cmd):
        raise argparse.ArgumentTypeError(
            _("Empty source ({})").format(repr(cmd))
        )
    parser_cls = available_parsers.get(parser_spec)
    if not parser_cls:
        parts = parser_spec.split(".")
        try:
            package, classname = ".".join(parts[:-1]), parts[-1]
            module = importlib.import_module(package)
            parser_cls = getattr(module, classname)
        except (IndexError, ImportError, AttributeError, ValueError) as e:
            raise argparse.ArgumentTypeError(
                _(
                    "parser specification {p} (for source {s}) "
                    "is neither a native parser (like {aliases}) "
                    "nor an importable class specification ({err})"
                    ""
                ).format(
                    p=repr(parser_spec),
                    s=repr(cmd),
                    aliases=", ".join(map(repr, available_parsers)),
                    err=e,
                )
            )
    return (parser_spec, cmd)


def regex(arg):
    try:
        return re.compile(arg, flags=re.IGNORECASE)
    except (ValueError, TypeError) as e:
        raise argparse.ArgumentTypeError(
            _("{regex} is not a valid regular expression: {error}").format(
                regex=repr(arg), error=e
            )
        )


user_config_file = os.path.join(
    xdgspec.XDGPackageDirectory("XDG_CONFIG_HOME", "polt").path, "polt.conf"
)
local_config_file = ".polt.conf"

argparser = argparse.ArgumentParser(
    prog="python3 -m polt",
    add_help=False,
    description="polt - {}".format(
        _("Live Data Visualisation via Matplotlib")
    ),
    epilog=_(
        "If no sources are specified, numbers are read from stdin. "
        "You can customize the plot via the Matplotlib `matplotlibrc` file. "
        "See https://matplotlib.org/users/customizing.html "
        "for further information."
    ),
)
generalgroup = argparser.add_argument_group(title=_("General Options"))
generalgroup.add_argument(
    "--version",
    action="store_true",
    help=_("show program's version number and exit"),
)
generalgroup.add_argument(
    "-h", "--help", help=_("show this help page and exit"), action="store_true"
)
configgroup = argparser.add_argument_group(
    title=_("Configuration Options"),
    description=_("These options control how configuration is managed"),
)
configgroup.add_argument(
    "--no-config",
    action="store_true",
    help=_("Don't read default configuration file(s) ({} and {})").format(
        repr(user_config_file), repr(local_config_file)
    ),
)
configgroup.add_argument(
    "-c",
    "--config",
    metavar="file",
    nargs="+",
    help=_("Extra configuration file(s) to read (after {} and {})").format(
        repr(user_config_file), repr(local_config_file)
    ),
    type=existing_file,
    default=[],
)
configgroup.add_argument(
    "--save-config",
    metavar="file",
    nargs="?",
    help=_(
        "Save the current configuration into this file. "
        "If this option is specified without further arguments, "
        "{} is used."
    ).format(repr(local_config_file)),
    const=local_config_file,
)
loggroup = argparser.add_argument_group(
    title=_("Logging Options"),
    description=_("These options control the amount of output verbosity"),
)
logoptions = loggroup.add_mutually_exclusive_group()
logoptions.add_argument(
    "-v", "--verbose", help=_("verbose output"), action="store_true"
)
logoptions.add_argument(
    "-q", "--quiet", help=_("only show warnings"), action="store_true"
)
inputgroup = argparser.add_argument_group(
    title=_("Input Options"),
    description=_("These options control from where and how data is read"),
)
inputgroup.add_argument(
    "--source",
    metavar=(_("[parser:]source")),
    type=source_spec,
    action="append",
    help=_(
        "Add a 'source' to read data from by parsing with 'parser'. "
        "Specify a dash (-) for 'source' to read from stdin. "
        "The 'parser' may either be one of the native parsers {} "
        "or a class path specification (like 'mypackage.MyParser') "
        "pointing to "
        "a subclass of 'polt.parser.Parser'. "
        "When 'parser' is left out, the default (polt.parser.NumberParser) "
        "is used to just extract any numbers."
    ).format(", ".join(map(repr, available_parsers))),
    default=[],
)
csvregexgroup = inputgroup.add_mutually_exclusive_group()
csvregexgroup.add_argument(
    "--csv-unit-last",
    help=_(
        "Extract units as the last part of the " "header fields in CSV sources"
    ),
    action="store_true",
)
csvregexgroup.add_argument(
    "--csv-header-regex",
    nargs=1,
    metavar=_("REGULAR-EXPRESSION"),
    help=_("Regular expression to parse CSV headers"),
    type=regex,
)
inputgroup.add_argument(
    "--soft-shutdown",
    help=_("Shut down input threads gracefully"),
    action="store_true",
)
plotoptions = argparser.add_argument_group(
    title=_("Plot Options"), description=_("These options control the plot")
)
plotoptions.add_argument(
    "--interval",
    metavar=(_("milliseconds")),
    help=_("plot update interval [default:200]"),
    type=lambda x: max(int(x), 1),  # minimum 1ms, below does not work
)
plotoptions.add_argument(
    "--subplots-for",
    metavar=(_("property")),
    help=_(
        "for which quantity ('parser', 'quantity', 'unit') to create "
        "subplots for"
    ),
    choices={"parser", "quantity", "unit", "nothing"},
)
plotoptions.add_argument(
    "--extrapolate",
    nargs="?",
    choices={"yes", "no"},
    help=_(
        "Extrapolate values (constant). By default, when --extrapolate is "
        "not given, no extrapolation is performed and lines are not continued "
        "constantly"
    ),
    type=yes,
    default=None,
    const="yes",
)
args = argparser.parse_args()

if args.help:
    argparser.print_help()
    sys.exit(0)

if args.version:
    print("polt v{}".format(polt.__version__))
    sys.exit(0)

# set up logging
loglevel = logging.DEBUG if args.verbose else logging.INFO
loglevel = logging.WARNING if args.quiet else loglevel
logging.basicConfig(
    level=loglevel,
    format="%(processName)s %(threadName)s  "
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("polt-cli")
for n, l in logger.manager.loggerDict.items():
    if not n.startswith("polt"):
        l.propagate = False

# initialise the configuration
config = polt.config.Configuration()
# read configuration files
config.read(
    ([] if args.no_config else [user_config_file, local_config_file])
    + args.config
)
# merge command-line arguments into the configuration
if "plot" not in config:
    config.add_section("plot")
if args.interval is None:
    if "interval" not in config["plot"]:
        config["plot"]["interval"] = str(200)
else:
    config["plot"]["interval"] = str(args.interval)
if args.extrapolate is None:
    if "extrapolate" not in config["plot"]:
        config["plot"]["extrapolate"] = "no"
else:
    config["plot"]["extrapolate"] = args.extrapolate
if args.subplots_for is not None:
    if args.subplots_for == "nothing":
        config.remove_option("plot", "subplots_for")
    else:
        config["plot"]["subplots_for"] = args.subplots_for


# merge command-line source commands into the configuration
for parser_spec, cmd in polt.utils.flatten(args.source):
    matching_sections = list(config.matching_source_section(command=cmd))
    for section in matching_sections:
        logger.warning(
            _(
                "Removing configuration section {section} because it matches "
                "the given command-line source command {clicmd}."
            ).format(
                clicmd=repr(cmd),
                section=_("{} (parsing {} from {})").format(
                    repr(section.name),
                    section.get("parser"),
                    repr(section.get("command")),
                ),
            )
        )
        config.remove_section(section.name)
    section_name = "{}:{}".format(
        config.SOURCE_SECTION_PREFIX,
        "stdin" if cmd == "-" else polt.utils.normalize_cmd(cmd),
    )
    config.add_section(section_name)
    config[section_name]["command"] = cmd
    config[section_name]["parser"] = parser_spec
    if issubclass(
        available_parsers.get(parser_spec, object), polt.parser.CsvParser
    ):
        if args.csv_unit_last:
            config[section_name][
                "parser.header_regex"
            ] = polt.parser.CsvParser.HEADER_REGEX_UNIT_LAST.pattern
        if args.csv_header_regex:
            config[section_name]["parser.header_regex"] = next(
                iter(args.csv_header_regex)
            ).pattern


# save configuration if desired
if args.save_config is not None:
    config_file = args.save_config
    directory, name = os.path.split(config_file)
    directory = os.path.expanduser(directory)
    logger.info(
        _("Saving current configuration to file {}").format(repr(config_file))
    )
    if directory:
        if not os.path.exists(directory):
            logger.warning(
                _("Create nonexistent directory {}").format(directory)
            )
            os.makedirs(directory)
    with open(config_file, "w") as f:
        config.write(f)
    logger.debug(
        _("Current configuration successfully saved to file {}").format(
            config_file
        )
    )


def input_parser(section):
    parser_spec = section.get("parser")
    if parser_spec:
        parser_cls = available_parsers.get(parser_spec)
        if not parser_cls:
            logger.debug(
                _(
                    "{} is not a native parser. "
                    "Trying to interpret it as a class path specification"
                ).format(parser_spec)
            )
            parts = parser_spec.split(".")
            try:
                package, classname = ".".join(parts[:-1]), parts[-1]
                module = importlib.import_module(package)
                parser_cls = getattr(module, classname)
            except (IndexError, ImportError, AttributeError):
                logger.error(
                    _(
                        "parser specification {p} in section {s} "
                        "is neither an alias (like {aliases}) "
                        "nor an importable class specification"
                    ).format(
                        p=repr(parser_spec),
                        s=repr(section.name),
                        aliases=", ".join(map(repr, available_parsers)),
                    )
                )
                sys.exit(1)
            if not isinstance(parser_cls, polt.parser.Parser):
                logger.warning(
                    _(
                        "Specified parser class {} is not a subclass "
                        "of {} and might not work."
                    ).format(parser_cls, polt.parser.Parser)
                )
    else:
        logger.error(
            _("Section {} does not specify a 'parser'").format(
                repr(section.name)
            )
        )
        sys.exit(1)
    cmd = section.get("command")
    if cmd:
        if cmd == "-":  # stdin
            f = sys.stdin
        else:  # a command
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            try:
                returncode = process.wait(timeout=0.5)
                if returncode == 0:
                    logger.warning(
                        _("Command {} is already done").format(repr(cmd))
                    )
                else:
                    logger.error(
                        _("Running {} did not work (return code {})").format(
                            repr(cmd), returncode
                        )
                    )
                    sys.exit(1)
            except subprocess.TimeoutExpired:  # still running
                logger.info(_("Successfully started {}").format(repr(cmd)))
            f = process.stdout
    else:
        logger.error(
            _("Section {} does not specify a 'command'").format(
                repr(section.name)
            )
        )
        sys.exit(1)
    source_text = "stdin" if cmd == "-" else repr(cmd)
    parser = parser_cls(
        f,
        name=_("{} from {}").format(
            {"NumberParser": _("numbers"), "CsvParser": _("csv")}.get(
                parser_spec, parser_spec
            ),
            {"stdin": _("standard input")}.get(source_text, source_text),
        ),
    )
    # set further properties
    configured_parser_properties = {
        k.split(".")[1]: v
        for k, v in section.items()
        if (k.startswith("parser.") and k.split(".")[1])
    }
    for prop, val in configured_parser_properties.items():
        try:
            logger.debug(
                _("Setting {parser}.{prop} to {val}").format(
                    prop=repr(prop), val=repr(val), parser=repr(parser)
                )
            )
            setattr(parser, prop, val)
        except BaseException as e:
            logger.warning(
                _(
                    "Could not set attribute {prop} to {val} "
                    "on parser {parser}: {err}"
                ).format(prop=repr(prop), val=repr(val), parser=repr(parser))
            )
    return parser


# set up parsers from configuration
parsers = list(map(input_parser, config.source_section))

if not parsers:
    logger.info(
        " ".join(
            [
                _("No sources specified."),
                _("Falling back to reading numbers from stdin."),
            ]
        )
    )
    parsers = [polt.parser.NumberParser(sys.stdin)]

with multiprocessing.Manager() as manager:

    def animate_process(buf):
        logger.debug(_("Creating Animator"))
        animator = polt.animator.Animator(
            buffer=buf,
            interval=config.getint("plot", "interval"),
            extrapolate=config.getboolean("plot", "extrapolate"),
            subplots_for=config.get("plot", "subplots_for", fallback=None),
        )

        logger.info(_("Running Animator"))
        animator.run()
        logger.info(_("Animator is done"))

    buf = manager.list()
    streamers = [polt.streamer.Streamer(parser, buf) for parser in parsers]
    p = multiprocessing.Process(
        target=animate_process,
        daemon=True,
        kwargs={"buf": buf},
        name="PlotProcess",
    )
    try:
        logger.debug(_("Starting plot process"))
        p.start()
        logger.info(_("plot process started"))
        logger.debug(_("starting parsing threads"))
        for streamer in streamers:
            logger.debug(_("starting parsing thread {}").format(streamer.name))
            streamer.start()
        logger.info(_("parsing threads started"))
        p.join()
        logger.debug(_("Plot process exited"))
    except KeyboardInterrupt:
        logger.info(_("User wants to stop"))
    if args.soft_shutdown:
        logger.info(_("shutting down gracefully"))
        try:
            for streamer in streamers:
                streamer.stop()
                logger.debug(
                    _("Waiting for thread {} to close").format(streamer.name)
                )
                streamer.join()
        except KeyboardInterrupt:
            logger.info(_("Okay, okay, stopping now..."))

logger.info(_("done"))
