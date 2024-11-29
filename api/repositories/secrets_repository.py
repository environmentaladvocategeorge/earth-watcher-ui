import boto3
import logging
from botocore.exceptions import ClientError
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class SecretsRepository:
    def __init__(self, region_name: str):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, secret_name: str) -> str:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret = response.get('SecretString')
            if not secret:
                raise HTTPException(status_code=500, detail=f"Secret {secret_name} is empty")
            return secret
        except ClientError as e:
            logger.error(f"Error retrieving secret {secret_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving secret {secret_name}")
        except Exception as e:
            logger.error(f"Unexpected error retrieving {secret_name}: {e}")
            raise HTTPException(status_code=500, detail="Unexpected error retrieving secrets")