from project.utils.x_api import x_client


class CommentModule:
    def __call__(self, *args, **kwargs):
        comments = x_client
        # ce ne sono nuovi?
        # se ce ne sono nuovi chiama il gatto e rispondi a caso
