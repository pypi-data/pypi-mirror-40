# Copyright © 2018 Absolute Performance, Inc
# Written by Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from strictyaml import Map, Str, Int, Optional

schema = Map({
    Optional('clientflags'): Str(),
    Optional('serverflags'): Str(),
    'dkeyprefix': Str(),
    'host': Str(),
    'username': Str(),
    Optional('password'): Str(),
    Optional('keyfilename'): Str(),
    Optional('port', default=-1): Int(),
})

