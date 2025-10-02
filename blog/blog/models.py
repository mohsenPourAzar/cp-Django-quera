# blog/models.py
from django.db import models, transaction

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def copy(self):

        new_post = BlogPost.objects.create(
            title=self.title,
            body=self.body,
            author=self.author,
        )
        
        # original_comments = self.comment_set.all().only("text")
        # Comment.objects.bulk_create(
        #     [Comment(blog_post=new_post, text=c.text) for c in original_comments]
        # )
        # Then dont use related_name in ForeignKey of Comment model
        
        original_comments = self.comments.all()
        for c in original_comments:
            Comment.objects.create(blog_post=new_post, text=c.text)

        return new_post.id


class Comment(models.Modelma):
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.CharField(max_length=500)

    def __str__(self):
        return f"Comment on {self.blog_post_id}"
