import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
import sys


class AlchemyNLPunderstanding(object):
    def __init__(self):
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            username='538f0686-d66e-467f-a85a-9226cde737bb',
            password='zZuFzslKLDeC',
            version='2017-02-27')

    def get_response(self, text):
        try:
            response = self.natural_language_understanding.analyze(
                text=text,
                features=Features(
                    sentiment=SentimentOptions(),
                    entities=EntitiesOptions(
                        emotion=True,
                        sentiment=True,
                        limit=2),
                    keywords=KeywordsOptions(
                        emotion=True,
                        sentiment=True,
                        limit=2)))
            return json.dumps(response, indent=2)
        except:
            print("Error: unsupported text language for natural language understanding")


# NLP_understanding = AlchemyNLPunderstanding()
# print(NLP_understanding.get_response('I tried to set up an appointment using the part of the website that I will display here,'
#                                      ' and they did not get beck to me, in fact the owner told me that he reported it as spam.'
#                                      ' I believe this is because of my race and gend'))
