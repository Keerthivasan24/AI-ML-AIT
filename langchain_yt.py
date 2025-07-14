#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install langchain-openai langchain-community


# In[2]:


openai_api_key="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"


# In[4]:


from langchain_openai import ChatOpenAI
llm = ChatOpenAI(openai_api_key=openai_api_key)


# In[5]:


response = llm.invoke("Suggest me a best Animated Movie in Tamil")
response


# In[6]:


from langchain_core.messages import HumanMessage,SystemMessage

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi")
    
]
llm.invoke(messages)


# In[7]:


from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)


# In[11]:


prompt = prompt_template.invoke({"language": "hindi", "text": "hi "})

prompt


# In[12]:


from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

prompt = prompt_template.invoke({"topic": "cats"})

response = llm.invoke(prompt)

response.content


# In[13]:


movie_title_template = PromptTemplate.from_template("Suggest me title of a movie to watch in language {language} and of genre {genre}")

movie_title_prompt = movie_title_template.invoke({"language": "hindi", "genre":"comedy"})

response = llm.invoke(movie_title_prompt)

response.content


# In[14]:


from langchain_core.output_parsers import StrOutputParser

movie_title_chain = movie_title_template | llm | StrOutputParser()

movie_title_chain.invoke({"language": "english", "genre":"horror"})


# In[15]:


movie_summary_prompt = PromptTemplate.from_template("Give me 2-3 line summary of the movie {movie_title}") 


# In[16]:


from langchain_core.runnables import RunnableLambda

print_title_step = RunnableLambda(lambda x : print(x["movie_title"]))

composed_chain = {"movie_title": movie_title_chain} | print_title_step | movie_summary_prompt | llm | StrOutputParser()


# In[17]:


from langchain_core.runnables import RunnableSequence

composed_chain = RunnableSequence({"movie_title": movie_title_chain}, print_title_step, movie_summary_prompt, llm, StrOutputParser())


# In[18]:


from langchain_core.runnables import RunnableParallel

translate_hindi_chain = ChatPromptTemplate.from_template("Translate the summary {summary} to hindi") | llm | StrOutputParser()
tranlate_spanish_chain = ChatPromptTemplate.from_template("Translate the summary {summary} to spanish") | llm | StrOutputParser()

translate_runnable = RunnableParallel(hindi_translate = translate_hindi_chain, spanish_translate = tranlate_spanish_chain)

translated_summary = translate_runnable.invoke({"summary" : summary})

print("Hindi Summary: ",  translated_summary["hindi_translate"])
print("Spanish Summary: ", translated_summary["spanish_translate"])


# In[ ]:




