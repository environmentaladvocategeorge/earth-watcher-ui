from pydantic import BaseModel
from typing import Optional, Union
from models.teller import TellerAccount, TellerAccountBalance
from models.account import AccountLink

class AccountCreateRequest(BaseModel):
    provider: str
    provider_id: str
    entity_data: dict[str, str]
    metadata: Optional[dict] = {}

class AccountCreateResponse(BaseModel):
    account: AccountLink

class CategorizedAccounts(BaseModel):
    accounts: list[dict[str, Union[TellerAccount, TellerAccountBalance]]] = []
    total_ledger: float = 0.0
    total_available: float = 0.0

class AccountGetResponse(BaseModel):
    debit: CategorizedAccounts
    credit: CategorizedAccounts