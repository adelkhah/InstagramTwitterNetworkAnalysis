import twitterscrape as ts
from collections import defaultdict, Counter
import re
from sent2vec.vectorizer import Vectorizer
import operator
from hazm import SentEmbedding
from langdetect import detect
from tqdm import tqdm
import json

sentEmbedding = SentEmbedding()
sentEmbedding.load_model('sent2vec\sent2vec-naab.model')
vectorizer = Vectorizer()

def read_tags_insta(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'instagramuser/{name}/tags.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def sentiment_analys(text):
    det = detect(text)
    if det == 'en':
        return sentiment_analys_english(text)
    elif det == 'fa':
        return sentiment_analys_farsi(text)
    else:
        return 'none'

def sentiment_analys_farsi(text):


    # joy
    # sad
    # hate
    # love
    # angry
    # fear
    result1 = sentEmbedding.similarity('شاد و خوشحال و سرزنده و شاداب و با طروات', text)
    result2 = sentEmbedding.similarity('افسوس و ناراحتی', text)
    result3 = sentEmbedding.similarity(' بدم میاد و دوست ندارم و خوشم نمیاد', text)
    result4 = sentEmbedding.similarity(' دوست دارم و عشق', text)
    result5 = sentEmbedding.similarity(' عصبانی و خشمگین و خشم', text)
    result6 = sentEmbedding.similarity(' میترسم و ترس و وحشت', text)
    simi = []
    simi.append(result1)
    simi.append(result2)
    simi.append(result3)
    simi.append(result4)
    simi.append(result5)
    simi.append(result6)
    max_index, max_value = max(enumerate(simi), key=operator.itemgetter(1))
    if max_index == 0:
        return 'joy'
    if max_index == 1:
        return 'sad'
    if max_index == 2:
        return 'hate'
    if max_index == 3:
        return 'love'
    if max_index == 4:
        return 'angry'
    if max_index == 5:
        return 'fear'



def sentiment_analys_english(text):

    # joy
    # sad
    # hate
    # love
    # angry
    # fear

    sentences = [
        "happy grateful enjoy",
        "sad upset bad",
        "hate resent",
        "love lover",
        "angry fury rage",
        "fear afraid dangerous",
    ]
    sentences.append(text)
    vectorizer.run(sentences)
    vectors = vectorizer.vectors

    from scipy import spatial
    distan = []
    for i in range(6):
        distan.append(spatial.distance.cosine(vectors[i], vectors[6]))

    min_index, min_value = min(enumerate(distan), key=operator.itemgetter(1))
    if min_index == 0:
        return 'joy'
    if min_index == 1:
        return 'sad'
    if min_index == 2:
        return 'hate'
    if min_index == 3:
        return 'love'
    if min_index == 4:
        return 'angry'
    if min_index == 5:
        return 'fear'


def remove_short_words(s, min_length = 4) :
    words = s.split()
    long_words = [word for word in words if len(word) >= min_length]
    return ' '.join(long_words)


def most_frequent_two_word_phrases(texts):
    hashtags = defaultdict(list)
    for text in texts:
        words = text.split()
        two_word_phrases = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        for word in words:
            if word.startswith('#'):
                hashtags[ts.remove_hashtag(word)].extend(two_word_phrases)
    result = {}
    for hashtag, phrases in hashtags.items():
        phrase_counts = Counter(phrases)
        del phrase_counts[hashtag]
        result[hashtag] = sorted(phrase_counts.most_common(), key=lambda x: x[1], reverse=True)
    return result

def most_frequent_words(texts):
    hashtags = defaultdict(list)
    for text in texts:
        words = text.split()
        for word in words:
            if word.startswith('#'):
                hashtags[ts.remove_hashtag(word)].extend(words)
    result = {}
    for hashtag, words in hashtags.items():
        word_counts = Counter(words)
        del word_counts[hashtag]
        result[hashtag] = sorted(word_counts.most_common(), key=lambda x: x[1], reverse=True)
    return result

def top_n_keys(d, n):
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    top_n = [k for k, v in sorted_items[:n]]
    return top_n




def find_trend(tagnumber=10, wordnumber=5):
    commdic = {}
    all = ts.read_alluser_fromFile()
    for p in all:
        c = []
        try:
            c = ts.read_comments(p)
        except:
            pass

        commdic[p] = ts.find_hashtags_list(c)

    counttag = {}
    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] = 0

    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] += 1

    textswith = []
    textswithout = []
    all = ts.read_alluser_fromFile()
    for u in all:
        comment = []
        try:
            comment = ts.read_comments(u)
        except:
            pass
        for c in comment:
            pp = re.sub('\u200c', '', c)
            ppp = remove_short_words(pp, 4)
            textswith.append(pp)
            textswithout.append(ppp)

    trends = most_frequent_words(textswithout)
    trends2 = most_frequent_two_word_phrases(textswith)
    trend = top_n_keys(counttag, tagnumber)
    newt2 = {}
    newt = {}
    tagtrend = {}
    for t in trend:
        tagtrend[t] = counttag[t]
        newt[t] = trends.get(t, [])[:wordnumber]
        newt2[t] = trends2.get(t, [])[:wordnumber]

    return (tagtrend ,newt, newt2)




def trend_tag_sentiment(tagnumber=10):
    commdic = {}
    alltweetfortag = {}
    all = ts.read_alluser_fromFile()
    for p in all:
        c = []
        try:
            c = ts.read_comments(p)
        except:
            pass

        commdic[p] = ts.find_hashtags_list(c)

    counttag = {}
    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] = 0
            alltweetfortag[ts.remove_hashtag(t)] = []

    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] += 1

    textswith = []
    textswithout = []
    all = ts.read_alluser_fromFile()
    for u in all:
        comment = []
        try:
            comment = ts.read_comments(u)
        except:
            pass
        for c in comment:
            pc = re.sub('\u200c', '', c)
            pp = re.sub('\u2069', '', pc)
            ppp = remove_short_words(pp, 4)
            textswith.append(pp)
            textswithout.append(ppp)

    for tex in textswith:
        taa = ts.find_hashtags(tex)
        for tata in taa:
            alltweetfortag.get(ts.remove_hashtag(tata), []).append(tex)

    tagsent = {}
    for tag in alltweetfortag:
        tagsent[tag] = {'joy': 0 ,'sad': 0,'hate': 0,
                        'love': 0,'angry': 0,'fear': 0, 'none' : 0}

    trend = top_n_keys(counttag, tagnumber)

    for tag in trend:
        for sentence in tqdm(alltweetfortag[tag]):
            ans = sentiment_analys(sentence)
            tagsent[tag][ans] += 1

    trendtagsent = {}
    for tag in trend:
        trendtagsent[tag] = tagsent[tag]

    return trendtagsent



if __name__ == '__main__':

    wordn = 2
    tagn = 15
    trends = find_trend(tagn, wordn)
    t = trend_tag_sentiment(tagn)

    with open(f'trendtags/trendtags_{tagn}.json', 'w+') as outfile:
        json.dump(trends[0], outfile)

    with open(f'trendtags/trendtagword{tagn}_{wordn}.json', 'w+') as outfile:
        json.dump(trends[1], outfile)

    with open(f'trendtags/trendtag2word{tagn}_{wordn}.json', 'w+') as outfile:
        json.dump(trends[2], outfile)

    with open(f'trendtags/trendtagsentiment_{tagn}.json', 'w+') as outfile:
        json.dump(t, outfile)


