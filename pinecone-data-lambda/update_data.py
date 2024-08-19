import os
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain.schema import Document
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main(event, context):
    load_dotenv(override=True)

    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Load environment variables
    index_name = os.getenv("PINECONE_INDEX_NAME")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    scope = ['https://www.googleapis.com/auth/documents.readonly']

    # Authenticate Google Docs API
    credentials = service_account.Credentials.from_service_account_file(
        filename='credentials.json', 
        scopes=scope
    )
    service = build('docs', 'v1', credentials=credentials)

    # Fetch the document from Google Docs
    document_id = '1YfimQqX74jEjHCZPIXWHy8hv6TZ9Yh_k4EhMs27nCr0'
    document = service.documents().get(documentId=document_id).execute()

    # Extract text from the document
    doc_content = document.get('body').get('content')
    text = ''
    for element in doc_content:
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                text += text_run.get('textRun', {}).get('content', '')

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    documents = text_splitter.split_text(text)
    documents = [
        Document(page_content=chunk, metadata={"source": f"https://docs.google.com/document/d/{document_id}/edit"})
        for chunk in documents
    ]

    # Initialize Pinecone
    pinecone = Pinecone(api_key=pinecone_api_key)
    index = pinecone.Index(index_name)

    # Query the Pinecone index
    query = index.query(
        vector=[0.1]*1536,  # Replace with actual vector for meaningful queries
        filter={"source": f"https://docs.google.com/document/d/{document_id}/edit"},
        top_k=10
    )

    # Delete existing entries related to this document
    matches = query.matches
    for doc in matches:
        print(f"Deleting document ID: {doc.id}")
        index.delete(doc.id)

    # Store the new documents in Pinecone
    pinecone_vector_store = PineconeVectorStore.from_documents(
        documents, embeddings, index_name=index_name
    )
    print(documents)

    return {"message": "Data updated successfully!"}

main(None, None)
