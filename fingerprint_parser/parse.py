import itertools
import bs4
import glob
import os.path as path
import numpy as np
import cluster

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

def script_features(value, url, dom_element):
    return 'self_hosted' if value.startswith('http') and value.find(url) > -1 else 'external_host'

def files_iterator(data_dir):
    return ((filename, extract_url(filename)) for filename in glob.glob(data_dir + "*"))

def raw_value(value, url, dom_element):
    return "{}.{}".format(dom_element.name, value)


class Fingerprint(object):
    def __init__(self, encoder, tag_features):
        self._encoder = encoder
        self._tag_features = tag_features

    def features(self, url, document):
        return [] if not hasattr(document, 'body') else self.get(url, document)

    def get(self, url, element):
        features = [self._encoder(feature) for feature in self._tag_features.extract(url, element)]
        children_features = flatten([self.get(url, child) for child in element.children if not isinstance(child, bs4.element.NavigableString)])
        return features + list(children_features)

class SingleValueAttribute(object):
    def __init__(self, attribute_name, features=[raw_value]):
        self._attribute_name = attribute_name
        self._features = features

    def features(self, url, dom_element):
        return self._all_features(url, dom_element) if self._valid(dom_element) else []

    def _all_features(self, url, dom_element):
        return (feature(dom_element.attrs[self._attribute_name], url, dom_element) for feature in self._features)

    def _valid(self, dom_element):
        return self._attribute_name in dom_element.attrs

class TagFeatures(object):
    def __init__(self, handlers, default=[SingleValueAttribute('id')]):
        self._handlers = handlers
        self._default_attributes = default

    def extract(self, url, element):
        return self._features(url, element, self._handlers.get(element.name, self._default_attributes))

    def _features(self, url, element, extractors):
        return flatten([extract.features(url, element) for extract in extractors])


def identity(x): return x
def remove_tag(x): return x.split(".", 1)[1]
#finger_print = Fingerprint(identity, TagFeatures({ 'script': [SingleValueAttribute('src')] }, []))
#finger_print = Fingerprint(remove_tag, TagFeatures({ 'link': [SingleValueAttribute('href')] }, []))
finger_print = Fingerprint(hash, TagFeatures({}))
features = {}


data_dir = "../data/html/"
for filename, url in files_iterator(data_dir):
    try:
        features[url] = finger_print.features(url, bs4.BeautifulSoup(read(filename), "html.parser"))
    except:
        print (filename)

c = cluster.create(2, 0.5)
for site, features in features.items():
    c.index(features, site)
c.dump("output", 2) # dump threshold
#similarity.extend(["{},{},{}".format(site1, site2, jarowinkler.jarowinkler_similarity(features[site1], features[site2])) for site1, site2 in itertools.combinations(features.keys(), 2)])
#write("similarity.csv", "\n".join(similarity))
