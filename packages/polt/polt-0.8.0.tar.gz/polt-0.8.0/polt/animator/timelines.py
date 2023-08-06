# system modules
import functools
import collections
import logging
import inspect
import datetime
import operator
import re

# internal modules
from polt.animator.lines import LinesAnimator

# external modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date

logger = logging.getLogger(__name__)


class TimeLinesAnimator(LinesAnimator):
    """
    Animator to display recieved data as lines.

    Args:
        args, kwargs: further arguments handed to the
            :any:`LinesAnimator` constructor.
        extrapolate (bool, optional): whether to extrapolate values (constant).
            Default is no extrapolation.
        share_time_axis (str, optional): whether to share the time axes.
            Default is ``True``.
        time_frame (int, optional): displayed time frame in seconds. By default
            (``None``), all times are diplayed.
        time_frame_buffer_ratio (float, optional): percentage of the time frame
            to expand the time axis into the future.
        show_data_rate (bool, optional): Whether to display the displayed data
            rate in the legend label. Defaults to ``False``.
    """

    def __init__(
        self,
        *args,
        extrapolate=None,
        share_time_axis=None,
        time_frame=None,
        time_frame_buffer_ratio=None,
        show_data_rate=None,
        **kwargs
    ):
        LinesAnimator.__init__(self, *args, **kwargs)
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def extrapolate(self):
        """
        Whether to extrapolate values constantly

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o extrapolate=yes|no``

        :type: :class:`bool`
        """
        try:
            self._extrapolate
        except AttributeError:
            self._extrapolate = False
        return self._extrapolate

    @extrapolate.setter
    def extrapolate(self, new):
        self._extrapolate = new == "yes" if isinstance(new, str) else bool(new)

    @property
    def share_time_axis(self):
        """
        Whether to share all time axes

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o share-time-axis=yes|no``

        :type: :class:`bool`
        """
        try:
            self._share_time_axis
        except AttributeError:
            self._share_time_axis = True
        return self._share_time_axis

    @share_time_axis.setter
    def share_time_axis(self, new):
        self._share_time_axis = (
            new == "yes" if isinstance(new, str) else bool(new)
        )

    @property
    def time_frame(self):
        """
        Time frame to display in seconds. Data outside the displayed window
        will be dropped.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o time-frame=SECONDS``

        :type: :class:`int` or ``None``
        """
        try:
            self._time_frame
        except AttributeError:
            self._time_frame = None
        return self._time_frame

    @time_frame.setter
    def time_frame(self, new):
        self._time_frame = int(new)

    @property
    def time_frame_buffer_ratio(self):
        """
        Percentage of the time frame to expand the time axis into the future.
        Default is ``0.5`` which means 50%.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o time-frame-buffer-ratio=RATIO``

        :type: :class:`float`
        """
        try:
            self._time_frame_buffer_ratio
        except AttributeError:
            self._time_frame_buffer_ratio = 0.5
        return self._time_frame_buffer_ratio

    @time_frame_buffer_ratio.setter
    def time_frame_buffer_ratio(self, new):
        assert new, "time_frame_buffer_ratio must be a positive float"
        self._time_frame_buffer_ratio = abs(float(new))

    @property
    def show_data_rate(self):
        """
        Whether to show the displayed data rate in the legend label. The
        default is ``False``.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o show-data-rate=yes|no``

        :type: :class:`bool`
        """
        try:
            self._show_data_rate
        except AttributeError:
            self._show_data_rate = False
        return self._show_data_rate

    @show_data_rate.setter
    def show_data_rate(self, new):
        self._show_data_rate = (
            new == "yes" if isinstance(new, str) else bool(new)
        )

    def update_figure_with_dataset(self, dataset):
        """
        Update the figure with a single dataset

        Args:
            dataset (dict): the dataset to update the :attr:`figure` with
        """
        logger.debug(_("Updating the figure with dataset {}").format(dataset))
        now = datetime.datetime.utcnow()
        time_recieved_utc = dataset.pop("time_recieved_utc", now)
        parser = dataset.pop("parser", None)
        data = dataset.pop("data", {})
        for quant, val in data.items():
            if val is None:
                continue
            quantiter = iter((quant,) if isinstance(quant, str) else quant)
            quantity, unit, key = (next(quantiter, None) for i in range(3))
            props = {
                "parser": parser,
                "quantity": quantity,
                "unit": unit,
                "key": key,
            }
            times = (
                [time_recieved_utc] * len(val)
                if isinstance(val, collections.Sequence)
                else time_recieved_utc
            )
            if isinstance(val, str):
                logger.debug(
                    _("Cannot plot string value {}").format(repr(val))
                )
                continue
            ax = next(self.matching_axes(props), None)
            if ax is not None:
                logger.debug(
                    _("Axes matching properties {} is {}").format(props, ax)
                )
            else:
                logger.debug(_("Didn't find matching axes. Adding new."))
                restrictions = {}
                if self.subplots_for is not None:
                    restrictions[self.subplots_for] = props[self.subplots_for]
                add_axes_kwargs = {}
                if self.share_time_axis:
                    first_ax = next(iter(self.figure.axes), None)
                    if first_ax:
                        add_axes_kwargs.update(sharex=first_ax)
                ax = self.add_axes(
                    restrictions=restrictions, **add_axes_kwargs
                )
                tz = plt.rcParams["timezone"]
                ax.set_xlabel("{} [{}]".format(_("time"), tz))
                ax.set_ylabel(_("value"))
            if not hasattr(ax, "units"):
                ax.units = set()
            if unit not in ax.units:
                ax.units.add(unit)
                ax.set_ylabel(
                    " ".join(
                        [
                            _("value"),
                            " ".join(
                                "[{}]".format(unit)
                                for unit in sorted(
                                    u if u is not None else _("unitless")
                                    for u in ax.units
                                )
                            ),
                        ]
                    )
                )
            line = next(self.matching_line(props), None)
            if line:
                logger.debug(
                    _("Line on {} matching {} is {}").format(ax, props, line)
                )
                x, y = line.get_xdata(), line.get_ydata()
                if (
                    line.last_extrapolated
                    if hasattr(line, "last_extrapolated")
                    else False
                ):
                    # if last value is just extrapolated, drop it
                    x = x[:-1]
                    y = y[:-1]
                x = np.append(x, times)
                y = np.append(y, val)
                line.set_xdata(x)
                line.set_ydata(y)
                line.last_extrapolated = False
                ax.relim()
                ax.autoscale_view()
            else:
                logger.debug(
                    _("No line on {} matches {}. Plotting new.").format(
                        ax, props
                    )
                )
                first_line = not bool(ax.get_lines())
                lines = ax.plot(
                    times,
                    val,
                    label=" ".join(
                        ([quantity] if quantity else [])
                        + ([key] if key else [])
                        + (["[{}]".format(unit)] if unit else [])
                        + (["({})".format(parser)] if parser else [])
                    ),
                )
                for cur_line in lines:
                    cur_line.restrictions = {
                        k: v
                        for k, v in props.items()
                        if k not in ax.restrictions
                    }
                if first_line:
                    time_frame = datetime.timedelta(
                        seconds=int(self.time_frame) if self.time_frame else 10
                    )
                    try:
                        iter(times)
                        if len(times) > 1:
                            ax.set_xlim(now)
                        else:
                            ax.set_xlim(now, now + time_frame)
                    except TypeError:
                        ax.set_xlim(now, now + time_frame)
                ax.legend()

    @LinesAnimator.register_method("after-adding-axes")
    def autofmt_xdate(self, *args, **kwargs):
        """
        Pretty-format the xaxis dates with
        :meth:`matplotlib.figure.Figure.autofmt_xdate` after resetting the
        x-axis tick params on all axes.

        Args:
            args, kwargs: just accept further arguments that might come in from
                the registering
        """
        for ax in self.figure.axes:
            ax.tick_params("x", reset=True)
        self.figure.autofmt_xdate()

    @LinesAnimator.register_method("after-each-frame")
    def update_data_rate_in_legends(self, *args, **kwargs):
        """
        If :any:`show_data_rate` is ``True``, update the displayed data rate in
        each line's legend.
        """
        now = datetime.datetime.utcnow()
        for ax in self.figure.axes:
            for line in ax.get_lines():
                if self.show_data_rate:
                    x = line.get_xdata()
                    if (
                        line.last_extrapolated
                        if hasattr(line, "last_extrapolated")
                        else False
                    ):
                        x = x[:-1]
                    tdiff = (max(x.max(), now) - x.min()).total_seconds()
                    rate = max(x.size - 1, 0) / tdiff if tdiff > 0 else 0
                    rate_val, rate_str = (
                        (1 / rate, _("sec/ds"))
                        if (0 < rate < 1)
                        else (rate, _("Hz"))
                    )
                    rate_text = "({:.1f} {})".format(rate_val, rate_str)
                    rate_text_pattern = r"\([^)]+?({}|{})\)".format(
                        re.escape(_("Hz")), re.escape(_("sec/ds"))
                    )
                    old_label = new_label = line.get_label()
                    if re.search(rate_text_pattern, old_label):
                        new_label = re.sub(
                            rate_text_pattern, rate_text, old_label
                        )
                    else:
                        new_label += " " + rate_text
                    if old_label != new_label:
                        line.set_label(new_label)
                        ax.legend()

    @LinesAnimator.register_method("after-each-frame")
    def drop_old_values(self, *args, **kwargs):
        """
        If a :any:`time_frame` is set, drop values that are too old from all
        lines.
        """
        for ax in self.figure.axes:
            for line in ax.get_lines():
                # drop outside values to the left
                if self.time_frame:
                    lower, upper = ax.get_xlim()
                    x, y = line.get_xdata(), line.get_ydata()
                    outside = date2num(x) < lower
                    outside_ind = np.where(outside)[0]
                    if outside_ind.size:
                        line.set_xdata(np.delete(x, outside_ind[:-1]))
                        line.set_ydata(np.delete(y, outside_ind[:-1]))

    @LinesAnimator.register_method("after-each-frame")
    def extrapolate_lines(self, *args, **kwargs):
        """
        If :any:`extrapolate` is ``True``, extrapolate all lines constantly.
        """
        now = datetime.datetime.utcnow()
        for ax in self.figure.axes:
            for line in ax.get_lines():
                if self.extrapolate:
                    x, y = line.get_xdata(), line.get_ydata()
                    if len(x) == 1:
                        x = np.append(x, now)
                        y = np.append(y, y[-1])
                    elif len(x) > 1:
                        if (
                            line.last_extrapolated
                            if hasattr(line, "last_extrapolated")
                            else False
                        ):
                            x[-1] = now
                        else:
                            x = np.append(x, now)
                            y = np.append(y, y[-1])
                    else:
                        continue
                    line.last_extrapolated = True
                    line.set_xdata(x)
                    line.set_ydata(y)

    @LinesAnimator.register_method("after-each-frame")
    def adjust_time_axis_limits(self, *args, **kwargs):
        now = datetime.datetime.utcnow()
        for ax in self.figure.axes:
            new_lower, new_upper = lower, upper = tuple(
                map(
                    lambda x: num2date(x)
                    .astimezone(datetime.timezone.utc)
                    .replace(tzinfo=None),
                    ax.get_xlim(),
                )
            )
            past_diff = now - lower
            future_diff = upper - now
            future_ratio = future_diff / past_diff
            if not 0 < future_ratio < self.time_frame_buffer_ratio:
                while not new_upper > now:
                    new_upper += past_diff * self.time_frame_buffer_ratio
            if self.time_frame is not None:
                new_lower = new_upper - datetime.timedelta(
                    seconds=int(self.time_frame)
                )
            if new_lower != lower or new_upper != upper:
                ax.set_xlim(*map(date2num, (new_lower, new_upper)))
            if self.share_time_axis:
                break
