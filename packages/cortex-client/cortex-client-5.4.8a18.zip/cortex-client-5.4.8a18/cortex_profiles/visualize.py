
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

import json
from typing import List, Optional

import pandas as pd

from cortex_client.profilesclient import ProfilesClient
from cortex_profiles.notebook.utils import InteractableJson
from cortex_profiles.notebook.utils import tab_with_content, to_output
from cortex_profiles.schemas.client_dataframes import COMMIT_COL, PROFILE_COL

OrderedList = List


class ProfileVisualizationClient(ProfilesClient):
    """A client for the Cortex Profiles SDK Functionality."""

    def visualizeHistoryOfAttribute(self, profileId:str, attributeKey:str):
        return tab_with_content({
            commitId: to_output(self._render_json(self.describeAttribute(profileId, attributeKey, commitId=commitId)))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeHistoryOfAttributesInProfile(self, profileId:str):
        return tab_with_content({
            commitId: to_output(self.listAttributes(profileId, commitId=commitId))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeHistoryOfCommitsOnProfile(self, profileId: str):
        return tab_with_content({
            commitId: to_output(self.listAttributes(profileId, commitId=commitId))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeProfile(self, profileId:str, commitId:Optional[str]=None):
        return self._render_json(self.describeProfile(profileId, commitId))

    def listProfiles(self, query:Optional[dict]=None) -> pd.DataFrame:
        return pd.DataFrame(
            self._internal_profiles_client.list_profiles(query), columns=list(PROFILE_COL.values())
        ).sort_values(by=[PROFILE_COL.PROFILE_TYPE, PROFILE_COL.PROFILE_ID])

    def _render_json(self, j:dict):
        return InteractableJson(json.loads(json.dumps(j)))
        # return pprint(utils.json_makeup(json.loads(json.dumps(j))))
