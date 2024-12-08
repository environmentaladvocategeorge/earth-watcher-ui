import requests
from requests.auth import HTTPBasicAuth
from services.certificate_service import CertificateService
import logging

logger = logging.getLogger(__name__)

class TellerService:
    def __init__(self, certificate_service: CertificateService):
        self.certificate_service = certificate_service

    def get_accounts(self, access_token: str):
        cert_file_path, key_file_path = self.certificate_service.load_certificates()
        
        api_url = "https://api.teller.io/accounts"
        headers = {'Content-Type': 'application/json'}
        auth = HTTPBasicAuth(access_token, '')

        try:
            response = requests.get(api_url, headers=headers, auth=auth, cert=(cert_file_path, key_file_path))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Teller API request error: {e}")
            raise RuntimeError("Failed to call Teller API")
