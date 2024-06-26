import streamlit as st
import replicate
import os

# App title
#cle = "r8_04XQqrT49S7nAYgtUUnGTmS1qlCUFnd3EOn0Q"
#st.set_page_config(page_title="💬 Parle avec Dr Evilafo")
st.set_page_config(page_title="IA Santé CI",
    layout="wide",  # Options: "centered" or "wide"
    initial_sidebar_state="collapsed"  # This hides the sidebar by default
)
st.header("💬 Parle avec Dr Evilafo")

# Replicate Credentials
with st.sidebar:
    st.title('💬 Parle avec Dr Evilafo ')
    st.write('Votre medecin virtuel.')
    #st.write('API key : r8_04XQqrT49S7nAYgtUUnGTmS1qlCUFnd3EOn0Q')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input("r8_04XQqrT49S7nAYgtUUnGTmS1qlCUFnd3EOn0Q", type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Saisir les identifiants!', icon='⚠️')
        else:
            st.success('Passer à la saisie du message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    ###
    #replicate_api = st.text_input('Token de l API:',"r8_04XQqrT49S7nAYgtUUnGTmS1qlCUFnd3EOn0Q", type='password')
    #replicate_api = "r8_04XQqrT49S7nAYgtUUnGTmS1qlCUFnd3EOn0Q"
    #os.environ['REPLICATE_API_TOKEN'] = replicate_api
    ###
    

    st.subheader('Modèles et paramètres')
    selected_model = st.sidebar.selectbox('Le modèle a Llama2', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)
    #st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour, je suis Dr Evilafo. \n\n Pouvez-vous me dire ce qui vous amène aujourd'hui ? Quels sont vos symptômes ou vos préoccupations ?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour, je suis Dr Evilafo. Pouvez-vous me dire ce qui vous amène aujourd'hui ? Quels sont vos symptômes ou vos préoccupations ?"}]
st.sidebar.button('Supprimer l historique', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "Exprime toi en français durant tout l'échange. Nous somme dans le cadre d'une application de santé, et tu joue le rôle d'un medecin. Ton nom est Dr Evilafo. Les utilisateurs se connectent pour des consultations et si possible des diagnostiques et prescription de médicament ou de conseil. Si on essaye de changer de sujet ou de parler d'autre chose, ne donne pas la reponse et rappelle que tu ne repond qu'aux questions medicales. Si les choses sont au delà de tes capacités, précise que je vas me recommander aux médécin Dr Valet. Evite de te presenter à chaque reponse. "
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
#if prompt := st.chat_input(disabled=not replicate_api):
if prompt := st.chat_input(placeholder="Entrez votre préocupation ici...", disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Je reflechi..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .stActionButton {visibility: hidden;}
            .viewerBadge_link__qRIco {visibility: hidden;}
            .viewerBadge_container__r5tak {visibility: hidden;}
            .styles_viewerBadge__CvC9N {visibility: hidden;}
            .viewerBadge_container__r5tak {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
