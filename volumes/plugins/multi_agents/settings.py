from cat.mad_hatter.decorators import tool, plugin, hook
from pydantic import BaseModel

class InstagramCommentsSettings(BaseModel):
    api_key: str

@tool(return_direct=True)
def handle_comment(comment, cat):
    """Risponde ad un commento fornito come input sempre con 'tua zia pelata'."""
    return "tua zia pelata"

# @hook
# def agent_prompt_suffix(suffix, cat):
#     suffix += "\nRispondi in modo malinconico"
#     return suffix

@plugin
def settings_model():
    return InstagramCommentsSettings