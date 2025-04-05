# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from boards_app.models import Board, BoardList


# @receiver(post_save, sender=Board)
# def create_empty_board_list(sender, instance, created, **kwargs):
#     if created:  
#         BoardList.objects.create(name='In-box', board=instance)  


from django.dispatch import receiver
from django.db.models.signals import post_save
from boards_app.models import Board, BoardList


@receiver(post_save, sender=Board)
def create_empty_board_list(sender, instance, created, **kwargs):
    pass