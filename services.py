from models import PostsModel


class PostsService:
    def __init__(self):
        self.model = PostsModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, post_id, params):
        return self.model.update(post_id, params)

    def delete(self, post_id):
        return self.model.delete(post_id)

    def list(self):
        response = self.model.list_items()
        return response