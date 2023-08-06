# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from collections import namedtuple
import re

Template = namedtuple('Template', ['uuid', 'data', 'date'])


def is_function(str):
    """Check if the string represents a function

    A function has the format: func_name(params)
    Search for a regex with open and close parenthesis
    """
    return re.match('.*\(.*\)', str)
