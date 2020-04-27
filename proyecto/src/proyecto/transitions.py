# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .states import F001xStartCheckFrame
from .states import F002xRepeatCheckFrame
from .triggers import IsNumber, NumberGameTrigger, EqualStringTrigger
from .triggers import BisectFrameTrigger2
from .triggers import ListAppenderTrigger


transitions = [
    Tr(
        dest=Hello,
        factory=trg.Text.builder(its.HELLO),
    ),

    # start guessing at frames
    Tr(
        dest=F001xStartCheckFrame,
        factory=EqualStringTrigger.builder(string="begin")
    ),

    # enter iteration of repeating frame questions
    Tr(
        dest=F002xRepeatCheckFrame,
        origin=F001xStartCheckFrame,
        factory=ListAppenderTrigger.builder()
    ),

    # remain inside repeating frame questions
    Tr(
        dest=F002xRepeatCheckFrame,
        origin=F002xRepeatCheckFrame,
        factory=ListAppenderTrigger.builder()
    )
]

# Number game transitions
"""
# enter the number game when writing "start" to the bot
Tr(
   dest=S002xGuessANumber,
   factory=EqualStringTrigger.builder(string="start")
),

# first number question
Tr(
    dest=S003xGuessAgain,
    origin=S002xGuessANumber,
    factory=NumberGameTrigger.builder(is_right=False)
),

# number question repeater
Tr(
    dest=S003xGuessAgain,
    origin=S003xGuessAgain,
    factory=NumberGameTrigger.builder(is_right=False)
),

# success in guessing the number
Tr(
    dest=S004xCongrats,
    origin=S003xGuessAgain,
    factory=NumberGameTrigger.builder(is_right=True),
),
"""
