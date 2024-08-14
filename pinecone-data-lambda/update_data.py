import os
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_google_community import GoogleDriveLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone

def main(event, context):
    load_dotenv(override=True)

    embeddings = OpenAIEmbeddings()

    index_name = os.getenv("PINECONE_INDEX_NAME")

    loader = GoogleDriveLoader(document_ids=["1YfimQqX74jEjHCZPIXWHy8hv6TZ9Yh_k4EhMs27nCr0"],
                          credentials_path="credentials.json",
                          load_extended_matadata=True,
                          token_path=".credentials/token.json",
                          supportsAllDrives=True
                          )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
    documents = text_splitter.split_documents(docs)
    print(documents[0:3])

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    query = index.query(
        vector=[0.1]*1536,
        filter={"source": "https://docs.google.com/document/d/1YfimQqX74jEjHCZPIXWHy8hv6TZ9Yh_k4EhMs27nCr0/edit"},
        top_k=10
    )

    matches = query.matches
    for doc in matches:
        print(doc.id)
        index.delete(doc.id)


    pinecone = PineconeVectorStore.from_documents(
        documents, embeddings, index_name=index_name
    )
    return {"message": "Data updated successfully!"}

main(None, None)