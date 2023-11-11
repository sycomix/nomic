"""
Maps text by using the nomic-embed-text-v1 model inference endpoint.

Note, this is mainly a demo.
You should just add_text to a project and let Atlas internally handle the embedding for you.
"""
from nomic import atlas, embed
import numpy as np
from datasets import load_dataset

dataset = load_dataset('ag_news')['train']

max_documents = 10000
subset_idxs = np.random.choice(len(dataset), size=max_documents, replace=True).tolist()
documents = [dataset[i] for i in subset_idxs]

usages = []

def print_total_tokens(usages):
    return sum(usage['total_tokens'] for usage in usages)

def generate_embeddings(documents):
    batch_size = 256
    document_embeddings = []

    batch = []
    for idx, doc in enumerate(documents):
        batch.append(doc['text'])
        if (idx + 1) % batch_size == 0 or idx == len(documents):
            batch_embeddings = embed.text(texts=batch, model='nomic-embed-text-v1')
            usages.append(batch_embeddings['usage'])
            document_embeddings.extend(iter(batch_embeddings['embeddings']))
            print(usages[-1], print_total_tokens(usages))

            batch = []

    return np.array(document_embeddings)

document_embeddings = generate_embeddings(documents)

print(document_embeddings.shape)
response = atlas.map_embeddings(embeddings=document_embeddings, data=documents, topic_label_field='text', build_topic_model=True)
print(response)