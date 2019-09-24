import sys

import fasttext
from annoy import AnnoyIndex


def create_trees():
    model = fasttext.load_model(sys.argv[1])
    labels = model.labels

    dim = model.get_dimension()
    distance_type = 'angular'
    t = AnnoyIndex(dim, distance_type)

    label_index = {}
    for i, label in enumerate(labels):
        v = model[label]
        t.add_item(i, v)

    t.build(50)
    t.save('tree.ann')
    with open("tree_labels.txt", "wt") as file_:
        file_.write("\n".join(labels))
    with open("tree_dim.txt", "wt") as file_:
        file_.write(str(dim))


def load_trees():
    dim = int(open("tree_dim.txt").read())
    tree = AnnoyIndex(dim, 'angular')
    tree.load('tree.ann')
    labels = [label.rstrip("\r\n") for label in open("tree_labels.txt").readlines()]
    labels_index = {}
    for i, label in enumerate(labels):
        labels_index[label] = i
    return dim, tree, labels, labels_index


def get_similars(tree, labels, labels_index, label):
    print("label:", label)
    import ipdb; import pprint; ipdb.set_trace(context=10); pass
    for result_index, score in zip(*tree.get_nns_by_item(labels_index[label], 25, include_distances=True)):
        print("\t", labels[result_index])


def main():
    create_trees()
    dim, tree, labels, labels_index = load_trees()
    get_similars(tree, labels, labels_index, "heart_failure")
    get_similars(tree, labels, labels_index, "lay_health_workers")
    get_similars(tree, labels, labels_index, "hospital-associated_infections")

    print("hola")

if __name__ == '__main__':
    main()
