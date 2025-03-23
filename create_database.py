from sentence_transformers import SentenceTransformer
import chromadb

def split_list(list_,chunk_size):
            return [list_[i:i+chunk_size] for i in range(0,len(list_),chunk_size)]

def create_database(txt):
    class EmbeddingFn:
        def __init__(self,model_name):
            self.model = SentenceTransformer(model_name)
        
        def __call__(self,input):
            return self.model.encode(input).tolist()

    embedding_fn = EmbeddingFn("sentence-transformers/all-mpnet-base-v2")

    ids = [str(i) for i in range(len(txt))]

    chroma_cli = chromadb.Client()
    collection = chroma_cli.create_collection("chat-with-docs",embedding_function=embedding_fn)
    
    txt = split_list(txt,5000)
    ids = split_list(ids,5000)

    for txt_chunk,ids_chunk in zip(txt,ids):
        collection.add(documents=txt_chunk,ids=ids_chunk)
    
    return collection