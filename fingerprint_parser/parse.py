import itertools
import jaro
import bs4
import glob
import os.path as path

def flatten(list_of_lists):
    return itertools.chain.from_iterable(list_of_lists)

def extract_url(string):
    return path.basename(string).replace(".html", "")

def read(filename):
    with open(filename, 'r') as f:
        return f.read()

def write(filename, contents):
    with open(filename, 'w') as f:
        f.write(contents)

def script_features(value, url, element):
    return 'self_hosted' if value.startswith('http') and value.find(url) > -1 else 'external_host'

def files_iterator(data_dir):
    return ((filename, extract_url(filename)) for filename in glob.glob(data_dir + "*"))

class TagFeatures(object):
    def __init__(self, handlers):
        self._handlers = handlers

    def extract(self, url, element):
        return self._features(url, element, self._handlers.get(element.name, self._default_attributes))

    def _features(self, url, element, extractors):
        return flatten([extract.features(url, element) for extract in extractors])

    @property
    def _default_attributes(self):
        return [SingleValueAttribute('id')]

class Fingerprint(object):
    def __init__(self, encoder, tag_features):
        self._encoder = encoder
        self._tag_features = tag_features

    def features(self, url, document):
        return [] if not hasattr(document, 'body') else self.get(url, document.body)

    def get(self, url, element):
        features = [self._encoder.add(feature) for feature in self._tag_features.extract(url, element)]
        children_features = flatten([self.get(url, child) for child in element.children if not isinstance(child, bs4.element.NavigableString)])
        return features + list(children_features)

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

class SingleValueAttribute(object):
    def __init__(self, attribute_name, extra_features=[]):
        self._attribute_name = attribute_name
        self._extra_features = extra_features

    def features(self, url, dom_element):
        return self._all_features(url, dom_element) if self._valid(dom_element) else []

    def _all_features(self, url, dom_element):
        return (feature(dom_element.attrs[self._attribute_name], url, dom_element) for feature in self._feature_extractors)

    def _valid(self, dom_element):
        return self._attribute_name in dom_element.attrs

    @property
    def _feature_extractors(self):
        return [self._value] + self._extra_features

    def _value(self, value, url, element):
        return "{}.{}".format(element.name, value)


finger_print = Fingerprint(Signature([], Encoder()), TagFeatures({
    'script': [SingleValueAttribute('src', [script_features]), SingleValueAttribute('id')]
}))
features = {}

data_dir = "../data/html/"
for filename, url in files_iterator(data_dir):
    try:
        features[url] = finger_print.features(url, bs4.BeautifulSoup(read(filename), "html.parser"))
    except:
        print (filename)

similarity = ["first,second,similarity"]
similarity.extend(["{},{},{}".format(site1, site2, jaro.jarowinkler_similarity(features[site1], features[site2])) for site1, site2 in itertools.combinations(features.keys(), 2)])
write("similarity.csv", "\n".join(similarity))
