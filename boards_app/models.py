from django.db import models

class Board(models.Model): 
    name = models.CharField(max_length=255)
    
    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise ValueError("The default board cannot be deleted.")
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    
class BoardList(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    
    def __str__(self):
        return f"{self.name} ({self.board.name})"
    
