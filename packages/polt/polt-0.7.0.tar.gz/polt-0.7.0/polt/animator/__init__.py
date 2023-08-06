# system modules
import functools
import itertools
import logging
import inspect
import math
from abc import abstractmethod, ABC

# internal modules

# external modules
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)


class Animator(ABC):
    """
    The :class:`Animator` is an abstract base class for animations. Subclasses
    need to override just the :meth:`Animator.update_figure` method.

    Args:
        figure (matplotlib.figure.Figure, optional): the figure to animate on
        buffer (list-like, optional): the buffer to retrieve
            data from.
        interval (int, optional): the frame update interval in milliseconds.
            Default is 200.
        drop_on_pause (bool, optional): Whether to drop data when paused. The
            default is ``True``.
    """

    def __init__(
        self, figure=None, buffer=None, interval=None, drop_on_pause=None
    ):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)
        # register key callbacks
        self.register_key_callback(
            self.toggle_pause, lambda event: event.key in (" ",)
        )

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
            fig = plt.figure()
            fig.canvas.mpl_connect(
                "key_press_event", self.execute_key_callbacks
            )
            self._figure = fig
        return self._figure

    @figure.setter
    @modifies_animation
    def figure(self, new):
        self._figure = new

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

    @property
    def paused(self):
        """
        Whether the animation is currently paused or not.
        During pause, recieved data is dropped if
        :attr:`Animator.drop_on_pause` is ``True``.

        :type: :class:`bool`
        """
        try:
            self._paused
        except AttributeError:
            self._paused = False
        return self._paused

    @paused.setter
    def paused(self, new):
        new = bool(new)
        if self.paused != new:
            if new:
                self.figure.canvas.set_window_title(
                    "{} ({})".format(_("polt").title(), _("paused"))
                )
            else:
                self.figure.canvas.set_window_title(_("polt").title())
        self._paused = new

    @property
    def drop_on_pause(self):
        """
        Whether to drop recieved data if the animation is paused. The default
        is ``False``.

        .. note::

            Set this option from the command-line via
            ``polt live -o drop-on-pause=yes|no``

        :type: :class:`bool`
        """
        try:
            self._drop_on_pause
        except AttributeError:
            self._drop_on_pause = False
        return self._drop_on_pause

    @drop_on_pause.setter
    def drop_on_pause(self, new):
        self._drop_on_pause = (
            new == "yes" if isinstance(new, str) else bool(new)
        )

    @property
    def key_callbacks(self):
        """
        Callbacks registered with :meth:`register_key_callback` to be called in
        order when a key was pressed.

        :type: :class:`list`
        """
        try:
            self._on_key_callbacks
        except AttributeError:
            self._on_key_callbacks = []
        return self._on_key_callbacks

    def register_key_callback(self, cb, condition=lambda event: True):
        """
        Register a function for being called if a ``key_press_event`` occurs.

        Args:
            cb (callable): the function to call on key press
            condition (callable, optional): The result of this callable taking
                the event as single argument is used to decide whether the
                registered function is executed or not. The default is to
                always execute the function.
        """
        self.key_callbacks.append((cb, condition))

    def execute_key_callbacks(self, event):
        """
        Execute all callbacks registered with :attr:`on_key`.
        """
        for callback, condition in self.key_callbacks:
            if condition(event):
                callback()

    def pause(self):
        """
        Pause the animation
        """
        self.paused = True

    def resume(self):
        """
        Resume the animation
        """
        self.paused = False

    def toggle_pause(self):
        """
        Change the paused state
        """
        if self.paused:
            logger.info(_("Resuming"))
        else:
            logger.info(_("Pausing"))
            if self.drop_on_pause:
                logger.info(_("Recieved data is dropped form now on."))
            else:
                logger.info(_("Data recording keeps going."))
        self.paused = not self.paused

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
                key
                    data key

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
                key
                    data key

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
        ax.restrictions = restrictions
        if ax.restrictions:
            ax.set_title(
                ", ".join(
                    (
                        {
                            "parser": _("no parser"),
                            "quantity": _("no quantity"),
                            "unit": _("no unit"),
                            "key": _("no key"),
                        }.get(prop, _("no {}").format(prop))
                        if val is None
                        else "{}: {}".format(
                            {
                                "parser": _("parser"),
                                "quantity": _("quantity"),
                                "unit": _("unit"),
                                "key": _("key"),
                            }.get(prop, prop),
                            val,
                        )
                    )
                    for prop, val in ax.restrictions.items()
                )
            )
        else:
            ax.set_title(_("Data from Every Parser, Quantity, Unit and Key"))
        return ax

    def clear_figure(self):
        """
        Clear the :attr:`figure` by calling
        :meth:`matplotlib.figure.Figure.clear`.
        """
        self.figure.clear()
        self.figure.canvas.set_window_title(_("polt").title())

    @abstractmethod
    def update_figure(self, buffer):
        """
        Update the :attr:`figure` with a sequence of datasets from the
        :attr:`Animator.buffer`.

        .. note::

            This is an :func:`abc.abstractmethod`, so subclasses have to
            override this.

        Args:
            buffer (sequence): the buffer containing the datasets
                to update the :attr:`figure` with.
        """

    @property
    def dataset(self):
        """
        Generator which :class:`list`-ifies the :attr:`Animator.buffer`, clears
        and yields it forever
        """
        while True:
            if self.paused:
                if self.drop_on_pause:
                    # empty the buffer
                    del self.buffer[:]
                yield None
            else:
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
