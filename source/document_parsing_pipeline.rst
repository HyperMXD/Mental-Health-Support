Parsing, Embedding, and Querying
================================

This document provides a comprehensive guide to understanding and working with the given Python script. The script uses **LlamaParse**, **LangChain**, and **Chroma** to parse a psychology PDF, create embeddings, and store data in a vector database for similarity-based retrieval.

Overview
--------

The script performs the following tasks:

1. **Parse a PDF file**: Extracts text and saves it into a Markdown file.
2. **Text splitting**: Splits the extracted text into manageable chunks for processing.
3. **Embeddings**: Converts the text chunks into numerical representations for storage and querying.
4. **Vector database setup**: Stores the embeddings in a Chroma vector database for similarity search.
5. **Query the database**: Retrieves relevant information from the database based on similarity.

Dependencies
------------

Ensure the following Python libraries are installed:

- `llama_parse`
- `langchain`
- `langchain_community`
- `chromadb`

To install the required dependencies, use:

.. code-block:: bash

   pip install llama_parse langchain chromadb

Environment Configuration
-------------------------

Set up the Llama Cloud API key as an environment variable:

.. code-block:: python

   import os
   os.environ["LLAMA_CLOUD_API_KEY"] = "API_KEY"

Replace ``API_KEY`` with your Llama Cloud API key.

Step-by-Step Explanation
------------------------

1. **Import Libraries**

   Import the required modules for parsing, text splitting, embeddings, and vector database operations:

   .. code-block:: python

      from llama_parse import LlamaParse
      from llama_parse.base import ResultType, Language
      from langchain.text_splitter import RecursiveCharacterTextSplitter
      from langchain.vectorstores import Chroma
      from langchain_community.embeddings.ollama import OllamaEmbeddings
      from langchain_core.documents import Document

2. **Define the Parser**

   Configure the parser to extract data from the PDF file:

   .. code-block:: python

      parser = LlamaParse(result_type=ResultType.MD, language=Language.ENGLISH)

3. **Parse the PDF**

   Load the text from the PDF and save it to a Markdown file:

   .. code-block:: python

      documents = parser.load_data("PsychologyKeyConcepts.pdf")

      # Save to a file
      filename = "psychology_data.md"
      with open(filename, 'w') as f:
          f.write(documents[0].text)

4. **Load and Split Text**

   Load the text from the Markdown file and split it into smaller chunks:

   .. code-block:: python

      with open("psychology_data.md", encoding='utf-8') as f:
          doc = f.read()

      r_splitter = RecursiveCharacterTextSplitter(
          chunk_size=2000,
          chunk_overlap=0,
          separators=["\n\n", "\n", "(?<=\. )", " ", ""]
      )
      docs = r_splitter.split_text(doc)
      docs = [Document(page_content=d) for d in docs]

      print("Text has been split.")

5. **Create Embeddings**

   Use the `OllamaEmbeddings` model to create embeddings for the text chunks:

   .. code-block:: python

      embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
      print("Embeddings created.")

6. **Set Up the Vector Database**

   Define and populate the Chroma vector database:

   .. code-block:: python

      persist_directory = "Psycho_db"

      vecdb = Chroma(
          persist_directory=persist_directory,
          embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"),
          collection_name="rag-chroma"
      )

      vecdb.add_documents(docs)
      vecdb.persist()

      print("Data has been ingested into the vector database.")

7. **Query the Database**

   Perform a similarity search on the database:

   .. code-block:: python

      question = "What is depression?"
      documents = vecdb.similarity_search(question, k=5)

      print(documents[0].page_content)

Outputs
-------

- **Parsed Data**: The text is saved to a Markdown file named ``psychology_data.md``.
- **Vector Database**: The embeddings are stored in a Chroma database at ``Psycho_db``.
- **Search Results**: Queries retrieve the most relevant document chunks from the database.

Notes
-----

- Ensure the input PDF is in the same directory as the script.
- Customize the ``chunk_size`` and ``chunk_overlap`` parameters to suit your needs.
- Use the correct model version for embeddings (e.g., ``mxbai-embed-large:latest``).

