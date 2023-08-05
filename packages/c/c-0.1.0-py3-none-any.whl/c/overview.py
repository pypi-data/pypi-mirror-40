#!/usr/bin/env python3

import os

import arrow
import matplotlib.pyplot as plt

from . import (
    battery_history,
    percent_cumulative_distribution,
    percent_distribution,
    reader,
    screen_on_week,
    stats,
    time_of_weekday,
    time_of_day,
    voltages,
)
from c.utils import time_tracker


def main():
    df = reader.read_battery_history()

    f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 9))

    with time_tracker('battery history'):
        battery_history.plot(df=df, canvas=ax1)
        ax1.set_xlim([  # "show a week"
            arrow.now().replace(days=-7).datetime,
            arrow.now().datetime])
        ax1.set_ylim([0, 100])

    with time_tracker('voltages'):
        voltages.plot(df=df, canvas=ax2)
        ax2.set_xlim([0, 100])
        ax2.set_ylim([3.4, 4.4])

    with time_tracker('percent distribution'):
        percent_distribution.plot(df=df, canvas=ax3)
        ax3.set_xlim([0, 100])
        ax3.set_ylim([0, 8])

    with time_tracker('screen on week'):
        screen_on_week.plot(df=df, canvas=ax4)
        ax4.set_ylim([0, 18])

    with time_tracker('time of day'):
        time_of_day.plot(df=df, canvas=ax5)
        ax5.set_xlim([0, 24])
        ax5.set_ylim([0, 80])

    with time_tracker('time of weekday'):
        time_of_weekday.plot(df=df, canvas=ax6)
        ax6.set_xlim([0, 24])
        ax6.set_ylim([0, 80])

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1, hspace=0.3)

    if os.path.exists('figs'):
        plt.savefig('figs/' + arrow.now().isoformat() + '.png')

    stats.chart(df)
    plt.show()


if __name__ == '__main__':
    main()
