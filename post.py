class Post:
    def __init__(self, content, author):
        self.content = content
        self.author = author

    def get_post_info(self):
        print(f"Post: '{self.content}' by {self.author}")