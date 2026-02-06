import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file; to then be superseded by the below

IIIF_CS_API_HOST = os.environ.get('IIIF_CS_API_HOST')
IIIF_CS_PRESENTATION_HOST = os.environ.get('IIIF_CS_PRESENTATION_HOST')
IIIF_CS_CUSTOMER_ID = os.environ.get('IIIF_CS_CUSTOMER_ID')
IIIF_CS_BASIC_CREDENTIALS = os.environ.get('IIIF_CS_BASIC_CREDENTIALS')