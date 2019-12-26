import re
import json
from nltk.tokenize import word_tokenize
import operator
import json
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams
import nltk
import string
import vincent
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

filename = 'jokowi.json'
clean_filename = 'clean_'+filename
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    # emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    s = re.sub(r"http\S+", "", s)
    s = stemming(s)
    return tokens_re.findall(s)


def process(s, lowercase=True):
    tokens = tokenize(s)
    # print('tokenize : {}'.format(tokens))
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]

    return tokens


def stemming(string):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    output = stemmer.stem(string)
    return output


def clean_data():
    clean_file = open(clean_filename, 'w')
    with open(filename, 'r') as file:
        for line in file:
            text = ''
            if(line.strip()):
                tweet = json.loads(line)
                print('cleaning: {}'.format(tweet['id']))
                if(tweet['truncated']):
                    text = {
                        'text': tweet['extended_tweet']['full_text'],

                    }
                else:
                    text = {
                        'text': tweet['text']
                    }

                hashtags = []
                for hashtag in tweet['entities']['hashtags']:
                    hashtags += [hashtag['text']]

                append_text = {
                    'screen_name': tweet['user']['screen_name'],
                    'timestamp': tweet['timestamp_ms'],
                    'hashtag': hashtags,
                    'tweet_id': tweet['id'],
                    'source': tweet['source']
                }
                text.update(append_text)
                clean_file.write(json.dumps(text))
                clean_file.write('\n')
    clean_file.close()


def clean_data_from_twitterscaper():
    file = open(filename, 'r')
    clean_file = open(clean_filename, 'w')
    tweets = file.readline()
    tweets = json.loads('{"data":' + tweets + '}')
    print("processing: {} data".format(len(tweets['data'])))
    for item in tweets['data']:
        print('cleaning: {}'.format(item['text']))
        data = {
            'text': item['text'],
            'timestamp': item['timestamp_epochs'],
            'tweet_id': item['tweet_id'],
            'hashtag': item['hashtags'],
            'screen_name': item['screen_name']
        }
        clean_file.write(json.dumps(data))
        clean_file.write('\n')
    print('finish')
    clean_file.close()


# clean_data()
# clean_data_from_twitterscaper()
# exit()
indonesian_stopwords = StopWordRemoverFactory().get_stop_words()
punctuation = list(string.punctuation)
stop = indonesian_stopwords + stopwords.words('english') + punctuation + \
    ['jokowi', 'yg', 'ada', 'pak', 'ini', 'juga',
        'dan', 'rt', '…', 'mau', 'jangan', 'tanya', 'dlm', 'sering', 'jadi']

word_count = 0
hashtag_all = []
source_all = []
print('Processing')
with open(clean_filename, 'r') as f:
    count_all = Counter()
    hashtag_counter = Counter()
    source_counter = Counter()
    for line in f:
        if(line.strip()):
            word_count += 1
            print('tweet processed: {}'.format(word_count))
            tweet = json.loads(line)

            # process tweet
            print('processing tweet of {}'.format(tweet['tweet_id']))
            terms_all = [term for term in process(
                tweet['text']) if term not in stop and not term.startswith(('#', '@'))]
            count_all.update(terms_all)

            # process hashtag
            if(tweet['hashtag']):
                print('processing hashtag of {}'.format(tweet['tweet_id']))
                hashtag_all = [hashtag.lower()
                               for hashtag in tweet['hashtag']]
                hashtag_counter.update(hashtag_all)

            # process source
            if(tweet['source']):
                print('processing source of {}'.format(tweet['tweet_id']))
                source_data = ['android', 'ios']
                s = re.sub(r"http\S+", "", tweet['source'])  # remove url
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', s)
                source_all = [source.lower()
                              for source in cleantext.split() if source.lower() in source_data]
                source_counter.update(source_all)
            
            print('-----------------')

    word_freq = count_all.most_common(20)
    hashtag_freq = hashtag_counter.most_common(20)
    source_freq = source_counter.most_common(20)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('result_' + filename)
    result_file = open('result_'+filename)
    result = {
        'text_result': word_freq,
        'hashtag_result': hashtag_freq,
        'source_result': source_counter
    }
    result_file.write(json.dumps(result))
    result_file.close()
    print(word_freq)
