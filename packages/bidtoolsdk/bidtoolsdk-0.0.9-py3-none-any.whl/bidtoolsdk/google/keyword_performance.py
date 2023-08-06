import requests
import pandas as pd
from io import BytesIO
from enum import Enum
from bidtoolsdk.settings import os


class KeywordPerformanceColumns(Enum):
    Date = 'Date'
    CampaignId = 'CampaignId'
    CampaignName = 'CampaignName'
    AdGroupId = 'AdGroupId',
    AdGroupName = 'AdGroupName'
    CpcBid = 'CpcBid'
    Device = 'Device'
    AverageCost = 'AverageCost'
    SearchExactMatchImpressionShare = 'SearchExactMatchImpressionShare'
    SearchImpressionShare = 'SearchImpressionShare'
    Conversions = 'Conversions'
    Cost = 'Cost'
    Impressions = 'Impressions'
    Clicks = 'Clicks'
    Criteria = 'Criteria'
    Id = 'Id'
    CostPerConversion = 'CostPerConversion'
    SystemServingStatus = 'SystemServingStatus'
    KeywordMatchType = 'KeywordMatchType'
    QualityScore = 'QualityScore'
    AveragePosition = 'AveragePosition'
    SearchRankLostImpressionShare = 'SearchRankLostImpressionShare'
    LabelIds = 'LabelIds'
    Labels = 'Labels'


def get_keyword_performance_df(platform_id, days_from_today=14, columns=[]):

    bidtoolapibaseurl = os.environ.get("bidtoolapibaseurl")
    response = requests.post(
        url=f'{bidtoolapibaseurl}/keyword-performance-report',
        auth=(os.environ.get('bidtoolapiuser'), os.environ.get('bidtoolapipass')),
        json={
            "platform_id": platform_id,
            "days_from_today": days_from_today,
            "columns": [col.value for col in columns] if len(columns) > 0 else None
        }
    )

    return pd.read_csv(BytesIO(response.content))
