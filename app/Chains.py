import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


load_dotenv()

os.getenv("grok_api_key")

class chain: 
    def __init__(self):
        self.llm =  ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7, groq_api_key = os.getenv("grok_api_key"))
    
    def extract_job(self , cleaned_text):
        prompt_extract  = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE :
            {page_data}
            ### INSTRUCTIONS : 
            The scraped text is from the carrer's page of a website. 
            your job is to extract the job postings and return them in JSON format containign the following keys:
            `role`,`experience`,`skills` and `description`
            only return the valid JSON.
            ### VALID JSON(NO PROBLEM)
            """)
        
        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={'page_data':cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_reponse = json_parser.parse(response.content)
        
        except OutputParserException:
            raise OutputParserException("Context to big , unable to parse the job !")
    
        return json_reponse if isinstance(json_reponse , list) else [json_reponse]
    
    
    
    def write_email(self , job , link_list):
        prompt_email = PromptTemplate.from_template("""
            ### JOB DISCRIPTION :
            {Job_description}

            ### INSTRUCTION:
            You are Ayush Kore, a passionate Full-Stack Data Scientist specializing in Generative AI, 
            eager to make an impact. You may not have professional experience yet, but you have strong 
            knowledge of AI, machine learning, data pipelines, and full-stack development.
             
            Your task is to write a personalized cold email to the hiring team for the job described above. 
            The email should: Ayush's portfolio: {link_list}
            Remember you are ayush,passionate Full-Stack Data Scientist . 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """)
        
        chain_email = prompt_email |self.llm
        res = chain_email.invoke({"Job_description":str(job) , "link_list":link_list} )
        return  res.content
