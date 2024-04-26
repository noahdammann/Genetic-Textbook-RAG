from tqdm.auto import tqdm  # for progress bar
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.document_loaders import DirectoryLoader
from datasets import load_dataset
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as PineconeStore

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = os.getenv("PINECONE_API_KEY")
spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

# configure client
pc = Pinecone(api_key=api_key)

def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

dataset = load_docs("gene-control")

def split_docs(documents, chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

data = split_docs(dataset)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
]

index_name = 'gene-control-rag'
existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

# check if index already exists (it shouldn't if this is first time)
if index_name not in existing_indexes:
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of ada 002
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")

batch_size = 50

for i in tqdm(range(0, len(data), batch_size)):
    i_end = min(len(data), i+batch_size)
    # get batch of data
    batch = data[i:i_end]
    # generate unique ids for each chunk
    ids = [f"doc-{i + j}" for j, _ in enumerate(batch)]
    # get text to embed
    texts = [f"{x.page_content}" for i, x in enumerate(batch)]
    # embed text
    embeds = embed_model.embed_documents(texts)
    # get metadata to store in Pinecone
    metadata = [
        {'text': x.page_content } for i, x in enumerate(batch)
    ]
    # add to Pinecone
    index.upsert(vectors=zip(ids, embeds, metadata))

text_field = "text"  # the metadata field that contains our text

# initialize the vector store object
vectorstore = PineconeStore(
    index, embed_model, text_field
)

def augment_prompt(query: str):
    # get top 3 results from knowledge base
    results = vectorstore.similarity_search(query, k=2)
    # get the text from the results
    source_knowledge = "\n".join([x.page_content for x in results])
    # feed into an augmented prompt
    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augmented_prompt

query = "" # add query

# create a new user prompt
prompt = HumanMessage(
    content=augment_prompt(query)
)
# add to messages
messages.append(prompt)

res = chat(messages)

print(res.content)