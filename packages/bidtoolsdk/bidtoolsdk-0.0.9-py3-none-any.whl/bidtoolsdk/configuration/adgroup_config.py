import pandas as pd
from bidtoolsdk.settings import os
import requests
import json
from enum import Enum


class AdGroupConfigColumns(Enum):
    AdGroupId = 'ad_group_id'
    AdGroupName = 'ad_group_name'
    BidStrategy = 'bid_strategy'
    CampaignId = 'campaign_id'
    CampaignName = 'campaign_name'
    CpcConstraint = 'cpc_constraint'
    Platform = 'platform'
    PlatformId = 'platform_id'
    TargetPosition = 'target_position'
    SearchLostISRank = 'search_lost_is_rank'
    Device = 'device'
    Exclude = 'exclude'


def get_adgroup_config_df(platform_id, is_staging=False):

    bidtoolapibaseurl = os.environ.get("bidtoolapibaseurl")
    response = requests.post(
        url=f'{bidtoolapibaseurl}/bid-tool-configurations',
        auth=(os.environ.get('bidtoolapiuser'), os.environ.get('bidtoolapipass')),
        json={"platform_id": platform_id, "is_staging": is_staging}
    )

    configs = pd.DataFrame.from_records(json.loads(response.content))

    return configs.rename(
        columns={col: AdGroupConfigColumns(col).name for col in configs.columns}
    )
