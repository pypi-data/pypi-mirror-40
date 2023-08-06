# system modules
import threading
import functools
import collections
import itertools
import logging
import inspect
import datetime
import operator
import math

# internal modules

# external modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)


class Animator:
    """
    Animator class

    Args:
        figure (matplotlib.figure.Figure, optional): the figure to animate on
        buffer (list-like, optional): the buffer to retrieve
            data from.
        interval (int, optional): the frame update interval in milliseconds.
            Default is 200.
        extrapolate (bool, optional): whether to extrapolate values (constant).
            Default is no extrapolation.
        subplots_for (str, optional): for which metadata property
            (``"parser"``, ``"quantity"``, ``"unit"``) subplots should be
            created. The default is to not use subplots and display all data in
            a single plot.
        share_time_axis (str, optional): whether to share the time axes.
            Default is ``True``.
        time_frame (int, optional): displayed time frame in seconds. By default
            (``None``), all times are diplayed.
        time_frame_buffer_ratio (float, optional): percentage of the time frame
            to expand the time axis into the future.
    """

    def __init__(
        self,
        figure=None,
        buffer=None,
        interval=None,
        extrapolate=None,
        subplots_for=None,
        share_time_axis=None,
        time_frame=None,
        time_frame_buffer_ratio=None,
    ):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    def modifies_animation(decorated_function):
        """
        Decorator for methods that require resetting the animation
        """

        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_animation"):
                logger.debug(
                    _("Clearing animation before {}").format(
                        decorated_function
                    )
                )
                del self._animation
            return decorated_function(self, *args, **kwargs)

        return wrapper

    @property
    def buffer(self):
        """
        The buffer to retrieve data from

        :type: list-like
        """
        try:
            self._buffer
        except AttributeError:  # pragma: no cover
            self._buffer = None
        return self._buffer

    @buffer.setter
    def buffer(self, new):
        self._buffer = new

    @property
    def interval(self):
        """
        The frame update interval

        :type: :any:`int`
        """
        try:
            self._interval
        except AttributeError:
            self._interval = 200
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        self._interval = int(new_interval)

    @property
    def figure(self):
        """
        The figure to animate on

        :type: :class:`matplotlib.figure.Figure`
        """
        try:
            self._figure
        except AttributeError:  # pragma: no cover
            self._figure = plt.figure()
        return self._figure

    @figure.setter
    @modifies_animation
    def figure(self, new):
        self._figure = new

    @property
    def extrapolate(self):
        """
        How to extrapolate values
        """
        try:
            self._extrapolate
        except AttributeError:
            self._extrapolate = False
        return self._extrapolate

    @extrapolate.setter
    def extrapolate(self, new):
        self._extrapolate = new

    @property
    def subplots_for(self):
        """
        For which metadata property (``"parser"``, ``"quantity"``, ``"unit"``)
        subplots should be created. The default is to not use subplots and
        display all data in a single plot.

        :type: :class:`str` or ``None``
        """
        try:
            self._subplots_for
        except AttributeError:
            self._subplots_for = None
        return self._subplots_for

    @subplots_for.setter
    def subplots_for(self, new):
        if new is None or new == "nothing":
            if hasattr(self, "_subplots_for"):
                del self._subplots_for
        else:
            self._subplots_for = str(new)

    @property
    def share_time_axis(self):
        """
        Whether to share all time axes

        :type: :class:`bool`
        """
        try:
            self._share_time_axis
        except AttributeError:
            self._share_time_axis = True
        return self._share_time_axis

    @share_time_axis.setter
    def share_time_axis(self, new):
        self._share_time_axis = bool(new)

    @property
    def time_frame(self):
        """
        Time frame to display in seconds

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
    def animation(self):
        """
        The underlying animation

        :type: :class:`matplotlib.animation.FuncAnimation`
        """
        try:
            self._animation
        except AttributeError:
            self._animation = FuncAnimation(
                fig=self.figure,
                init_func=self.clear_figure,
                func=self.update_figure,
                frames=self.dataset,
                interval=self.interval,
                repeat=False,
            )
        return self._animation

    def matching_axes(self, props={}):
        """
        Generator yielding the next axes matching certain data properties

        Args:
            props (dict, optional): dictionary of data properties
                with keys

                source
                    name of the data source
                quantity
                    name of the data quantity
                unit
                    data unit

        Yields:
            matplotlib.axes.Subplot : the next matching axes instance
        """
        for ax in self.figure.axes:
            if all(
                props.get(k) == v
                for k, v in (
                    ax.restrictions if hasattr(ax, "restrictions") else {}
                ).items()
            ):
                yield ax

    def matching_line(self, props={}, ax=None):
        """
        Generator yielding the next line matching a data properties

        Args:
            props (dict, optional): dictionary of data properties
                with keys

                source
                    name of the data source
                quantity
                    name of the data quantity
                unit
                    data unit

            ax(matplotlib.axes.Subplot, optional): the axes to look on.
                Defaults to all axes on :attr:`figure`.

        Yields:
            matplotlib.lines.Lines2D : the next matching line instance
        """
        for cur_ax in self.matching_axes(props) if ax is None else [ax]:
            for line in cur_ax.get_lines():
                if all(
                    props.get(k) == v
                    for k, v in (
                        line.restrictions
                        if hasattr(line, "restrictions")
                        else {}
                    ).items()
                ):
                    yield line

    def optimal_row_col_grid(self, n=None, width=None, height=None):
        """
        Determine the optimal number of rows and columns to fit a specified
        number of subplots into the :attr:`figure`, taking its current
        height/width-ratio into account. The algorithm minimizes both deviation
        of the grid ratio from the figure ratio and the left-free space.

        Args:
            n (int, optional): the minimum number of plots to fit into the
                figure. The default is the current amount of subplots.
            width, height (float, optional): the figure dimensions. Defaults to
                the current figure dimensions.

        Returns:
            n_rows, n_cols: the optimal number of rows and columns
        """
        n = len(self.figure.axes) if n is None else n
        width = self.figure.get_size_inches()[0] if width is None else width
        height = self.figure.get_size_inches()[1] if height is None else height
        return min(
            filter(
                lambda rowcol: rowcol[0] * rowcol[1] >= n,
                itertools.product(range(1, n + 1), range(1, n + 1)),
            ),
            key=lambda rowcol: (
                functools.reduce(
                    lambda c1, c2: c1 * (1 + c2),
                    (
                        1,
                        # relative ratio difference (in linear angle domain)
                        abs(
                            (
                                math.atan(height / width)
                                - math.atan(rowcol[0] / rowcol[1])
                            )
                            / math.atan(height / width)
                        ),
                        # left-free space ratio
                        # This ratio is artificially increased (weighted)
                        # as it yields more intuitive layouts
                        2
                        * (rowcol[1] * rowcol[0] - n)
                        / (rowcol[1] * rowcol[0]),
                    ),
                )
            ),
        )

    def reorder_subplots(self, n=None):
        """
        Reorder subplots on :attr:`figure` according
        :meth:`optimal_row_col_grid`.

        Args:
            n (int, optional): the minimum number of plots to fit onto the
                figure. The default is the current amount of subplots.

        Returns:
            n_rows, n_cols: the new number of rows and columns
        """
        rows, cols = self.optimal_row_col_grid(n=n)
        for i, ax in enumerate(self.figure.axes):
            ax.change_geometry(rows, cols, i + 1)
        self.autofmt_xdate()
        return rows, cols

    def add_axes(self, restrictions={}, **kwargs):
        """
        Make room for a new subplot with :meth:`reorder_subplots` and add a
        new axes to the :attr:`figure`.


        Args:
            restrictions (dict, optional): dictionary of restrictions for this
                axes with the following all-optional keys

                source
                    name of the data source
                quantity
                    name of the data quantity
                unit
                    data unit

                Only data with matching metadata will then be displayed on this
                axis. The default is no restriction.
            **kwargs: keyword arguments to
                :meth:`matplotlib.figure.Figure.add_subplot`

        Returns:
            matplotlib.axes.Subplot : the newly added axes
        """
        logger.debug(
            _("Creating new axes with restrictions {}").format(restrictions)
        )
        rows, cols = self.reorder_subplots(n=len(self.figure.axes) + 1)
        ax = self.figure.add_subplot(
            rows, cols, len(self.figure.axes) + 1, **kwargs
        )
        self.autofmt_xdate()
        ax.restrictions = restrictions
        if ax.restrictions:
            ax.set_title(
                ", ".join(
                    (
                        {
                            "parser": _("no parser"),
                            "quantity": _("no quantity"),
                            "unit": _("no unit"),
                        }.get(prop, _("no {}").format(prop))
                        if val is None
                        else "{}: {}".format(
                            {
                                "parser": _("parser"),
                                "quantity": _("quantity"),
                                "unit": _("unit"),
                            }.get(prop, prop),
                            val,
                        )
                    )
                    for prop, val in ax.restrictions.items()
                )
            )
        else:
            ax.set_title(_("Data from Every Parser, Quantity and Unit"))
        return ax

    def clear_figure(self):
        """
        Clear the :attr:`figure` by calling
        :meth:`matplotlib.figure.Figure.clear`.
        """
        self.figure.clear()
        self.figure.canvas.set_window_title(_("polt").title())

    def autofmt_xdate(self):
        """
        Pretty-format the xaxis dates with
        :meth:`matplotlib.figure.Figure.autofmt_xdate` after resetting the
        x-axis tick params on all axes.
        """
        for ax in self.figure.axes:
            ax.tick_params("x", reset=True)
        self.figure.autofmt_xdate()

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
            quantity, unit = (next(quantiter, None) for i in range(2))
            props = {"parser": parser, "quantity": quantity, "unit": unit}
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

    def update_figure(self, buffer):
        """
        Update the :attr:`figure`

        Args:
            buffer (list-like, optional): the buffer to update the
                :attr:`figure` with.
        """
        current_ratio = functools.reduce(
            operator.truediv, self.figure.get_size_inches()
        )
        if (
            self.figure.last_ratio
            if hasattr(self.figure, "last_ratio")
            else None
        ) != current_ratio and len(self.figure.axes):
            self.reorder_subplots()
            self.figure.last_ratio = current_ratio
        now = datetime.datetime.utcnow()
        # update the figure with all buffered datasets
        while buffer:
            self.update_figure_with_dataset(buffer.pop(0))
        # adjust axes limits
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
        # modify lines if necessary
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
                # extrapolate to the right
                if self.extrapolate:
                    x, y = line.get_xdata(), line.get_ydata()
                    if len(x) == 1:
                        x = np.append(x, now)
                        y = np.append(y, y[-1])
                    elif len(x) > 1:
                        if y[-1] == y[-2]:
                            x[-1] = now
                        else:
                            x = np.append(x, now)
                            y = np.append(y, y[-1])
                    else:
                        continue
                    line.last_extrapolated = True
                    line.set_xdata(x)
                    line.set_ydata(y)

    @property
    def dataset(self):
        """
        Generator which :class:`list`-ifies the :attr:`Animator.buffer`, clears
        and yields it forever
        """
        while True:
            # read the whole buffer
            buf = list(self.buffer)
            # empty the buffer
            del self.buffer[:]
            yield buf

    def run(self):
        """
        Run the animation by calling :func:`matplotlib.pyplot.show`
        """
        self.animation
        logger.debug(_("Showing the plot"))
        plt.show()
        logger.debug(_("Plot was closed"))
