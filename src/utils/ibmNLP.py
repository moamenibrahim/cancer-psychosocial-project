import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class AlchemyNLPunderstanding():
    def __init__(self, apikey: str):
        """
        Natural Language Understanding includes a set of text analytics features that 
        you can use to extract meaning from unstructured data.
        """
        authenticator = IAMAuthenticator('{apikey}')
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
            )
        self.personality_insights = PersonalityInsightsV3(
            version='2022-04-07',
            authenticator=authenticator
            )
        self.natural_language_understanding.set_service_url('{url}')


    def get_nlp_analysis(self, text: str):
        """ Get text analysis features: Sentiment, Named entities, Keywords """
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
            return json.dumps(response)
        except Exception as e:
            print("Error: unsupported text language for natural language understanding {e}")

    def get_personality(self, text: str):
        """ Get personality detection (Deprecated) """
        profile = self.personality_insights.profile(
                text, content_type='application/json',
                raw_scores=True, consumption_preferences=True)
        return json.dumps(profile)

# nlp_understanding = AlchemyNLPunderstanding()
# print(nlp_understanding.get_nlp_analysis('I tried to set up an appointment using the part of the website that I will display here and they did not get beck to me, in fact the owner told me that he reported it as spam.'))
# nlp_understanding.get_personality('and they did not get beck to me, in fact the owner told me that he reported it as spam.')
