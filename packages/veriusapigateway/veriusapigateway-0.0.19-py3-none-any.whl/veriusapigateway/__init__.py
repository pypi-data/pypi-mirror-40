import requests
import json


class VeriUsAPIGateway:

    def __init__(self, apikey):
        self.apikey = apikey
        self.headers = {'Content-Type': 'application/json', "apikey": self.apikey}

    @staticmethod
    def clean_text(text):
        return text.replace('\r', ' ').replace('\b', ' ').replace('\f', ' ').replace('\v', ' ')\
            .replace('\r\n', ' ').replace('"', " ").replace('\t', ' ')\
            .replace('\n', ' ').replace('\'', ' ').replace('\\', ' ').replace('\"', ' ').strip()

    def __post_to_access(self, endpoint, text1, text2=None):
        text1 = self.clean_text(text1)
        if not text2:
            data = '{"text":"' + text1 + '"}'
        else:
            text2 = self.clean_text(text2)
            data = '{"text1":"' + text1 + '","text2":"' + text2 + '"}'
        try:
            response = requests.post("https://api.verius.com.tr/" + endpoint,
                                     headers=self.headers, data=data.encode('utf-8'))

            response_text = json.loads(response.text)
            if "result" in response_text:
                result = response_text["result"]
            elif "word_list" in response_text:
                result = list(zip(response_text["word_list"], response_text["prediction_list"]))
            elif "message" in response_text:
                result = response_text["message"]
            else:
                result = "Something went wrong. Please contact bilgi@verius.com.tr"
        except:
                result = "Something went wrong. Please contact bilgi@verius.com.tr"
        return result

    def get_text_similarity(self, text1, text2):
        return self.__post_to_access(endpoint="text-similarity", text1=text1, text2=text2)

    def get_semantic_similarity(self, text1, text2):
        return self.__post_to_access(endpoint="semantic-similarity", text1=text1, text2=text2)

    def get_language(self, text):
        return self.__post_to_access(endpoint="language-detection", text1=text)

    def get_part_of_speech_tags(self, text):
        return self.__post_to_access(endpoint="pos-tag", text1=text)

    def get_abusive(self, text):
        return self.__post_to_access(endpoint="abusive-content-detection/abusive-content-detection", text1=text)

    def get_summary(self, text):
        return self.__post_to_access(endpoint="text-summarizer", text1=text)

    def get_keywords(self, text):
        return self.__post_to_access(endpoint="keyword-extractor", text1=text)

    def get_named_entities(self, text):
        return self.__post_to_access(endpoint="entity-extraction", text1=text)

    def get_distorted(self, text):
        return self.__post_to_access(endpoint="distorted-language-detection", text1=text)

    def get_intent(self, text):
        return self.__post_to_access(endpoint="intent-detection", text1=text)

    def get_news_class(self, text):
        return self.__post_to_access(endpoint="news-classification", text1=text)

    def get_product_category(self, text):
        return self.__post_to_access(endpoint="product-category-classification", text1=text)

    def get_morphology(self, text):
        return self.__post_to_access(endpoint="morphology", text1=text)

    def get_sexual(self, text):
        return self.__post_to_access(endpoint="sexual-content-detection", text1=text)

    def get_gibberish(self, text):
        return self.__post_to_access(endpoint="gibberish-detection", text1=text)

    def get_normal(self, text):
        return self.__post_to_access(endpoint="normalization/normalization", text1=text)

    def get_deasciified(self, text):
        return self.__post_to_access(endpoint="deasciifier/deasciifier", text1=text)

    def get_sentence_tokens(self, text):
        return self.__post_to_access(endpoint="sentence-tokenizer", text1=text)

    def get_sentiment(self, text):
        return self.__post_to_access(endpoint="sentiment-analysis/sentiment-analysis", text1=text)

    def get_arabic_sentiment(self, text):
        return self.__post_to_access(endpoint="sentiment-analysis-arabic", text1=text)

    def get_arabic_news_class(self, text):
        return self.__post_to_access(endpoint="arabic-news-classification", text1=text)
