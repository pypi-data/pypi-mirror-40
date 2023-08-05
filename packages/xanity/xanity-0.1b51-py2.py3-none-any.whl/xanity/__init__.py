# -*- coding: utf-8 -*-
#
# Copyright 2018 Barry Muldrey
#
# This file is part of xanity.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

__version__ = "0.1b51"            # this is the definitive version for distribution
__author__ = "Barry Muldrey"
__copyright__ = "Copyright 2018"
__license__ = "GNU Affero GPL"
__maintainer__ = "Barry Muldrey"
__email__ = "barry@muldrey.net"
__status__ = "Alpha"
__credits__ = []

import sys
import traceback
from .Xanity import Xanity
from .constants import ACTIVITIES
from .common import get_external_caller

items_to_expose = [
        'experiment_parameters',
        'associated_experiments',
        'log',
        'save_variable',
        'load_variable',
        'analyze_this',
        'load_checkpoint',
        'save_checkpoint',
        'persistent',
        'report_status',
        'run',
        'find_recent_data',
        'status',
        'project_root',
        'trials',
        '_rcfile',
        '_env_path',
]

thismodule = sys.modules[__name__]

if 'xanity' not in locals():

    # may have to set placeholders because modules which import
    # xanity might have to be imported during the creation of the Xanity object
    xanity = Xanity()

# check frame, register import, check_invocation
tb = traceback.extract_stack(limit=15)
for frame in tb:
    if 'import xanity' in frame[3]:
        xanity._register_import(frame[0])


def _log_and_get(item_name):
    if not xanity.status.act_tags:
        xanity._register_external_access(get_external_caller())
    return getattr(xanity, item_name)


def _xanity_getter(item_name):
    if callable(getattr(xanity, item_name)):
        return lambda *args, **kwargs: _log_and_get(item_name)(*args, **kwargs)
    else:
        return lambda: _log_and_get(item_name)


for fn in items_to_expose:
    setattr(thismodule, fn, _xanity_getter(fn))




