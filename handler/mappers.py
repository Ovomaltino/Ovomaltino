from typing import List
from types.social_fact_type import SocialFactType


def to_social_fact(obj: dict) -> SocialFactType:

    filters: List[str] = ['createdAt', 'updatedAt', '__v']
    return {k: v for k, v in obj.items() if k not in filters}
