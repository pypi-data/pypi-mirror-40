# -*- coding: utf-8 -*-
# Copyright 2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
""" AppEngine ndb integration """
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from serafin import util
from serafin.serializer import serialize

# GAE bundled imports
from google.appengine.ext import ndb


__version__ = '0.1.2'


@serialize.type(ndb.Model)
def serialize_ndb_model(obj, spec, ctx):
    """ serafin serializer for ndb models. """
    if spec is True or spec.empty():
        return {}

    ret = {'id': obj.key.id()}
    props = list(util.iter_public_props(obj, lambda n, v: n in spec))

    ret.update(serialize_ndb_props(obj, spec, ctx))
    ret.update({key: serialize.raw(val, spec[key], ctx) for key, val in props})

    return ret


def serialize_ndb_props(model, fieldspec, ctx):
    """ Serialize properties on a ndb.Model

    :param ndb.Model model:
        The model we want to serialize.
    :param Fieldspec fieldspec:
        Defines what fields will be included in the result.
    :param Context context:
        Serialization context. For more information, refer to **serafin**
        documentation.
    :return dict:
        A dictionary containing the serialized data. The layout of the
        dictionary will depend on the fieldspec passed.
    """
    data = {}

    for prop in model._properties.itervalues():
        name = prop._code_name

        if name in fieldspec:
            value = prop._get_for_dict(model)

            if isinstance(value, ndb.Key):
                name += '_id'
                value = value.id()

            data[name] = serialize.raw(value, fieldspec[name], ctx)

    return data
