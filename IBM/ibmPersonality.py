from watson_developer_cloud import PersonalityInsightsV3
import os,sys,json


class AlchemyPersonalityDetection(object):
  def __init__(self):
    self.personality_insights = PersonalityInsightsV3(
      version='2017-10-13',
      username='fb0ff3e8-a0c8-4ad7-a0f7-ba2b65bbb34e',
      password='mEkXMY2PHyoe'
    )

  def get_response(self, fileName):
    with open(fileName) as profile_json:
      profile = self.personality_insights.profile(
        profile_json.read(), content_type='application/json',
        raw_scores=True, consumption_preferences=True)
    print(json.dumps(profile, indent=2))


AlchemyPD=AlchemyPersonalityDetection()
AlchemyPD.get_response('profile.json')
