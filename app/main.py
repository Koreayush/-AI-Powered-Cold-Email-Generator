import streamlit as st 
from langchain_community.document_loaders import WebBaseLoader

from Chains import chain
from Links import Portfolio
from clean_text import  cleaned_text


def create_app(llm, Portfolio, cleaned_text):
    st.title("📧 AI-Powered Cold Email Generator")
    st.caption(
        "Generate personalized cold emails directly from a company's career page using AI."
    )

    url_input = st.text_input(
        "🔗 Enter the job or career page URL",
        value="https://www.accenture.com/in-en/careers/jobdetails?id=ATCI-5310405-S1947221_en&title=Database+Administrator",
        help="Paste a public job posting or career page URL"
    )

    submit_button = st.button("🚀 Generate Cold Email")
    
    if submit_button:
        try :
            loader = WebBaseLoader([url_input])
            data = cleaned_text(loader.load().pop().page_content)
            Portfolio.load_portfolio()
            jobs = llm.extract_job(data)
            
            for job in jobs :
                skills  = job.get('skills',[])
                links = Portfolio.query_links(skills)
                email = llm.write_email(job,links)
                
                st.code(email , language='markdown')
                
        except Exception as e :
            st.error(f"An error Occured : {e}")
            

if __name__ == "__main__":

    Chains =    chain()
    Links = Portfolio()
    st.set_page_config(layout="wide" , page_title="Cold Email Generator",page_icon="📧")
    create_app(Chains , Links, cleaned_text)
