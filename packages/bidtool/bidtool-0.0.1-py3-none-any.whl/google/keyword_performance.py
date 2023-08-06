import requests
import pandas as pd
from io import StringIO
from enum import Enum
from settings import os


class Columns(Enum):
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


def get_keyword_performance_df(platform_id, days_from_today=14, columns=None):

    bidtoolapibaseurl = os.environ.get("bidtoolapibaseurl")
    response = requests.post(
        url=f'{bidtoolapibaseurl}/keyword-performance-report',
        auth=(os.environ.get('bidtoolapiuser'), os.environ.get('bidtoolapipass')),
        json={
            "platform_id": platform_id,
            "days_from_today": days_from_today,
            "columns": [col.value for col in columns]
        }
    )

    return pd.read_csv(StringIO(response.content))
