# system modules
import functools
import itertools
import logging
import inspect
import math
from abc import abstractmethod

# internal modules
from polt.registry import FunctionRegistry

# external modules
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

logger = logging.getLogger(__name__)


class Animator(FunctionRegistry):
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
            self._buffer = list()
        return self._buffer

    @buffer.setter
    def buffer(self, new):
        self._buffer = new

    @property
    def interval(self):
        """
        The frame update interval

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o interval=MILLISECONDS``

        :type: :any:`int`
        """
        try:
            self._interval
        except AttributeError:
            self._interval = 200
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        self._interval = max(1, int(new_interval))

    @property
    def max_fps(self):
        """
        The maximum update framerate in frames per second (Hz). Internally this
        sets :any:`interval`.

        .. note::

            Set this option from the command-line via
            ``polt live -a lines -o max-fps=FRAMERATE``

        :getter: return the inverse of :attr:`interval`
        :setter: set :attr:`interval` to the inverse of the given value in
            millisecons capped below ``1e-2`` which means 100 seconds per frame
            (very slow...)
        :type: :class:`float`
        """
        return 1 / self.interval

    @max_fps.setter
    def max_fps(self, new):
        self.interval = 1e3 / max(1e-2, float(new))

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
                "key_press_event",
                lambda e: self.call_registered_functions(
                    "key-pressed", event=e
                ),
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

    @FunctionRegistry.register_method("key-pressed")
    def toggle_pause_key_callback(self, event):
        """
        Callback to pause the animation with :any:`toggle_pause` if the pressed
        key was the spacebar.

        Args:
            event (matplotlib.backend_bases.KeyEvent, optional): the key event
        """
        if event.key == " ":
            self.toggle_pause()

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
        and yields it forever. If :any:`paused` and :any:`drop_on_pause` is
        ``True``, drop the data and yield an empty list.

        The following registry hooks are executed:

        frame-before-data-check
            first thing in each iteration

        frame-during-pause
            on each iteration but only during pause before dropping the
            :any:`buffer`

        frame-when-not-paused
            on each iteration but only during pause before reading and clearing
            the :any:`buffer`
        """
        while True:
            self.call_registered_functions("frame-before-data-check")
            if self.paused:
                self.call_registered_functions("frame-during-pause")
                if self.drop_on_pause:
                    # empty the buffer
                    del self.buffer[:]
            else:
                self.call_registered_functions("frame-when-not-paused")
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
