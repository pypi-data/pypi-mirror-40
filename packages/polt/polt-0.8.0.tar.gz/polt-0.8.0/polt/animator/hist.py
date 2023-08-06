# system modules
import functools
import datetime
import logging
import inspect
import operator
import sys

# internal modules
from polt.animator.lines import LinesAnimator
from polt.utils import *

# external modules
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class HistAnimator(LinesAnimator):
    """
    Animator to display recieved data as lines.

    Args:
        args, kwargs: further arguments handed to the
            :any:`LinesAnimator` constructor.
        bins (int, optional): the number of bins to use.
        normed (bool, optional): whether to display density instead of
            frequency. Default is ``False``.
        time_frame (int, optional): displayed time frame in seconds. By default
            (``None``), all times are diplayed.
    """

    def __init__(
        self, *args, bins=None, normed=None, time_frame=None, **kwargs
    ):
        LinesAnimator.__init__(self, *args, **kwargs)
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def bins(self):
        """
        How many bins to use. Default is 10.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o bins=NUMBER``

        :type: :class:`str` or ``None``
        """
        try:
            self._bins
        except AttributeError:
            self._bins = 10
        return self._bins

    @bins.setter
    def bins(self, new):
        self._bins = max(2, abs(int(new)))

    @property
    def normed(self):
        """
        Whether to norm the histogram. By default (``False``), the
        absolute frequency is used.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o normed=yes|no``

        :type: :class:`str` or ``None``
        """
        try:
            self._normed
        except AttributeError:
            self._normed = False
        return self._normed

    @normed.setter
    def normed(self, new):
        self._normed = new == "yes" if isinstance(new, str) else bool(new)

    @property
    def time_frame(self):
        """
        Time frame to use in seconds. Data outside that window
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
        self._time_frame = max(sys.float_info.min, int(new))

    def histogram(self, *args, **kwargs):
        """
        Call :any:`numpy.histogram` with default arguments.

        Args:
            **kwargs: overwriting keyword arguments

        Returns:
            sequence : the same as :any:`numpy.histogram`
        """
        hist_kwargs = {"bins": self.bins, "density": self.normed}
        hist_kwargs.update(kwargs)
        return np.histogram(*args, **hist_kwargs)

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
            if isinstance(val, str):
                logger.debug(
                    _("Cannot plot string value {}").format(repr(val))
                )
                continue
            else:
                val = to_tuple(val)
            # determine matching axes
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
                ax = self.add_axes(
                    restrictions=restrictions, **add_axes_kwargs
                )
                ax.set_ylabel(_("density") if self.normed else _("frequency"))
                ax.set_xlabel(_("value"))
            if not hasattr(ax, "units"):
                ax.units = set()
            if unit not in ax.units:
                ax.units.add(unit)
                ax.set_xlabel(
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
            # determine matching line
            values = np.array(val)
            times = np.repeat(np.datetime64(time_recieved_utc), values.size)
            line = next(self.matching_line(props), None)
            if line:
                line.values = np.append(line.values, values)
                line.times = np.append(line.times, times)
                if self.time_frame:
                    outside = (
                        np.datetime64(datetime.datetime.utcnow()) - line.times
                    ) / np.timedelta64(1, "s") > self.time_frame
                    if outside.any():
                        outside_ind = np.where(outside)[0]
                        line.values = np.delete(line.values, outside_ind)
                        line.times = np.delete(line.times, outside_ind)
                freq, bins = self.histogram(line.values)
                line.set_xdata(np.repeat(bins, 2))
                line.set_ydata(
                    np.concatenate(
                        [np.array([0]), np.repeat(freq, 2), np.array([0])]
                    )
                )
                ax.relim()
                ax.autoscale_view()
            else:
                freq, bins = self.histogram(values)
                lines = ax.plot(
                    np.repeat(bins, 2),
                    np.concatenate(
                        [np.array([0]), np.repeat(freq, 2), np.array([0])]
                    ),
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
                    cur_line.values = values
                    cur_line.times = times
                ax.legend()

    @LinesAnimator.register_method("after-each-frame")
    def proper_ylim(self, *args, **kwargs):
        """
        Make sure the y-axis limit are appropriate
        """
        for ax in self.figure.axes:
            ax.set_ylim(
                -0.01,
                max(max(line.get_ydata()) for line in ax.get_lines()) * 1.01,
            )
