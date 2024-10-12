class User:
    def __init__(self, email, name, password, job_title):
        self.email = email
        self.name = name
        self.password = password
        self.job_title = job_title
        self.posts = []  # Each user will have an array of posts

    def get_user_info(self):
        print(f"User {self.name} is a {self.job_title}. Email: {self.email}")

    def add_post(self, post):
        self.posts.append(post)

    def get_all_posts(self):
        for post in self.posts:
            post.get_post_info()