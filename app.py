import streamlit as st

from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaLLM

from scholarly import scholarly, ProxyGenerator

# ----- CONFIG PROXY -----

if "pg" not in st.session_state:
    SCRAPER_API_KEY = ""
    #st.session_state.pg = None
    st.session_state.pg = ProxyGenerator()
    st.session_state.pg.ScraperAPI(SCRAPER_API_KEY)
# end if

scholarly.use_proxy(st.session_state.pg)

# --- END CONFIG PROXY ---

# ----- CONFIG -----

DEBUG = True

def debug_print(arg):
    if DEBUG:
        print(arg)
    # end if
# end def


st.set_page_config(layout="wide")

if "description_submitted" not in st.session_state:
    st.session_state.description_submitted = False
# end if

if "Ollama_llm" not in st.session_state:
    st.session_state.Ollama_llm = OllamaLLM(model = "llama3.2", temperature = 0)
# end if

if "Ollama_llm_chat" not in st.session_state:
    st.session_state.Ollama_llm_chat = ChatOllama(model = "llama3.2", temperature = 0)
# end if

if "description_to_query_prompt_template" not in st.session_state:
    st.session_state.description_to_query_prompt_template = ChatPromptTemplate(
        [
            SystemMessage(content = "Transform the user description into one GoogleScholar search query. Use double stright quotes only for exact phrases. Output only the query string."),
            ("human", "{user_description}")
        ]
    )
# end if

if "description_abstract_comparison_prompt_template" not in st.session_state:

    template = """
    Score from 0 to 9 how well the abstract matches the description in content and key concepts.
    0 - no match at all
    2 - some keywords match but unrelated content
    5 - shares general topic but differs in specific focus or details
    7 - related content, minor differences like lack of some concepts or presence of different ones
    9 - perfect match

    Output only the integer score

    Description:
    {description}

    Abstract:
    {abstract}
    """

    st.session_state.description_abstract_comparison_prompt_template = PromptTemplate(template = template)
# end if

if "description_to_query_chain" not in st.session_state:
    st.session_state.description_to_query_chain = st.session_state.description_to_query_prompt_template | st.session_state.Ollama_llm_chat | StrOutputParser()
# end if

USER_STYLE = "background-color:#DCF8C6; color:#000000; padding:12px; border-radius:8px; margin-bottom: 12px"
ASSISTANT_STYLE = "background-color:#F1F0F0; color:#000000; padding:12px; border-radius:8px; margin-bottom: 12px"
LIST_STYLE = ["background-color:#F5F5F5; color:#000000; padding:12px; border-radius:8px; margin-bottom: 8px", "background-color:#E8E8E8; color:#000000; padding:12px; border-radius:8px; margin-bottom: 8px"]

MAX_QUERY_EXECUTIONS = 5
MAX_RESULTS = 3

ABSTRACT_MATCH_THRESHOLD = 7

# --- END CONFIG ---

if user_description := st.chat_input("Description of research paper"):
    st.session_state.user_description = user_description
    st.session_state.description_submitted = True
# end if

if st.session_state.description_submitted:

    debug_print(st.session_state.user_description)
    st.markdown(f'<div style="{USER_STYLE}">{st.session_state.user_description}</div>', unsafe_allow_html = True)

    scholar_search_query = st.session_state.description_to_query_chain.invoke({"user_description": st.session_state.user_description})

    debug_print(scholar_search_query)
    st.markdown(f'<div style="{ASSISTANT_STYLE}">{scholar_search_query}</div>', unsafe_allow_html = True)

    search_query = scholarly.search_pubs(scholar_search_query)

    results = 0

    for i in range(0, MAX_QUERY_EXECUTIONS):
        if results >= MAX_RESULTS:
            break
        # end if

        # fill
        pub = next(search_query)

        title = pub['bib']['title']
        authors = ", ".join(pub['bib']['author'])
        abstract = pub['bib']['abstract']
        url = pub['pub_url']

        debug_print(title)
        debug_print(abstract)

        score = st.session_state.Ollama_llm.invoke(st.session_state.description_abstract_comparison_prompt_template.format(description = st.session_state.user_description, abstract = abstract))

        try:
            score = int(StrOutputParser().parse(score))
        except ValueError:
            score = 0
        # end try

        print(score)

        if score >= ABSTRACT_MATCH_THRESHOLD:
            st.markdown(f"""
            <div style="{LIST_STYLE[results % 2]}">
            <h1><a href={url}>{title}</a></h1>
            <h4>Authors: {authors}</h4>
            <br>
            <p>{abstract}</p>
            <br>
            </div>
            """, unsafe_allow_html = True)

            results += 1
        # end if

    # end for

# end if

