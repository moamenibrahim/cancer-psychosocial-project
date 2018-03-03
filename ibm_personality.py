from watson_developer_cloud import PersonalityInsightsV3
import os,sys,json

personality_insights = PersonalityInsightsV3(
  version='2017-10-13',
  username='fb0ff3e8-a0c8-4ad7-a0f7-ba2b65bbb34e',
  password='mEkXMY2PHyoe'
)

# profile(content, content_type='application/json', content_language=None,
#   accept='application/json', accept_language=None, raw_scores=None,
#   csv_headers=None, consumption_preferences=None)


with open("".join(os.path.dirname(__file__), './profile.json')) as profile_json:
  profile = personality_insights.profile(
    profile_json.read(), content_type='application/json',
    raw_scores=True, consumption_preferences=True)

print(json.dumps(profile, indent=2))