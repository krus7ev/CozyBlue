import itertools
import jaro
import bs4
import glob


def read(filename):
    with open(filename, 'r') as f:
        return f.read()

def write(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)

data_dir = "../data/html/"

class Fingerprint(object):
    def __init__(self, encoder):
        self._encoder = encoder

    def features(self, document):
        return [] if not hasattr(document, 'body') else self.get(document.body)

    def get(self, element):
        children = [child for child in element.children if not isinstance(child, bs4.element.NavigableString)]
        if len(children) == 1:
            return self.get(children[0])
        result = []
        if 'id' in element.attrs:
            result.append(self._encoder.add("{}#{}".format(element.name, element.attrs['id'])))

        # if 'class' in element.attrs:
        #     result.append("{}.{}".format(element.name, ' '.join(element.attrs['class'])))
        for child in children:
            result.extend(self.get(child))
        return result

class Encoder(object):
    def __init__(self):
        self._data = {}

    def id(self, code):
        if not code in self._data:
            self._data[code] = len(self._data)
        return self._data[code]

class Signature(object):
    def __init__(self, items, encoder):
        self._items = items
        self._encoder = encoder

    def add(self, item):
        item_id = self._encoder.id(item)
        if len(self._items) == 0 or item_id != self._items[-1]:
            self._items.append(item_id)
        return item_id

s = Signature([], Encoder())
s = Fingerprint(s)
features = {}
for filename in glob.glob(data_dir + "*"):
    try:
        features[filename] = s.features(bs4.BeautifulSoup(read(filename), "html.parser"))
    except:
        print (filename)


similarity = ["first,second,similarity"]
similarity.extend(["{},{},{}".format(site1, site2, jaro.jarowinkler_similarity(features[site1], features[site2])) for site1, site2 in itertools.combinations(features.keys(), 2)])
write("similarity.csv", "\n".join(similarity))
