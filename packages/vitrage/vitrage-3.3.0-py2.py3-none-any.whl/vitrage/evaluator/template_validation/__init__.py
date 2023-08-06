# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_log import log

from vitrage.evaluator.template_fields import TemplateFields
from vitrage.evaluator.template_validation.content.base import \
    get_template_schema
from vitrage.evaluator.template_validation.content.template_content_validator \
    import content_validation
from vitrage.evaluator.template_validation.template_syntax_validator import \
    def_template_syntax_validation
from vitrage.evaluator.template_validation.template_syntax_validator import \
    syntax_validation


LOG = log.getLogger(__name__)


def validate_template(template, def_templates):
    result = syntax_validation(template)
    if not result.is_valid_config:
        LOG.error('Unable to load template, syntax error: %s' % result.comment)
        return result
    result = content_validation(template, def_templates)
    if not result.is_valid_config:
        LOG.error('Unable to load template, content error:%s' % result.comment)
        return result
    return result


def validate_definition_template(template_def):
    result, template_schema = get_template_schema(template_def)
    if not result.is_valid_config:
        return result

    result = def_template_syntax_validation(template_def)
    if not result.is_valid_config:
        LOG.error('Unable to load template, syntax err: %s' % result.comment)
        return result

    validator = template_schema.validators.get(TemplateFields.DEFINITIONS)
    result = validator.def_template_content_validation(template_def)
    if not result.is_valid_config:
        LOG.error('Unable to load template, content err: %s' % result.comment)
        return result
    return result
