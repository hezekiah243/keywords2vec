from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser


def create_index():
    schema = Schema(
        label=NGRAMWORDS(
            minsize=2, maxsize=10,
            stored=True, field_boost=1.0,
            tokenizer=None, at='start',
            queryor=False, sortable=False
        ),
        pos=NUMERIC(stored=True, sortable=True)
    )
    ix = create_in("indexdir", schema)
    writer = ix.writer(procs=4)
    with open("labels.txt", "rt") as file_:
        for index, label in enumerate(file_):
            writer.add_document(label=label.strip(), pos=index+1)
            if index > 0 and index % 50000 == 0:
                print(index)
    writer.commit()


def load_index():
    ix = open_dir("indexdir", readonly=True)
    return ix

def query(ix, text, top_n=100):
    print("searching")
    with ix.searcher() as searcher:
        query = QueryParser("label", ix.schema).parse(text)
        results = searcher.search(query,limit=top_n, sortedby="pos")
        print(results)
        for result in results:
            import ipdb; import pprint; ipdb.set_trace(context=10); pass
            print(result)

def main():
    #create_index()
    ix = load_index()
    query(ix, "heart_failure")

if __name__ == '__main__':
    main()
    # for i in range(topN):
    #     print(results[i]['title'], str(results[i].score), results[i]['textdata'])

#
# with ix.searcher() as searcher:
#     query = QueryParser("label", ix.schema).parse("*heart_f*")
#     results = searcher.search(query, limit=20)
#     print(results[0:10])
