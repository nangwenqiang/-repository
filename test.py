from langchain_community.vectorstores import Zilliz
from langchain_community.embeddings import SparkLLMTextEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatSparkLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

connection_args = { 'uri': 'https://in05-d1907fdffdea754.serverless.ali-cn-hangzhou.cloud.zilliz.com.cn', 'token': '5980a9e42fd9390a8ff79fad78ab92b128ad8bb895ae355c3fcb5545ce7a44be02aeea6b0327de75b70e5f55ac32996eabd813ed' }
embeddings = SparkLLMTextEmbeddings(
    app_id='e4278af3',
    api_key='d928519667d11992a79ca93d1ffb2f2b',
    api_secret='YTEwOWEzZWVjOGYzMTUwODI1ZmZmN2Vh'
)

vector_store = Zilliz(
    embedding_function=embeddings, 
    connection_args=connection_args,
    collection_name='ifly_A',
    drop_old=False,
    vector_field='embedding',
    text_field='chunk_text'
)

model = ChatSparkLLM(
    spark_app_id='e4278af3',
    spark_api_key='d928519667d11992a79ca93d1ffb2f2b',
    spark_api_secret='YTEwOWEzZWVjOGYzMTUwODI1ZmZmN2Vh',
    spark_api_url='wss://spark-api.xf-yun.com/v3.1/chat',
    spark_llm_domain='generalv3'
)

# query = "招标投标活动雏形产生于清朝末期，但发展缓慢。中华人民共和国成立初期?"
# docs = vector_store.similarity_search(query)
retriever = vector_store.as_retriever()
# docs = retriever.invoke(query)
# print(docs[0].page_content)


template ="""根据接下来的文本回答问题并且详细的列出分别根据哪条回答了什么:
{context}

问题: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

answer = retrieval_chain.invoke("招标人透露潜在投标人的信息会导致什么后果？")
print(f'星火：{answer}')
# print('end_________')