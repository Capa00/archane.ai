from cat.mad_hatter.decorators import tool, plugin
from pydantic import BaseModel

class InstagramCommentsSettings(BaseModel):
    api_key: str

@tool
def answer_comment(comment, cat):
    """Reply to the comment. Input is the comment"""
    return "Dioporco"

@plugin
def settings_model():
    return InstagramCommentsSettings