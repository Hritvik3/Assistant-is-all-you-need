import os
import tempfile
import sys
import streamlit as st
from ingest import main as ingest_main
from inGPT import main as inGPT_main
from colors import set_colors


def clean_temp_files():
    # Clean up temporary files from previous runs
    temp_dir = tempfile.gettempdir()
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning temporary file: {e}")


st.button("Clear cache",on_click = clean_temp_files())

def main():

    # Clean up temporary files from previous runs
    clean_temp_files()
    #Title
    st.title('Assistant is all you need 🤖')

    #Welcoming message
    st.write("""Hello, 👋 I am your AI Assistant and here to help you unleash the power of exploration! 
              Upload files, delve deep, and ask insightful questions tailored to your project's needs""")
     # Set colors
    set_colors()

        
    # #Explanation sidebar
    # with st.sidebar:
    #     st.write('*Your Data Assistant is here to help you.*')
    #     st.caption('''**You may already know that every exciting data science journey starts with a dataset.
    #     That's why I'd love for you to upload a CSV file.
    #     Once we have your data in hand, we'll dive into understanding it and have some fun exploring it.
    #     Then, we'll work together to shape your business challenge into a data science framework.
    #     I'll introduce you to the coolest machine learning models, and we'll use them to tackle your problem. Sounds fun right?**
    #     ''')

    #     st.divider()

        
   
       # CSS styling for fixed position buttons and reload button
    st.markdown(
        """
        <style>
        .fixed-buttons {
            position: fixed;
            bottom: 10px;
            left: 10px;
            z-index: 9999;
        }
        .reload-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease;
        }
        .reload-button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


  


    #     # Reload button (fixed position)
    # reload_button_html = '<button class="fixed-buttons" onclick="window.location.reload();">Reload App</button>'
    # st.markdown(reload_button_html, unsafe_allow_html=True)




    # File upload section
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "html", "md"])

    if uploaded_file is not None:
        # Create a temporary directory to store the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Process the uploaded file
            if st.button("Process File"):
                # Set environment variables
                os.environ['SOURCE_DIRECTORY'] = temp_dir
                os.environ['PERSIST_DIRECTORY'] = temp_dir

                # Run the main function from ingest.py
                ingest_main([file_path])

                st.success(f"File processing completed.")

    # Initialize conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []


    # Query section
    query = st.text_input("Enter your query:", key="query_input", help='Press Enter to submit')
    # print(query)



    if query:
        os.environ['MODEL'] = 'mistral'
        os.environ['EMBEDDINGS_MODEL_NAME'] = 'all-MiniLM-L6-v2'
        os.environ['TARGET_SOURCE_CHUNKS'] = '4'
        
        # Call the main function from inGPT.py
        answer, source_documents = inGPT_main(query, hide_source=False, mute_stream=False)

        # Add the query and answer to the conversation history
        st.session_state.conversation.append({"query": query, "answer": answer, "source_documents": source_documents})

        # query = ""

        #Clear the input text box
        # query = None

    # Toggle button for showing/hiding source documents
    # show_source = st.checkbox("Show Source Documents", key="show_source_checkbox", class_="fixed-buttons")

        # Toggle button for showing/hiding source documents
    show_source = st.checkbox("Show Source Documents", key="show_source_checkbox")
    # Reload button
    if st.button("Reload App", key="reload_button"):
        # Reload the app
        st.experimental_rerun()


    # Display the conversation history
    for message in st.session_state.conversation:
        st.write(f"**Query:** {message['query']}")
        st.write(f"**Answer:** {message['answer']}")
        if show_source and message['source_documents']:
            st.write("**Source Documents:**")
            st.write(message['source_documents'])
        st.write("---")

    st.caption("<p style ='text-align:center'> made with ❤️ by Hritvik</p>",unsafe_allow_html=True )

    st.markdown(
        """
        <style>
        .stTextInput {
            position: fixed;
            bottom: 10%;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 50px; /* Adjust the height as needed */
            padding: 10px;
            border-top: 1px solid #ccc;
            # background-color:#FFFFFF; 
            z-index: 9999;
        }
        # .stButton {
        #     position: fixed;
        #     bottom: 10px;
        #     left: 50%;
        #     transform: translateX(-50%);
        #     z-index: 9999;
        # }
        </style>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()