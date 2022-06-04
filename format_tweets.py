import json
import sys
import os


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def formatRawJsons(filepath):
    with open(filepath, encoding='cp850') as f:
        lines = f.read().splitlines()

    formattedFilepath = filepath.split(
        '.')[0] + "-formatted." + filepath.split('.')[1]

    with open(formattedFilepath, "w", encoding='cp850') as f:
        f.write("[")
        for line in lines:
            f.write(line + ",\n")
        # f.seek(-1, os.SEEK_CUR)
        # f.truncate()
        # f.write("]")

    os.system("sed -i '$ s/.$/]/' " + formattedFilepath)

    return formattedFilepath


def createAdjList(tweets):
    result = {}

    for tweet in tweets:
        hashtags = tweet['entities']['hashtags']
        for hashtag in hashtags:
            sourceNode = hashtag['text']
            if sourceNode not in result:
                result[sourceNode] = set(())
            for hashtag in hashtags:
                result[sourceNode].add(hashtag['text'])

    return result


def createEdgeList(tweets):
    result = {
        "Source": [],
        "Target": []
    }

    for tweet in tweets:
        hashtags = tweet['entities']['hashtags']
        for hashtag in hashtags:
            result['Source'].append(hashtag['text'])
            for hashtag in hashtags:
                result['Target'].append(hashtag['text'])

    return result


def saveGephiData(data, name="output"):
    f = open(name + ".json", "w")
    json.dump(data, f, cls=SetEncoder)
    f.close()


filepath = sys.argv[1]
formattedFilepath = formatRawJsons(filepath)
f = open(formattedFilepath, encoding='cp850')
tweets = json.load(f)
f.close()
adjList = createAdjList(tweets)
saveGephiData(adjList, "adj-list")
edgeList = createEdgeList(tweets)
saveGephiData(edgeList, "edge-list")
