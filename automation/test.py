# # Importing openAI 
# import openai
# import os
# import sys
# sys.path.append('./')
# import keys.ekeys as key

# from langchain.llms import OpenAI
# from langchain import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import SequentialChain

# import streamlit as st

# os.environ["OPENAI_API_KEY"] = key.openai_key

# # streamlit framework

# st.title('Article to generate')
# input_text = st.text_input('Type the title for Article to be generated:')

# # Prompt Templates

# first_input_prompt=PromptTemplate(
#     input_variables=['title'],
#     template="In not more than thousand words and Keeping in mind that the article is for indian audience Write an article on: {title}"
# )


# # Memory

# article_memory = ConversationBufferMemory(input_key='title', memory_key='articles_content')
# img_prompt_memory = ConversationBufferMemory(input_key='content', memory_key='articles_content')
# desc_memory = ConversationBufferMemory(input_key='img_prompt', memory_key='articles_content')

# # OpenAI LLMS
# llm = OpenAI(temperature=0.8)

# chain1 = LLMChain(
#     llm= llm,
#     prompt=first_input_prompt,
#     verbose=True,
#     output_key='content',
#     memory=article_memory
# )

# # Prompt for image generation
# second_input_prompt=PromptTemplate(
#     input_variables=['content'],
#     template="Based on this content describe me a fitting imagery which it evokes in not more than 100 words - {content}"
# )

# chain2 = LLMChain(
#     llm= llm,
#     prompt=second_input_prompt,
#     verbose=True,
#     output_key='img_prompt',
#     memory=img_prompt_memory
# )


# parent_chain = SequentialChain(
#     chains=[chain1,chain2],
#     input_variables=['title'],
#     output_variables=['content','img_prompt'],
#     verbose=True
# )

# if input_text:
#     st.write(parent_chain({'title':input_text}))

#     with st.expander('article_title'): 
#         st.info(article_memory.buffer)

#     with st.expander('article_title'): 
#         st.info(article_memory.buffer)

# # json file -> img_gen

