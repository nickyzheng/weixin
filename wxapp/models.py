from django.db import models

# Create your models here.
class clothes(models.Model):
	name = models.CharField(max_length = 30, blank = True)
	CATEGORY_LIST = (
		('1', 'business'),
		('2', 'business casual'),
		('3', 'casual'),
		('4', 'sport'),
		)
	category = models.CharField(max_length = 2, choices = CATEGORY_LIST, blank = True)
	SEASON_LIST = (
        ('1', 'spring and autumn'),
        ('2', 'summer'),
        ('3', 'winter'),
    	)
	season = models.CharField(max_length = 1, choices = SEASON_LIST, blank = True)
	tag = models.CharField(max_length = 200, blank = True)
	choose_count = models.SmallIntegerField(default = 0) # times the clothes has been choosed
	add_date = models.DateField(auto_now_add = True, blank = True)
	image_filename = models.CharField(max_length = 20, blank = True)

	def __unicode__(self):
		return self.name