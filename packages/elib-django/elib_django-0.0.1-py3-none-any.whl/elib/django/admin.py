#
# copyright (c) 2019 east301
#
# This software is released under the Apache License, Version 2.0.
# https://opensource.org/licenses/Apache-2.0
#


def short_description(description):
    def apply(func):
        func.short_description = description
        return func

    return apply
