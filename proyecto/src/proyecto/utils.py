import typing
from typing import Callable
import io
import os
import sys
from typing import List, NamedTuple, Text
from urllib.parse import quote, urljoin

import httpx


API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/")

VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)


async def get_frame_number(position: int):
    async with httpx.AsyncClient() as client:
        r = await client.get("http://framex-dev.wadrid.net/api/video/")
        if r.status_code == 200:
            try:
                return r.json()[position]['frames']
            except:
                return None
        return None


def frame_url(n):
    url = "http://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/"
    return url + str(n) + "/"


def identity_mapper(n, debug=False):
    """
    In that case there is no need to map (or rather, the mapping
    is done visually by the user)
    """
    if debug:
        print("Identity mapper at %s" % n)
    return n


def bisect(n, mapper, tester):
    """
    Runs a bisection.

    - `n` is the number of elements to be bisected
    - `mapper` is a callable that will transform an integer from "0" to "n"
      into a value that can be tested
    - `tester` returns true if the value is within the "right" range
    """

    if n < 1:
        raise ValueError("Cannot bissect an empty array")

    left = 0
    right = n - 1

    while left + 1 < right:
        mid = int((left + right) / 2)

        val = mapper(mid)

        if tester(val):
            right = mid
        else:
            left = mid

    return mapper(right)


class Bisection(object):

    def __init__(self, n: int):
        self.n = n
        self.current_value = identity_mapper(self.n)
        self.finished = False

        self.left = 0
        self.right = n - 1
        self.mid = None

        # first step is done automatically, so we stand ready to receive a boolean
        self.compute()

    @staticmethod
    def from_answers(n: int, answers: List[bool]) -> List[int]:
        obj = Bisection(n)
        results = []

        for answer in answers:
            obj.step(answer)
            results.append(obj.current_value)

        return results

    def can_continue(self):
        return self.left + 1 < self.right

    def compute(self):
        self.mid = int((self.left + self.right) / 2)
        self.current_value = identity_mapper(self.mid)

    def step(self, boolean: bool):
        self.compute()

        if boolean:
            self.right = self.mid
        else:
            self.left = self.mid

        if not self.can_continue():
            self.finished = True


def make_value_tester():
    def inner(n):
        print("Inner at %s" % n)
        user_input = input("Has it launched? ").lower()
        if user_input == "y" or user_input == "yes" or user_input == "true":
            return True
        return False
    return inner


if __name__ == '__main__':
    """
    Simple interactive testing for the functions.
    Remember that expected value is around 37231.
    
    YES
    Inner at 30847
    Has it launched? yes
    Inner at 15423
    Has it launched? yes
    Inner at 7711
    Has it launched? yes
    Inner at 3855
    Has it launched?
    
    NO
    Inner at 30847
    Has it launched? no
    Inner at 46270
    Has it launched? no
    Inner at 53982
    Has it launched? no
    Inner at 57838
    Has it launched? no
    Inner at 59766
    """
    n = 61695
    print(Bisection.from_answers(n, [False, False, False, False, False]))

    sys.exit()
    # tester = make_value_tester()
    # bisect(n, identity_mapper, tester)
    bisecter = Bisection(n)

    while bisecter.can_continue():
        bisecter.step(True)
        print(bisecter.current_value)
