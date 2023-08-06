# system modules
import logging
import importlib
import subprocess
import shlex
import multiprocessing
import sys
import io

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
        if not issubclass(parser_cls, polt.parser.parser.Parser):
            logger.warning(
                _(
                    "Specified parser class {spec_class} is not a subclass "
                    "of {parser_class} and might not work."
                ).format(
                    spec_class=parser_cls,
                    parser_class=polt.parser.parser.Parser,
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
    encoding = section.get("encoding")
    if cmd:
        if cmd == "-":  # stdin
            if encoding:
                try:
                    f = io.TextIOWrapper(sys.stdin.buffer, encoding=encoding)
                except BaseException as e:
                    logger.error(
                        _(
                            "Could not use given encoding {encoding}: "
                            "{err}. Continuing without changing encoding."
                        ).format(encoding=repr(encoding), err=e)
                    )
                    f = sys.stdin
            else:
                f = sys.stdin
        else:  # a command
            try:
                process = subprocess.Popen(
                    shlex.split(cmd),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
            except BaseException as e:
                logger.error(
                    _("Could not start command {cmd}: {err}").format(
                        cmd=repr(cmd), err=e
                    )
                )
                sys.exit(1)
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
            if encoding:
                try:
                    # for backwards-compatibility with Python < 3.6 we can't
                    # just use the encoding and errors arguments of Popen().
                    # Instead, we use an io.TextIOWrapper here.
                    f = io.TextIOWrapper(
                        process.stdout, encoding=encoding, errors="ignore"
                    )
                except BaseException as e:
                    logger.error(
                        _(
                            "Could not use encoding {encoding} "
                            "for output of {cmd}: {err}"
                        ).format(encoding=repr(encoding), cmd=repr(cmd), err=e)
                    )
                    f = process.stdout
            else:
                f = process.stdout
    else:
        logger.error(
            _("Section {} does not specify a 'command'").format(
                repr(section.name)
            )
        )
        sys.exit(1)
    source_text = _("stdin") if cmd == "-" else repr(cmd)
    parser_name = section.get("name") or _("{parser} on {source}").format(
        parser=parser_spec,
        source={"stdin": _("standard input")}.get(source_text, source_text),
    )
    try:
        parser = parser_cls(f, name=parser_name)
    except BaseException as e:
        logger.error(
            _(
                "Could not instantiate parser {name} "
                "with class {cls}: {err}"
            ).format(
                name=repr(parser_name),
                cls=repr(
                    ".".join((parser_cls.__module__, parser_cls.__name__))
                ),
                err=e,
            )
        )
        return None
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
    help=_(
        "plot update interval. "
        "The smaller the value the smoother the animation will be. "
        "However, too small values might now work depending on your setup."
    ),
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
        "constantly."
    ),
    default=None,
    is_flag=True,
)
@click.option(
    "--shared-time/--separate-time",
    help=_("Whether to share the time axis. Default is yes."),
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
    "--time-frame",
    help=_(
        "Displayed time frame in seconds. "
        "Specifying this causes graphs to behave like a moving window, only "
        "displaying the bounded time span and forgetting values "
        "outside this span. "
        "The default is no display everything. "
        "Keep in mind that without this option "
        "this program's RAM usage can grow indefinitely."
    ),
    default=None,
    metavar=_("seconds").upper(),
    type=click.IntRange(min=1, clamp=True),
)
@click.option(
    "--time-buffer",
    help=_(
        "What percentage of the displayed time frame to "
        "expand the time axis when necessary. "
        "The default is 0.5 which the time axis will be enlarged by half of "
        "the current span when the current time lies no longer within. "
        "Note that specifying values larger than 1 in combination with "
        "--time-frame will lead to times where no graph is displayed."
    ),
    default=0.5,
    metavar=_("ratio").upper(),
    type=click.FloatRange(min=0.01, clamp=True),
)
@click.option(
    "-n",
    "--no-plot",
    help=_("Don't actually do any live plotting, just set the configuration"),
    default=False,
    is_flag=True,
)
@click.pass_context
def live(
    ctx,
    interval,
    extrapolate,
    subplots_for,
    soft_shutdown,
    no_plot,
    shared_time,
    time_buffer,
    time_frame,
):
    config = ctx.obj["config"]
    config.update_option("plot", "interval", interval, 200)
    config.update_option("plot", "extrapolate", extrapolate, False)
    config.update_option("plot", "subplots-for", subplots_for, "nothing")
    config.update_option("plot", "soft-shutdown", soft_shutdown, False)
    config.update_option("plot", "shared-time", shared_time, True)
    config.update_option("plot", "time-buffer", time_buffer)
    config.update_option("plot", "time-frame", time_frame)

    if time_frame and time_buffer:
        if time_buffer > 1:
            logger.warning(
                _(
                    "Using a time buffer ratio greater "
                    "than 1 (--time-buffer={time_buffer}) when specifying "
                    "a time frame (--time-frame={time_frame}) "
                    "will result in the graph being invisible for some "
                    "time which is probabily not what you want."
                ).format(time_buffer=time_buffer, time_frame=time_frame)
            )

    if no_plot:
        logger.info(_("Skip plotting as requested via command-line"))
        return

    parsers = list(filter(bool, map(input_parser, config.source_section)))

    if not parsers:
        logger.info(
            " ".join(
                [
                    _("No sources specified."),
                    _("Falling back to reading numbers from stdin."),
                ]
            )
        )
        if sys.stdin.isatty():
            click.echo(
                _(
                    "You may now repeatedly type any numbers "
                    "and press <Enter>."
                )
            )
        parsers = [polt.parser.numberparser.NumberParser(sys.stdin)]

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
                share_time_axis=config.get(
                    "plot", "shared-time", fallback=None
                ),
                time_frame_buffer_ratio=config.getfloat(
                    "plot", "time-buffer", fallback=None
                ),
                time_frame=config.getint("plot", "time-frame", fallback=None),
            )

            logger.debug(_("Running Animator"))
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
            logger.debug(_("plot process started"))
            logger.debug(_("starting parsing threads"))
            for streamer in streamers:
                logger.debug(
                    _("starting parsing thread {}").format(streamer.name)
                )
                streamer.start()
            logger.debug(_("parsing threads started"))
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
