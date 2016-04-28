from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import models as auth_models
from django.db.models import Avg

class Product(models.Model): 
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=False)    

    minimum_age_appropriate = models.IntegerField(default=0, blank=False)
    maximum_age_appropriate = models.IntegerField(default=-1, blank=False)
    image = models.ImageField(blank=True)


    def __str__(self):
        return "{} ${}".format(self.name, self.price)

    def age_range(self):
    	if self.maximum_age_appropriate == -1:
    		return "Age {} up.".format(self.minimum_age_appropriate)
    	else:
    		if self.maximum_age_appropriate == self.maximum_age_appropriate:
    			return "Age {}.".format(self.minimum_age_appropriate)
    		return "Age {} to {}.".format(self.minimum_age_appropriate, self.maximum_age_appropriate)

    def ratings(self):
        
        return self.review_set.all().aggregate(Avg('stars'))['stars__avg']


class Review(models.Model):
    stars = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    review_text = models.TextField()
    product = models.ForeignKey(Product)
    user = models.ForeignKey(auth_models.User)

    def __str__(self):
        return "({} star{}) {}".format(self.stars, ('s' if self.stars > 1 else ''), self.review_text)