#!/usr/bin/env python3
def positive_number(ctx, param, value):
    if value > 0:
        return value
    raise ValueError
