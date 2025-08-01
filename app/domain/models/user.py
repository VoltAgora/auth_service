from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
  id: Optional[int]
  name: str
  lastname: str
  phone: str
  email: str
  hashed_password: str
  is_active: bool
  role: str
