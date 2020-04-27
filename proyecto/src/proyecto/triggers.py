from bernard import (
    layers as lyr,
)
from bernard.engine.triggers import (
    BaseTrigger,
)

from .store import cs
from .utils import Bisection


class IsNumber(BaseTrigger):
    """
    Simplified version of the example for the number game. Only checks if user
    input is a number.
    """
    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        try:
            int(self.request.get_layer(lyr.RawText).text)
            return 1.0
        except (KeyError, ValueError, TypeError):
            return .0


class EqualStringTrigger(BaseTrigger):
    """
    Trigger that fires when the input is a specific string, case insensitive.
    """
    def __init__(self, request, string):
        super().__init__(request)
        self.string = string

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        text = self.request.get_layer(lyr.RawText).text

        if text.lower() == self.string.lower():
            return 1.0
        else:
            return 0.0


class ListAppenderTrigger(BaseTrigger):
    def __init__(self, request):
        super().__init__(request)

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        user_input = str(self.request.get_layer(lyr.RawText).text)
        context['list'].append(user_input)
        return 0.5


class BisectFrameTrigger2(BaseTrigger):
    """
    BisectFrameTrigger based on answer list.
    """
    def __init__(self, request):
        super().__init__(request)
        self.results = []

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        starting_value = context.get('starting_value')
        answers = context.get('answers')
        user_input = str(self.request.get_layer(lyr.RawText).text)
        user_input = user_input.lower()
        is_yes = "yes" in user_input
        is_no = "no" in user_input

        if not is_yes:
            if not is_no:
                return .0

        if is_yes:
            answers.append(True)
            context['answers'] = answers
        else:
            answers.append(False)
            context['answers'] = answers

        self.results = Bisection.from_answers(starting_value, answers)
        return 1.0


class BisectFrameTrigger(BaseTrigger):
    """
    TODO
    """

    def __init__(self, request):
        super().__init__(request)
        self.n = None
        self.answers = []
        # self.bisection = None

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        user_input = str(self.request.get_layer(lyr.RawText).text)
        user_input = user_input.lower()
        is_yes = "yes" in user_input
        is_no = "no" in user_input

        if not is_yes and not is_no:
            return .0

        if self.n is None:
            n = context.get('n')
            self.n = n
        else:
            n = self.n

        bisection = Bisection(n)

        if not bisection:
            return .0

        if "yes" in user_input:
            bisection.step(True)
            self.n = bisection.current_value
            context['n'] = bisection.current_value
        else:
            bisection.step(False)
            self.n = bisection.current_value
            context['n'] = bisection.current_value

        return 1.0


class NumberGameTrigger(BaseTrigger):
    """
    This trigger will try to interpret what the user sends as a number. If it
    is a number, then it's compared to the number to guess in the context.
    The `is_right` parameter allows to say if you want the trigger to activate
    when the guess is right or not.
    """

    def __init__(self, request, is_right):
        super().__init__(request)
        self.is_right = is_right
        self.user_number = None

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        number = context.get('number')

        if not number:
            return .0

        try:
            self.user_number = int(self.request.get_layer(lyr.RawText).text)
        except (KeyError, ValueError, TypeError):
            return .0

        is_right = number == self.user_number

        return 1. if is_right == self.is_right else .0
