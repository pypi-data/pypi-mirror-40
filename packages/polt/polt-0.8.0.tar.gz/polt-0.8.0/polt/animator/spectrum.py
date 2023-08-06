# system modules
import functools
import sys
import datetime
import logging
import inspect
import operator

# internal modules
from polt.animator.lines import LinesAnimator
from polt.utils import *

# external modules
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class SpectrumAnimator(LinesAnimator):
    """
    Animator to display recieved data as lines.

    Args:
        args, kwargs: further arguments handed to the
            :any:`LinesAnimator` constructor.
        blocks (int, optional): Into how many block-wise averages should be
            taken of the FFT. Default is to not split the data up.
        hanning (bool, optional): Whether to apply a
            :any:`numpy.hanning`-window before the FFT. Default is ``True``.
        time_frame (int, optional): displayed time frame in seconds. By default
            (``None``), all times are diplayed.
    """

    def __init__(self, *args, time_frame=None, hanning=None, **kwargs):
        LinesAnimator.__init__(self, *args, **kwargs)
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    @property
    def hanning(self):
        """
        Whether to apply a :any:`numpy.hanning`-window before the FFT.

        .. note::

            Set this option from the command-line via
            ``polt live -a spectrum -o hanning=yes|no``

        :type: :class:`bool`
        """
        try:
            self._hanning
        except AttributeError:
            self._hanning = False
        return self._hanning

    @hanning.setter
    def hanning(self, new):
        self._hanning = new == "yes" if isinstance(new, str) else bool(new)

    @property
    def blocks(self):
        """
        Into how many blocks to split the data for later averaging of the FFT.
        Default is to not split the data up.

        .. note::

            Set this option from the command-line via
            ``polt live -a spectrum -o blocks=N``

        :type: :class:`bool`
        """
        try:
            self._blocks
        except AttributeError:
            self._blocks = 1
        return self._blocks

    @blocks.setter
    def blocks(self, new):
        self._blocks = max(1, int(new))

    @property
    def time_frame(self):
        """
        Time frame to use in seconds. Data outside that window
        will be dropped.

        .. note::

            Set this option from the command-line via
            ``polt live -a spectrum -o time-frame=SECONDS``

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

    def spectrum(self, x, y, hanning=None, blocks=None):
        """
        Call :any:`numpy.fft.fft` and :any:`numpy.fft.fftfreq`
            with default arguments.

        Args:
            x,y (sequences of floats): x and y values
            hanning (bool, optional): whether to apply a Hanning window

        Returns:
            sequence : frequencies, power as arrays
        """
        hanning = self.hanning if hanning is None else hanning
        blocks = self.blocks if blocks is None else blocks
        # convert inputs to numpy arrays
        x, y = map(np.asarray, (x, y))
        # drop older values to fit the number of blocks
        if x.size > blocks:
            drop = x.size % blocks
            x, y = x[drop:], y[drop:]
        # interpolate to evenly-spaced times
        if x.size > 1:
            interpolator = scipy.interpolate.interp1d(x, y)
            x = np.linspace(x.min(), x.max(), num=x.size)
            y = interpolator(x)
        # calculate power spectrum
        power = (
            np.abs(
                # calculate average across block means
                np.mean(
                    # stack fft block resuls
                    np.vstack(
                        tuple(
                            # Fourrier transformation
                            map(
                                np.fft.fft,
                                # apply hanning window if desired
                                map(
                                    lambda a: a * np.hanning(a.size)
                                    if hanning
                                    else a,
                                    # split y into blocks
                                    np.split(y, blocks)
                                    if y.size > blocks
                                    else (y,),
                                ),
                            )
                        )
                    ),
                    axis=0,
                )
            )
            ** 2
        )
        # calculate frequencies
        freq = np.fft.fftfreq(power.size, ((x.max() - x.min()) / x.size) or 1)
        # sort frequencies
        idx = np.argsort(freq)
        freq, power = freq[idx], power[idx]
        positive_freq = freq >= 0
        return freq[positive_freq], power[positive_freq]

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
            if not val:
                continue
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
                ax.set_ylabel(_("power"))
                ax.set_xlabel(_("frequency [Hz]"))
            if not hasattr(ax, "units"):
                ax.units = set()
            # determine matching line
            new_value = np.mean(np.array(val))
            new_time = np.datetime64(time_recieved_utc)
            line = next(self.matching_line(props), None)
            if line:
                line.values = np.append(line.values, new_value)
                line.times = np.append(
                    line.times, np.datetime64(time_recieved_utc)
                )
                if self.time_frame:
                    outside = (
                        np.datetime64(datetime.datetime.utcnow()) - line.times
                    ) / np.timedelta64(1, "s") > self.time_frame
                    if outside.any():
                        outside_ind = np.where(outside)[0]
                        line.values = np.delete(line.values, outside_ind)
                        line.times = np.delete(line.times, outside_ind)
                freq, fft = self.spectrum(
                    (line.times - line.times.min()) / np.timedelta64(1, "s"),
                    line.values,
                )
                line.set_xdata(freq)
                line.set_ydata(fft)
                ax.relim()
                ax.autoscale_view()
            else:
                times, values = new_time.reshape(-1), new_value.reshape(-1)
                freq, fft = self.spectrum(
                    (times - times.min()) / np.timedelta64(1, "s"), values
                )
                lines = ax.plot(
                    freq,
                    fft,
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
            cur_min = min(min(line.get_ydata()) for line in ax.get_lines())
            cur_max = max(max(line.get_ydata()) for line in ax.get_lines())
            ax.ylim_min = min(
                ax.ylim_min if hasattr(ax, "ylim_min") else cur_min, cur_min
            )
            ax.ylim_max = max(
                ax.ylim_max if hasattr(ax, "ylim_max") else cur_max, cur_max
            )
            ax.set_ylim(bottom=ax.ylim_min, top=ax.ylim_max)
