
# Copyright (c) 2019 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import io
import logging

import attr

from packagedcode import models
from commoncode import saneyaml


"""
Handle CRAN package.
R is a programming languages and CRAN its package repository.
https://cran.r-project.org/
"""

TRACE = False

logger = logging.getLogger(__name__)

if TRACE:
    import sys
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)


@attr.s()
class CranPackage(models.Package):
    metafiles = ('DESCRIPTION',)
    default_type = 'cran'

    @classmethod
    def recognize(cls, location):
        return parse(location)

    @classmethod
    def get_package_root(cls, manifest_resource, codebase):
        return manifest_resource.parent(codebase)

def parse(location):
    """
    Return a Package object from a DESCRIPTION file or None.
    """
    yaml_data = get_yaml_data(location)
    return build_package(yaml_data)


def build_package(package_data):
    """
    Return a cran Package object from a dictionary yaml data.
    """
    name = package_data.get('Package')
    if name:
        package = CranPackage(
            name=name,
        )
        return package

def get_yaml_data(location):
    """
    Parse the yaml file
    """
    yaml_lines = []
    with io.open(location, encoding='utf-8') as loc:
        for line in loc.readlines():
            if not line:
                continue
            yaml_lines.append(line)
    return saneyaml.load('\n'.join(yaml_lines))
    