"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Dict

from .types import InputMessage
from .client import _Client
from .client import build_client

class CatalogClient(_Client):
    """A client for the Catalog REST API."""

    URIs = {'types':        'catalog/types',
            'agents':       'catalog/agents',
            'processors':   'catalog/processors',
            'skills':       'catalog/skills'
           }

    def save_type(self, type: Dict[str, object]):
        """Save a type.

        :param type: A Cortex Type as dict.
        """
        return self._post_json(self.URIs['types'], type)

    def save_agent(self, agent: Dict[str, object]):
        """Save an Agent.

        :param agent: A Cortex Agent as dict.
        """
        return self._post_json(self.URIs['agents'], agent)

    def save_processor(self, processor: Dict[str, object]):
        """Save a Processor / Skill

        :param processor: A Cortex Processor as dict.
        """
        return self._post_json(self.URIs['processors'], processor)

    def save_skill(self, skill: Dict[str, object]):
        """Save a Skill.

        :param skill: A Cortex Skill as dict.
        """
        return self._post_json(self.URIs['skills'], skill)


def build_catalogclient(input_message: InputMessage, version) -> CatalogClient:
    return build_client(CatalogClient, input_message, version)
