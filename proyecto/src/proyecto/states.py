# coding: utf-8
from random import (
    SystemRandom,
)

from bernard import (
    layers as lyr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    translate as t,
)

from urllib.parse import urlencode, quote_plus
from bernard.platforms.telegram.media import Photo

from .utils import Bisection

from .store import cs
random = SystemRandom()

from .utils import frame_url
from .utils import get_frame_number
import json


class ProyectoState(BaseState):
    """
    Root class for Proyecto.

    Here you must implement "error" and "confused" to suit your needs. They
    are the default functions called when something goes wrong. The ERROR and
    CONFUSED texts are defined in `i18n/en/responses.csv`.
    """

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError


class Hello(ProyectoState):
    """
    Example "Hello" state, to show you how it's done. You can remove it.

    Please note the @page_view decorator that allows to track the viewing of
    this page using the analytics provider set in the configuration. If there
    is no analytics provider, nothing special will happen and the handler
    will be called as usual.
    """
    @page_view('/bot/hello')
    async def handle(self):
        name = await self.request.user.get_friendly_name()
        self.send(lyr.Text(t.HELLO))
        self.send(lyr.Text(name))


class F001xStartCheckFrame(ProyectoState):
    """
    Starts the frame checking.
    """
    # noinspection PyMethodOverriding
    @cs.inject()
    async def handle(self, context) -> None:
        context['starting_value'] = await get_frame_number(0)
        context['list'] = []
        self.send(lyr.Text("Start: Has the rocket launched? (%s, %s) " %
                           (str(context['starting_value']), str(context['list']))))
        # self.send(lyr.Markdown(url))


class F002xRepeatCheckFrame(ProyectoState):
    """
    Cycles the frame check.
    """
    # noinspection PyMethodOverriding
    @cs.inject()
    async def handle(self, context) -> None:
        # current_value = context.get('n')
        # url = frame_url(current_value)
        # answers = context['answers']
        self.send(lyr.Text("Has the rocket launched? (%s) " %
                           (str(context['list']))))
        # self.send(lyr.Markdown(url))


class F003xFinishCheckFrames(ProyectoState):
    # TODO
    pass


class IsNumberSimpleState(ProyectoState):
    """
    State to indicate that what was received is a number.
    """

    async def handle(self):
        self.send(lyr.Text("It is a number"))


class S002xGuessANumber(ProyectoState):
    """
    Define the number to guess behind the scenes and tell the user to guess it.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-a-number')
    @cs.inject()
    async def handle(self, context) -> None:
        context['number'] = random.randint(1, 100)
        print("Number is")
        print(context['number'])
        print("\n")
        self.send(lyr.Text("Guess a number"))


class S003xGuessAgain(ProyectoState):
    """
    If the user gave a number that is wrong, we give an indication whether that
    guess is too low or too high.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        user_number = self.trigger.user_number

        self.send(lyr.Text("WRONG"))

        if user_number < context['number']:
            self.send(lyr.Text("HIGHER"))
        else:
            self.send(lyr.Text("LOWER"))


class S004xCongrats(ProyectoState):
    """
    Congratulate the user for finding the number and propose to find another
    one.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        self.send(lyr.Text("CONGRATULATIONS"))


random = SystemRandom()
