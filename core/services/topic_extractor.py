import openai
import spacy
from django.conf import settings
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class TopicExtractor:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.nlp = spacy.load('en_core_web_sm')

    def extract_topics(self, text):
        """Extract topics using OpenAI with fallback to spaCy"""
        try:
            return self.extract_topics_openai(text)
        except Exception as e:
            logger.error(f"OpenAI topic extraction failed: {e}")
            return self.extract_topics_spacy(text)

    def extract_topics_openai(self, text):
        """Extract topics using OpenAI's GPT model"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract 3-5 main topics from the following text as a comma-separated list:"},
                {"role": "user", "content": text}
            ],
            max_tokens=100
        )
        topics = response.choices[0].message['content'].split(',')
        return [topic.strip().lower() for topic in topics]

    def extract_topics_spacy(self, text):
        """Extract topics using spaCy"""
        doc = self.nlp(text)
        noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
        return list(set(noun_phrases))[:5]

    def extract_entities(self, text):
        """Extract named entities using spaCy"""
        doc = self.nlp(text)
        entities = {
            'persons': [],
            'organizations': [],
            'locations': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ in ['GPE', 'LOC']:
                entities['locations'].append(ent.text)
        
        return {k: list(set(v)) for k, v in entities.items()}