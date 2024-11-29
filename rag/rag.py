import os
from llama_parse import LlamaParse
from llama_parse.base import ResultType, Language
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.retrievers.document_compressors import flashrank_rerank
from langchain.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.documents import Document

#Configure your API
os.environ["LLAMA_CLOUD_API_KEY"]= "API_KEY"

#Define parser
parser = LlamaParse(result_type=ResultType.MD,language=Language.ENGLISH)

#Parsing into the documents variable
documents = LlamaParse(
    result_type=ResultType.MD
).load_data(
    "PsychologyKeyConcepts.pdf"
)

#Writing the result of parsing into the file psychology_data.md
filename = "psychology_data.md"
with open(filename, 'w') as f:
    f.write(documents[0].text)

#putting the text of psychology_data into a doc variable
with open("psychology_data.md", encoding='utf-8') as f:
    doc = f.read()


r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""]
)

#Splitting the text
docs = r_splitter.split_text(doc)
print("data has been splitted.")

# Convert the list of strings to a list of Document objects
docs = [Document(page_content=d) for d in docs]
embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
print("embeddings created.")

#defining vector database directory
persist_directory = "Psycho_db"

# Load the database
vecdb = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"), collection_name="rag-chroma")

vecdb.add_documents(docs)
print("data has been added to the database.")
vecdb.persist()
print("Data has been ingested into vector database.")


#Testing
question = "what is depression?"
documents = vecdb.similarity_search(question,k=5)

print(documents[0].page_content)