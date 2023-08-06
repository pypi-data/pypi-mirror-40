# system modules
import functools
import collections
import logging
import inspect
import datetime
import operator
import re
from abc import abstractmethod

# internal modules
from polt.animator.subplots import SubPlotsAnimator

# external modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date

logger = logging.getLogger(__name__)


class LinesAnimator(SubPlotsAnimator):
    """
    Animator to display recieved data as lines.

    Args:
        args, kwargs: further arguments handed to the
            :any:`SubPlotsAnimator` constructor.
    """

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
                key
                    data key

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

    @abstractmethod
    def update_figure_with_dataset(self, dataset):
        """
        Update the figure with a single dataset. This is an
        :any:`abc.abstractmethod`, so subclasses have to override this.

        Args:
            dataset (dict): the dataset to update the :attr:`figure` with
        """

    @SubPlotsAnimator.register_method("before-each-frame")
    def optimal_subplots_layout(self, *args, **kwargs):
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

    def update_figure(self, buffer):
        """
        If :any:`paused`, return. Otherwise, :any:`update_figure_with_dataset`
        for all datasets in the given buffer.

        The following registry hooks are executed:

        before-each-frame
            first thing that is done in this function (and before pausing)

        after-each-frame
            last thing that is done in this function

        Args:
            buffer (list-like): the buffer containing the datasets
                to update the :attr:`figure` with.
        """
        # call functions registered for before the frame
        self.call_registered_functions("before-each-frame", buffer)
        if self.paused:
            return
        # update the figure with all buffered datasets
        while buffer:
            self.update_figure_with_dataset(buffer.pop(0))
        # call functions registered for after the frame
        self.call_registered_functions("after-each-frame")
