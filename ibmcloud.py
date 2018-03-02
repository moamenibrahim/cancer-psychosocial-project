import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, EntitiesOptions, KeywordsOptions
import fileinput 

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='538f0686-d66e-467f-a85a-9226cde737bb',
  password='zZuFzslKLDeC',
  version='2017-02-27')

response = natural_language_understanding.analyze(
  text='I tried to set up an appointment using the part of the website that I will display here,'
  ' and they did not get beck to me, in fact the owner told me that he reported it as spam.'
  ' I believe this is because of my race and gend',
  features=Features(
    entities=EntitiesOptions(
      emotion=True,
      sentiment=True,
      limit=2),
    keywords=KeywordsOptions(
      emotion=True,
      sentiment=True,
      limit=2)))

print(json.dumps(response, indent=2))