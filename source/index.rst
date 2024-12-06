.. Mental-Health-Support documentation master file, created by
   sphinx-quickstart on Fri Nov 29 13:20:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mental-Health-Support documentation
===================================

This is a chatbot project, for mental health support.

It's goal is to make it **easier** for people to find someone they can **talk with**, spit what's in their heart without fearing anything. And most importantly, getting **advices** on what to do.

The amount of people getting depressed and mental illness keeps on increasing day by day. Therefore, it's a must to find a solution to help people get back on the right track!


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   Requirements
   Ollama
   RAG

====================
Building the chatbot
====================

In this section we will be covering how to make a simple chatbot application, and in further sections we will mention how to make it only get responses related to the health domaine from a specific database (RAG).

------------
Requirements
------------

To be able to run the applications, you must install the libraries used with this command :

``pip install requirements.txt
``

------
Ollama
------

in this project we will be using the **ollama** library.

^^^
Mac
^^^

`Download <https://ollama.com/download/Ollama-darwin.zip>`_ now.

^^^^^^^
Windows
^^^^^^^

`Download <https://ollama.com/download/OllamaSetup.exe>`_ now.


^^^^^
Linux
^^^^^


``curl -fsSL https://ollama.com/install.sh | sh
``

----------
QuickStart
----------

you can now easily get a LLM model locally and chat with it using ollama.

open a cmd and run the command:

``ollama run llama3.1
``

*llama3.1 is the model used in this project*

---
RAG
---

RAG stands for Retrieval-Augmented Generation, we will be using it so that the model can respond to the user's query from specific data (which either he didn't have before, or we're projecting the responses only on that data).

You can use this technique to avoid possible hallucinations if the subject is very specific.


^^^^^
Steps
^^^^^

**1- Ingesting the documents into a vector Database**

The ``rag.py`` is made for this task.

Using LLama_Parse, ``psychology_data.md`` is saved and used to extract the data.

The data is then splitted into chunks, Embedded using the Ollama_Embeddings function and stored in a Chroma vector Database.

**2- Loading the vector database and generating answers**

The ``chat_with_rag.py`` file contains this part.

The concept is to retrieve the answers from the database once the user is talking about some mental health concept or symptom.
