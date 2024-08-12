from pinecone import Pinecone
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai.chat_models import ChatOpenAI
import os
import json
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

def main(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid JSON format"
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    question = body.get("prompt", "No prompt provided")
    
    load_dotenv(override=True)
    print("debug0")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    parser = StrOutputParser()
    chain = model | parser
    print("debug0.5: " + question)

    embeddings = OpenAIEmbeddings()

    query_vector = embeddings.embed_query(question)
    print("debug0.6")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
    print("debug0.7")
    vector_store = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())
    print("debug1")

    pinecone_data = vector_store.max_marginal_relevance_search_by_vector(embedding=query_vector, k=2)
    # print(pinecone_data)

    context = "\n\n".join(doc.page_content for doc in pinecone_data)
    question = f"""
    Answer the question based on the context below. If you can't 
    answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    """
    print("debug2")

    output = chain.invoke(question)
    print(output)
    return {
        "statusCode": 200,
        "body": output
    }

# main({
#     "sup":"hi",
#     "body": "{\"prompt\":\"What countries are supported by thsi app?\"}"
# }, {})