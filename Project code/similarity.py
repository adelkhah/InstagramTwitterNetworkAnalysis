from imgbeddings import imgbeddings
from numpy import dot
from numpy.linalg import norm
import numpy as np
from PIL import Image
import os
import instagramscraper as isp
import twitterscrape as ts
from sent2vec.vectorizer import Vectorizer
from hazm import SentEmbedding
from langdetect import detect
import json
from tqdm import tqdm


# Farsi text AI model
sentEmbedding = SentEmbedding()
sentEmbedding.load_model('sent2vec\sent2vec-naab.model')

# english text AI model
vectorizer = Vectorizer()

# image AI modle
ibed = imgbeddings()


def cos_similarity(a, b):
    aa = np.squeeze(np.asarray(a))
    bb = np.squeeze(np.asarray(b))
    return dot(aa, bb)/(norm(aa)*norm(bb))


def count_jpg_files(name):
    directory = f'instagramuser/{name}/images'

    if not os.path.exists(directory):
        os.makedirs(directory)

    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            count += 1
    return count




def image_similarity_two_user(u1, u2):
    u1image = []
    u2image = []
    u1n = count_jpg_files(u1)
    u2n = count_jpg_files(u2)
    if u1n == 0 or u2n == 0:
        return 0

    directory = f'instagramuser/{u1}/images'
    for i in range(u1n):
        path = directory + f'/image-{i}.jpg'
        u1image.append(Image.open(path))

    directory = f'instagramuser/{u2}/images'
    for i in range(u2n):
        path = directory + f'/image-{i}.jpg'
        u2image.append(Image.open(path))


    u1bed = []
    u2bed = []
    for i in range(u1n):
        u1bed.append(ibed.to_embeddings(u1image[i]))

    for i in range(u2n):
        u2bed.append(ibed.to_embeddings(u2image[i]))

    sum = 0
    for i in range(u1n):
        for j in range(u2n):
            sum += cos_similarity(u1bed[i], u2bed[j])

    count = u1n * u2n
    return sum / count



def common_instaneighbor_two_user(u1, u2):
    u1f = isp.read_follower_fromFile(u1)
    u2f = isp.read_follower_fromFile(u2)

    result = [i for i in u1f if i in u2f]

    return len(result)


def common_twitterneighbor_two_user(u1, u2):
    u1f = ts.read_follower_fromFile(u1)
    u2f = ts.read_follower_fromFile(u2)

    result = [i for i in u1f if i in u2f]

    return len(result)




def english_text_similarity(text1, text2):
    sentences = [text1, text2]
    vectorizer.run(sentences)
    vectors = vectorizer.vectors
    return cos_similarity(vectors[0], vectors[1])

def text_similarity(text1, text2):
    det1 = 'none'
    det2 = 'none'
    try:
        det1 = detect(text1)
        det2 = detect(text2)
    except:
        pass

    if det1 == 'en' and det2 == 'en':
        return english_text_similarity(text1, text2)
    elif det1 == 'fa' and det2 == 'fa':
        return sentEmbedding.similarity(text1, text2)
    else:
        return -10


def tweet_similarity(u1, u2):
    u1t = []
    u2t = []
    try:
        u1t = ts.read_comments(u1)
    except:
        pass
    try:
        u2t = ts.read_comments(u2)
    except:
        pass

    count = 1
    sum = 0
    for t1 in u1t:
        for t2 in u2t:
            res = text_similarity(t1, t2)
            if res != -10:
                count += 1
                sum += res

    ans = sum / count
    return ans


def read_comments(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'instagramuser/{name}/comments.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names


def post_similarity(u1, u2):
    u1t = []
    u2t = []
    try:
        u1t = read_comments(u1)
    except:
        pass
    try:
        u2t = read_comments(u2)
    except:
        pass

    count = 0
    sum = 0
    for t1 in u1t:
        for t2 in u2t:
            res = text_similarity(t1, t2)
            if res != -10:
                count += 1
                sum += res

    ans = sum / count
    return ans


def find_most_similar_instagram_users(numberOfuser, minimumNeighbor):
    alluser = isp.read_alluser_fromFile()
    linkpredict = []
    dick = {}
    n = len(alluser)
    for i in tqdm(range(n)):

        for j in range(i + 1, n):

            u1 = alluser[i]
            u2 = alluser[j]
            u1fol = isp.read_follower_fromFile(u1)
            u2fol = isp.read_follower_fromFile(u2)
            if (u1 in u2fol) or (u2 in u1fol):
                continue

            neighbor = common_instaneighbor_two_user(u1, u2)

            if neighbor < minimumNeighbor:
                continue

            tsim = image_similarity_two_user(u1, u2)

            linkpredict.append((u1, u2, neighbor, tsim))

    baba = sorted(linkpredict, key=lambda x: x[2], reverse=True)
    dick['similarity'] = baba[:numberOfuser]
    with open(f'trendtags/instagram_similarity_{numberOfuser}.json', 'w+') as outfile:
        json.dump(dick, outfile)


def find_most_similar_twitter_users(numberOfuser, minimumNeighbor):
    alluser = ts.read_alluser_fromFile()
    linkpredict = []
    dick = {}
    n = len(alluser)
    for i in tqdm(range(n)):

        for j in range(i + 1, n):

            u1 = alluser[i]
            u2 = alluser[j]
            u1fol = ts.read_follower_fromFile(u1)
            u2fol = ts.read_follower_fromFile(u2)
            if (u1 in u2fol) or (u2 in u1fol):
                continue

            neighbor = common_instaneighbor_two_user(u1, u2)

            if neighbor < minimumNeighbor:
                continue

            tsim = image_similarity_two_user(u1, u2)

            linkpredict.append((u1, u2, neighbor, tsim))

    baba = sorted(linkpredict, key=lambda x: x[2], reverse=True)
    dick['similarity'] = baba[:numberOfuser]

    with open(f'trendtags/twitter_similarity_{numberOfuser}.json', 'w+') as outfile:
        json.dump(dick, outfile)


if __name__ == '__main__':
    find_most_similar_instagram_users(10, 100)
    find_most_similar_twitter_users(10, 100)
