# 🎬 Graph RAG Movie Question Answering System

A Neo4j-based movie question answering and recommendation system using a knowledge graph, Cypher queries, and Streamlit.

## 📌 Project Overview

This project uses a Neo4j knowledge graph to retrieve information about movies and actors. The application provides an interactive Streamlit interface for querying the movie graph and generating graph-based movie recommendations.

## ✨ Features

- 🎭 Find actors who acted in a movie
- 🎬 Find movies associated with an actor
- ⭐ Recommend movies based on common actors
- 🔗 Retrieve information from a Neo4j knowledge graph
- 🗃️ Execute Cypher queries for graph-based retrieval
- 🖥️ Interactive Streamlit web interface

## 🛠️ Technologies Used

- Python
- Neo4j
- Cypher
- Streamlit
- Neo4j Python Driver
- Knowledge Graph
- Graph RAG

## 🏗️ System Architecture

```text
User
  ↓
Streamlit Interface
  ↓
Python Application
  ↓
Cypher Queries
  ↓
Neo4j Knowledge Graph
  ↓
Movies / Actors / Recommendations
  ↓
Results displayed to User
