import numpy as np
import jarowinkler

class KSimilarityCluster(object):
    def __init__(self, k=2, partitions=[]):
        self._k = k
        self._partitions = partitions

    def index(self, features, key):
        indexes = self._partitions.similarity(features)
        if len(indexes) == 0:
            self._partitions.create_partition(self._k, [(key, features)])
            return
        self._partitions.add_item(indexes[0], (key, features))
        if len(indexes) > 1:
            self._partitions.merge(indexes)

    def dump(self, dirname):
        for index, partition in enumerate(self._partitions):
            write("{}/{}.data".format(dirname, index), partition)


def write(filename, partition):
    with open(filename, 'w') as f:
        f.write(partition.export())


class Partitions(object):
    def __init__(self, threshold = 0.7, partitions=[]):
        self._threshold = threshold
        self._partitions = partitions

    def similarity(self, vector):
        return [index for index, partition in enumerate(self._partitions) if partition.similarity(vector) > self._threshold]

    def create_partition(self, k, items):
        self._partitions.append(Partition(k, items))

    def add_item(self, index, item):
        self._partitions[index].add(item)

    def __iter__(self):
        return iter(self._partitions)

    def merge(self, indexes):
        for index in indexes[1:]:
            self._partitions[indexes[0]].merge(self._partitions[index])
        self._partitions = [partition for index, partition in enumerate(self._partitions) if index not in indexes[1:]]


class Partition(object):
    def __init__(self, k, items=[]):
        self._k = k
        self._items = items

    def add(self, item):
        self._items.append(item)

    def merge(self, partition):
        self._items.extend(partition._items)

    def similarity(self, vector):
        return max([jarowinkler.jarowinkler_similarity(item, vector) for item in self._random_items])

    def export(self):
        return "\n".join(["{} {}".format(*item) for (item) in self._items])

    def __len__(self):
        return len(self._items)

    @property
    def _random_items(self):
        return (self._items[i][1] for i in np.random.choice(range(len(self._items)), min(self._k, len(self._items)), replace=False))

def create(k, threshold):
    return KSimilarityCluster(k, Partitions(threshold, []))
