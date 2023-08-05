#!/usr/bin/env python3
import click
import pyautogui

from autoclicker.funcs import mouse_click
from autoclicker.funcs import mouse_scroll
from autoclicker.validation import positive_number


@click.group()
def autoclicker():
    pass


@autoclicker.command()
@click.option('-s', '--screen_location', nargs=2, type=int, default=None)
@click.option('-r', '--repeats', default=10000, callback=positive_number)
@click.option('-t', '--time_break', required=True, type=float, callback=positive_number)
@click.option('-d', '--time_different', default=0.2, callback=positive_number)
def clicker(screen_location, repeats, time_break, time_different):
    posx, posy = screen_location if screen_location else pyautogui.position()
    mouse_click(posx, posy, repeats, time_break, time_different)


@autoclicker.command()
@click.option('-s', '--scrolls', required=True, type=int, callback=positive_number)
def scroll(scrolls):
    mouse_scroll(scrolls)


if __name__ == '__main__':
    autoclicker()
