# MuhammadHussain07-WhatsApp-HR-Chatbot-with-PDF-Search-Integration

Certainly! Here's the updated documentation tailored for an HR (Human Resources) audience:

---

# WhatsApp HR Chatbot with PDF Search Integration

## Overview
This Python script implements a WhatsApp chatbot tailored for HR professionals using the Flask framework and integrates it with Tenable.sc for asset list management. The chatbot enables HR personnel to respond to employee queries based on company policies and provides seamless access to product details. Leveraging natural language processing and PDF search capabilities, the chatbot enhances HR efficiency and responsiveness.

## Features
- **WhatsApp Integration**: The chatbot listens for incoming messages from a WhatsApp number using the Twilio API and responds with relevant information.
- **PDF Search**: HR professionals can search for information within a PDF document containing company policies and procedures, enabling quick access to relevant content.
- **MongoDB Integration**: Product details are stored in a MongoDB database, allowing HR personnel to retrieve and communicate product information to employees seamlessly.
- **OpenAI Integration**: For queries not found in the PDF document, the chatbot utilizes the OpenAI API to generate responses tailored to employee inquiries.

## Requirements
- Python 3.x
- Flask
- PyPDF2
- Twilio
- Python Dotenv
- TenableSC Python SDK
- PyMongo
- OpenAI Python Client

## Setup
1. Install the required Python packages using pip:
   ```
   pip install Flask PyPDF2 twilio python-dotenv pymongo openai
   ```

2. Set up a Twilio account and obtain the necessary credentials for WhatsApp integration.

3. Configure environment variables in a `.env` file with the following keys:
   ```
   MONGODB_URI=<MongoDB_URI>
   MONGODB_DB_NAME=<MongoDB_DB_Name>
   OPENAI_API_KEY=<OpenAI_API_Key>
   ```

4. Place the PDF document containing company policies in the specified path (currently commented out in the script).

5. Run the script using the command:
   ```
   python script_name.py
   ```

## Usage
1. HR professionals receive messages from employees on the WhatsApp number associated with the Twilio integration.
2. Respond to employee queries related to company policies, procedures, or product details.
3. The chatbot utilizes PDF search capabilities and external APIs to provide timely and accurate responses to employee inquiries.

## GitHub Repository
The source code for this script can be found on GitHub at: [GitHub Repository Link](https://github.com/your-username/your-repository)

---

Feel free to customize this documentation further to suit your HR audience's needs and expectations!


!<img width="636" alt="Screenshot 2024-03-17 114621" src="https://github.com/MuhammadHussain07/MuhammadHussain07-WhatsApp-HR-Chatbot-with-PDF-Search-Integration/assets/129845318/8bc536fc-2400-42eb-8c78-7b3f2aeb24ad">
