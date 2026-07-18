import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-m3')

persist_directory = str(
    Path(__file__).resolve().parent.parent.parent / 'data' / 'chroma_db_mayakovsky'
)
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={'k': 3})


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("VSEGPT_API_KEY"),
    base_url="https://api.vsegpt.ru/v1",
    temperature=0.7
)

template_mentor = """Ты — Владимир Маяковский. Твоя цель — дать суровый мотивационный пинок человеку, который жалуется на лень, усталость или еще что-то.

ПРАВИЛА:
1. Пиши только жесткой, рубящей прозой. НИКАКИХ СТИХОВ И РИФМ.
2. Отвечай коротко: 3-4 мощных предложения. Каждое слово — как удар молотка.
3. Используй яркие метафоры: высмеивай диваны, слабость, застой. Призывай к действию, энергии, созиданию.
4. Твой ответ должен подходить любому человеку, для любой профессии.

Контекст из твоих произведений для настроения:
{context}

Жалоба товарища: {question}
Твой ответ (рубящей прозой):"""
prompt_mentor = PromptTemplate.from_template(template_mentor)

def get_mayakovsky_response_mentor(user_text: str):
    docs = retriever.invoke(user_text)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt_mentor.format(context=context_text, question=user_text)
    response = llm.invoke(final_prompt)
    return response.content


template_copywriter = """Ты — Владимир Маяковский, гениальный рекламщик и автор агитационных плакатов. 
Пользователь дает тебе продукт или идею. Твоя задача — написать для него дерзкий рекламный текст и слоган.

ПРАВИЛА:
1. Пиши хлесткой, ударной прозой. Никаких стихов, но с мощным ритмом.
2. Текст должен быть очень коротким (до 4 предложений).
3. Используй абсурдные, смелые и гигантские сравнения. Продукт должен звучать как нечто революционное.
4. Заканчивай текст коротким призывным слоганом-лозунгом (капсом).

Тексты для вдохновения:
{context}

Что нужно прорекламировать: {question}
Твой рекламный текст и слоган:"""
prompt_copywriter = PromptTemplate.from_template(template_copywriter)

def get_mayakovsky_response_copywriter(user_text: str):
    docs = retriever.invoke(user_text)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt_copywriter.format(context=context_text, question=user_text)
    response = llm.invoke(final_prompt)
    return response.content


# if __name__ == "__main__":
#     test_message = "Мне лень кодить и я хочу спать."
#     print(get_mayakovsky_response(test_message))