# system modules
import logging
import importlib
import subprocess
import shlex
import multiprocessing
import sys

# internal modules
import polt
from polt.cli.commands.main import cli

# external modules
import click

logger = logging.getLogger(__name__)

subplots_for_choices = {"parser", "quantity", "unit", "nothing"}


def input_parser(section):
    parser_spec = section.get("parser")
    if parser_spec:
        parts = parser_spec.split(".")
        try:
            package, classname = ".".join(parts[:-1]), parts[-1]
            module = importlib.import_module(package)
            parser_cls = getattr(module, classname)
        except (IndexError, ImportError, AttributeError):
            logger.error(
                _(
                    "parser specification {parser_spec} in section {section} "
                    "is neither an alias (like {aliases}) "
                    "nor an importable class specification"
                ).format(
                    parser_spec=repr(parser_spec),
                    section=repr(section.name),
                    aliases=", ".join(map(repr, available_parsers)),
                )
            )
            sys.exit(1)
        if not issubclass(parser_cls, polt.parser.Parser):
            logger.warning(
                _(
                    "Specified parser class {spec_class} is not a subclass "
                    "of {parser_class} and might not work."
                ).format(
                    spec_class=parser_cls, parser_class=polt.parser.Parser
                )
            )
    else:
        logger.error(
            _("Section {section} does not specify a 'parser'").format(
                repr(section=section.name)
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
                        _("Command {cmd} is already done").format(
                            cmd=repr(cmd)
                        )
                    )
                else:
                    logger.error(
                        _(
                            "Running {cmd} did not work (return code {code})"
                        ).format(cmd=repr(cmd), code=returncode)
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
    source_text = _("stdin") if cmd == "-" else repr(cmd)
    parser = parser_cls(
        f,
        name=section.get("name")
        or _("{} from {}").format(
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
                ).format(
                    prop=repr(prop),
                    val=repr(val),
                    parser=repr(parser),
                    err=repr(e),
                )
            )
    return parser


@cli.command(
    help="\n\n".join(
        (
            _("plot live data"),
            _(
                "This command parses the current configuration, "
                "sets up all parsers with their respective sources "
                "and launches the interactive plot window."
            ),
        )
    ),
    short_help=_("plot live data"),
)
@click.option(
    "-i",
    "--interval",
    metavar=_("milliseconds").upper(),
    help=_("plot update interval"),
    type=click.IntRange(min=1, clamp=True),
)
@click.option(
    "--subplots-for",
    metavar=_("property").upper(),
    help=_("for which property ({quantities}) to create subplots for").format(
        quantities=", ".join(map(repr, subplots_for_choices))
    ),
    type=click.Choice(subplots_for_choices, case_sensitive=False),
    show_choices=True,
)
@click.option(
    "--extrapolate/--dont-extrapolate",
    help=_(
        "Extrapolate values (constantly). By default, when --extrapolate is "
        "not given, no extrapolation is performed and lines are not continued "
        "constantly"
    ),
    default=None,
    is_flag=True,
)
@click.option(
    "--soft-shutdown/--hard-shutdown",
    "soft_shutdown",
    help=_("Shut down input threads gracefully"),
    default=None,
    is_flag=True,
)
@click.option(
    "-n",
    "--no-plot",
    help=_("Don't actually do any live plotting, just set the configuration"),
    default=False,
    is_flag=True,
)
@click.pass_context
def live(ctx, interval, extrapolate, subplots_for, soft_shutdown, no_plot):
    config = ctx.obj["config"]
    config.update_option("plot", "interval", interval, 200)
    config.update_option("plot", "extrapolate", extrapolate, False)
    config.update_option("plot", "subplots-for", subplots_for, "nothing")
    config.update_option("plot", "soft-shutdown", soft_shutdown, False)

    if no_plot:
        logger.info(_("Skip plotting as requested via command-line"))
        return

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
                interval=config.getint("plot", "interval", fallback=200),
                extrapolate=config.getboolean(
                    "plot", "extrapolate", fallback=False
                ),
                subplots_for=config.get("plot", "subplots-for", fallback=None),
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
            name=_("PlotProcess"),
        )
        try:
            logger.debug(_("Starting plot process"))
            p.start()
            logger.info(_("plot process started"))
            logger.debug(_("starting parsing threads"))
            for streamer in streamers:
                logger.debug(
                    _("starting parsing thread {}").format(streamer.name)
                )
                streamer.start()
            logger.info(_("parsing threads started"))
            p.join()
            logger.debug(_("Plot process exited"))
        except KeyboardInterrupt:
            logger.info(_("User wants to stop"))
        if config.getboolean("plot", "soft-shutdown", fallback=False):
            logger.info(_("shutting down gracefully"))
            try:
                for streamer in streamers:
                    streamer.stop()
                    logger.debug(
                        _("Waiting for thread {} to close").format(
                            streamer.name
                        )
                    )
                    streamer.join()
            except KeyboardInterrupt:
                logger.info(_("Okay, okay, stopping now..."))

    logger.info(_("live plotting done"))
