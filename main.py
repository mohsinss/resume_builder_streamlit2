import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



template = """
    Below is news text that may be negative or depressing.
    Your goal is to:
    - Properly format the news
    - Convert the input text to a more positive and optimastic text (400 words Minimum) based on a specified tone:
    
     Here are some examples of words in different dialects:
    - Optimistic: Hopeful, Positive, Confident, Cheerful, Bright, Upbeat, Promising,Encouraging, Reassuring, Favorable Assured bright buoyant cheerful cheering confident encouraged expectant happy high hopeful hoping idealistic keeping the faith merry on cloud nine on top of world positive promising ray of sunshine rose-colored rosy sanguine sunny trusting utopian
    - Positive: Admiring, Affectionate, Appreciative, AppCalm, Celebratory, Cheerful, Compassionate, Confident, Ecstatic , Empathetic, Encouraging, Hilarious, Hopeful, Humorous, Interested, Joyful, Laudatory, Light, Lively, Modest, Nostalgic, Optimistic, Passionate, Placid, Playful amazing, straight, quickest, unbroken, nonstop, uninterrupted, to the point, no emotions, straight through
    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen
    - Texan: Yee-haw!, ah'ite,bald, Big'o, Caw, Fixin', Gimme, Gonna, In'thang, Jeetjet, Kicker, Libel'ta

    Please start the news with a warm introduction. Add the introduction if you need to.
    
    Below is the news text, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    News: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM():
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7)
    return llm

llm = load_LLM()

st.set_page_config(page_title="Positive News", page_icon=":robot:")
st.header("Positive News")

col1, col2 = st.columns(2)

with col1:
    st.markdown("often we receive news that are negative and depressing. \n\n This tool \
                will help reword the content to make it more optimistic and positive. \
                is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
               [@Mohsinbazea](https://twitter.com/MohsinBazea)")

with col2:
    st.image(image='TweetScreenshot.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter The News To Convert")



col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like the news to have?',
        ('Positive','Optimistic'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British', 'Texan'))

def get_text():
    input_text = st.text_area(label="News Input", label_visibility='collapsed', placeholder="Your News...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter Text. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "there is a strong argument for artificial intelligence negatively impacting unemployment rates within retail industry in numerous ways. For instance, self-service checkouts are extremely popular in stores, particularly supermarkets, so there is less of a requirement for cashiers. Also, AI can sort out the troublesome task of arranging a good online shopping experience for a businesses customers with product tagging, similar product recommendations etc. Beforehand, you would’ve found employees manually assigning product attributes but now there are image recognition models which have been trained to do all of that super efficiently."

st.button("*See An Example*", type='secondary', help="Click to see an example of the News you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted News:")

if email_input:
    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
    