from ..abstract_module import Module
from ...utils.x_api import XClient


class Commenter(Module):
    def observe_environment(self, *args, **kwargs):
        posts = XClient().get_post()
        return posts

    def read_state(self, *args, **kwargs):
        pass

    def write_state(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass