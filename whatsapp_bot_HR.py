import os
import logging
from PyPDF2 import PdfReader
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from pymongo import MongoClient

# Initialize logging and load environment variables
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGODB_URI')
mongo_db_name = os.getenv('MONGODB_DB_NAME')
client = MongoClient(mongo_uri)
db = client[mongo_db_name]
products_collection = db['defaultCollection']

# OpenAI API and PDF path setup
openai.api_key = os.getenv('OPENAI_API_KEY')
# pdf_path = os.getenv('PDF_PATH')

def get_pdf_text(pdf_path):
    try:
        pdf_reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        return ""

# Pre-load PDF content to avoid reading the PDF file on each request
pdf_text = get_pdf_text('C:/Users/lenovo/whatsapp_bot_project/TechMaster_Company_Policies_FAQ.pdf')
logger.info(f"PDF text loaded: {len(pdf_text)} characters")



def search_pdf_for_query(query):
    lower_query = query.lower()
    if lower_query in pdf_text.lower():
        start_index = pdf_text.lower().find(lower_query)
        # Find the end of the sentence for better context
        end_index = pdf_text.find('.', start_index) + 1
        if end_index == 0:  # No end of sentence found
            end_index = start_index + len(query) + 200  # Fallback to fixed length
        context = pdf_text[start_index:end_index].replace('\n', ' ')  # Extract context
        return context
    else:
        # Query not found, consider logging this for review or using OpenAI as fallback
        return "I couldn't find an answer in the document. Could you please ask something else or rephrase your question?"

    
def query_products_set(set_number, per_set=3):
    logger.info("Querying products from MongoDB.")
    try:
        skip = (set_number - 1) * per_set
        cursor = products_collection.find({}).skip(skip).limit(per_set)
        products_details = [f"Name: {product.get('product_name', 'N/A')}, Price: {product.get('product_price', 'N/A')}" for product in cursor]

        if not products_details:
            return "No more products found."
        
        response_text = "\n".join(products_details)
        # Assuming you want to guide the user to the next set of products
        total_products = products_collection.count_documents({})
        if skip + per_set < total_products:
            next_set = set_number + 1
            response_text += f"\n\nPress {next_set} for the next list of products."
        else:
            response_text += "\n\nNo more products to display."
        return response_text
    except Exception as e:
        logger.error(f"Failed to query product details from MongoDB: {e}")
        return "Failed to fetch product details."


@app.route("/whatsapp", methods=["POST"])
def wa_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    logger.info(f"Received message: {incoming_msg}")

    if "how many models are present" in incoming_msg:
        total_products = products_collection.count_documents({})
        response_text = f"There are {total_products} models present.\n\nPress 1 for the list of first 3 products."
    elif incoming_msg.isdigit():
        set_number = int(incoming_msg)
        response_text = query_products_set(set_number)
    else:
        # Search for a query in the PDF content
        pdf_search_result = search_pdf_for_query(incoming_msg)
        if pdf_search_result.startswith("I couldn't find an answer"):
            # If not found in PDF, consider other query handling or fallback to OpenAI directly
            response_text = query_openai(incoming_msg)
        else:
            # If found in PDF, construct a prompt for OpenAI using the PDF context
            prompt = f"As an HR person, how would you explain this to an employee? \"{pdf_search_result}\""
            response_text = query_openai(prompt)

    resp = MessagingResponse()
    msg = resp.message(response_text)
    return str(resp)

def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "system", "content": "You are an HR professional responding to employee queries based on company policies."}, 
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"An error occurred during the OpenAI API call: {e}")
        return "I encountered an error while trying to find an answer for you."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
