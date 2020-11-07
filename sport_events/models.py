from django.db import models
from django.urls import reverse
from users.models import CustomUser

# Create your models here.


class Sport(models.Model):
    sport_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.sport_name


class Event(models.Model):

    ELIGIBLE_CHOICES    = models.TextChoices('eligible_user_type', 'STUDENT TEACHER').choices
    STATUS_CHOICES      = models.TextChoices('status', 'ACTIVE CLOSED COMPLETED').choices

    name                = models.CharField(max_length=50)
    description         = models.TextField()
    sport               = models.ForeignKey(Sport, on_delete=models.SET('Deleted Sport'), related_name='events')
    fee                 = models.IntegerField(default=0)
    venue               = models.CharField(max_length=50)
    date_time           = models.DateTimeField(auto_now=False, auto_now_add=False)  # Use timeone instead
    reg_close_date      = models.DateField(auto_now=False, auto_now_add=False)
    eligible_user_type  = models.CharField(choices=ELIGIBLE_CHOICES, max_length=10)  

    status              = models.CharField(choices=STATUS_CHOICES, max_length=10)
    curr_round          = models.IntegerField(default=0)
    participants        = models.ManyToManyField(CustomUser,blank=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})    

    def complete(self):
        print(self.status)
        self.status = 'COMPLETED'
        print(self.name)
        print(self.status)



class Match(models.Model):

    event           = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='matches')
    participant_1   = models.ForeignKey(CustomUser, on_delete=models.SET('Deleted user'), related_name='participant_1')
    participant_2   = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET('Deleted user'), related_name='participant_2')
    round_no        = models.IntegerField()
    winner          = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET('Deleted user'), related_name='winner')

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        s = self.participant_1.username+" "
        if self.participant_2:
            s = s +  self.participant_2.username
        return s

    def get_absolute_url(self):
        return reverse("sport_events:event_detail", kwargs={"pk": self.event.pk})




'''
SELECT CONCAT('DROP TABLE ', TABLE_NAME, ';')
FROM INFORMATION_SCHEMA.tables
WHERE TABLE_SCHEMA = 'event_reg_db'

DROP TABLE auth_group;                        
DROP TABLE auth_group_permissions;            
DROP TABLE auth_permission;                   
DROP TABLE django_admin_log;                  
DROP TABLE django_content_type;               
DROP TABLE django_migrations;                 
DROP TABLE django_session;                    
DROP TABLE users_customuser;                  
DROP TABLE users_customuser_groups;           
DROP TABLE users_customuser_user_permissions; 
'''

