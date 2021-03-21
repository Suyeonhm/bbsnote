from django.db import models

class Board(models.Model): #게시글모델
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject
 
class Comment(models.Model): #댓글모델
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
