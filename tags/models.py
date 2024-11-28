from django.db import models

# Create your models here.


# class Tags(models.Model):
    
#     tag_label = models.CharField(max_length=255)


# class Tagged_Item:
    
#     #ContentType
#     tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
#     ##Identifiers
#     #field for id of the class
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content-type", "object_id")