# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:33:15 2018

@author: pmarella
"""

import pandas as pd

theme_list = [{'Summary': 'Dynamic Throttling for Gen10 6000 series models (vSphere Only)', 'FixVersions': 'Omnistack 3.7.5 (PSI 13)', 'Key': 'PMB-1197', 'IssueType': 'Release Theme'} ,
              {'Summary': 'Spike: SW RAID Stack', 'FixVersions': 'Omnistack 3.7.3 (PSI 12)', 'Key': 'PMB-1067', 'IssueType': 'Release Theme'},
              {'Summary': 'Dynamic Throttling for Gen10 4000 series models (vSphere Only)', 'FixVersions': 'Omnistack 3.7.3 (PSI 12)', 'Key': 'PMB-982', 'IssueType': 'Release Theme'},
              {'Summary': 'Gen-10 DL380 "Value Flash" XLarge for VMware', 'FixVersions': 'Omnistack 3.7.3 (PSI 12)', 'Key': 'PMB-959', 'IssueType': 'Release Theme'},
              {'Summary': 'SHA-1 to SHA-2 Update - Torch', 'FixVersions': 'Omnistack 3.7.3 (PSI 12)', 'Key': 'PMB-944', 'IssueType': 'Release Theme'},
              {'Summary': 'SHA-1 to SHA-2 Update - Torch', 'FixVersions': 'Torch GA', 'Key': 'PMB-944', 'IssueType': 'Release Theme'}]

epic_list = [{'Summary': 'Enterprise Container-as-a-Service MVI1', 'ReleaseThemeId': 'PMB-1154', 'Key': 'VDI-1489', 'IssueType': 'Epic'},
             {'Summary': 'VDI testing and analysis for Apollo', 'ReleaseThemeId': 'PMB-1137', 'Key': 'VDI-1488', 'IssueType': 'Epic'},
             {'Summary': 'VMware Horizon 7.3.1 on HPE SimpliVity 380 Gen 10 Reference Architecture', 'ReleaseThemeId': 'PMB-1104', 'Key': 'VDI-1456', 'IssueType': 'Epic'},
             {'Summary': 'EUC Sizing Tool for HPE Simplivity 380', 'ReleaseThemeId': 'PMB-982', 'Key': 'VDI-1417', 'IssueType': 'Epic'},
             {'Summary': 'EUC Sizing Tool for HPE Simplivity 380', 'ReleaseThemeId': 'PMB-1197', 'Key': 'VDI-1417', 'IssueType': 'Epic'},
             {'Summary': 'VMware Horizon 7.3.1 on HPE SimpliVity 380 Gen 10 Reference Architecture', 'ReleaseThemeId': 'PMB-1197', 'Key': 'VDI-1653', 'IssueType': 'Epic'}]

story_list = [{'EpicId': 'VDI-1653', 'Summary': 'Refresh Existing Prometheus Grafana stack', 'Sprint': 'CloudBusters PSI 15 Sprint 1, CloudBusters PSI 14 Sprint 4, CloudBusters PSI 14 Sprint 2, ', 'Key': 'VDI-1653', 'IssueType': 'Story'},
               {'EpicId': "VDI-1653", 'Summary': 'Enable full clone balancing with an existing UPGRADED full clone pool', 'Sprint': 'PSI 14 Sprint 4, ', 'Key': 'VDI-1653', 'IssueType': 'Story'},
               {'EpicId': None, 'Summary': 'V100 Deployment in DL380 Gen10', 'Sprint': 'PSI 14 Sprint 3, ', 'Key': 'VDI-1653', 'IssueType': 'Story'},
               {'EpicId': None, 'Summary': 'P100 Deployment in DL380 Gen10', 'Sprint': 'PSI 14 Sprint 3, ', 'Key': 'VDI-1653', 'IssueType': 'Story'}]

theme = pd.DataFrame(theme_list)
theme = theme.rename(columns={"Summary":"ReleseThemeSummary", "Key":"ReleaseThemeId", "IssueType":"ReleseThemeIssueType"})
epic = pd.DataFrame(epic_list)
epic = epic.rename(columns={"Summary":"EpicSummary", "Key":"EpicId", "IssueType":"EpicIssueType"})
story = pd.DataFrame(story_list)
story.EpicId = story.EpicId.fillna("Not applicable")
story = story.rename(columns={"Summary":"StorySummary", "Key":"StoryId", "IssueType":"StoryIsuueType"})

theme_epic = pd.merge(theme, epic, on="ReleaseThemeId", sort=False, how="outer")
final = pd.merge(theme_epic, story, on="EpicId", sort=False, how="outer")
final.to_csv("ReleaseTheme.csv")