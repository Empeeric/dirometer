from django.db import models

####################Defines extended user class###################
class RentReport(models.Model):
    city = models.CharField( max_length = 20, blank = False, null = False )
    street = models.CharField( max_length = 20, blank = False, null = False )
    address = models.CharField( max_length = 5, blank = False, null = False )
    apartment = models.CharField( max_length = 5, blank = False, null = False,default=0 )
    old_price = models.IntegerField( blank = False, null = True )
    new_price = models.IntegerField( blank = False, null = True )
    price_up = models.BooleanField( blank = False, null = False )
    num_of_rooms=models.IntegerField(default=0)
    lng = models.FloatField( null = True )
    lat = models.FloatField( null = True )

class SingleRank(models.Model):
    is_boolean=models.BooleanField(default=False)
    owner_report = models.ForeignKey('MobileFullReport')
    rid = models.IntegerField(default=0)
    ranks_sum = models.IntegerField(default=0)
    num_of_ranks = models.IntegerField(default=0)

    def addRanking(self,rank):
        self.num_of_ranks += 1
        self.ranks_sum += rank

    def getRank(self):
        if self.is_boolean:
            if self.ranks_sum >= self.num_of_ranks/2 :
                return  1
            else:
                return 0
        else:
            return self.ranks_sum / self.num_of_ranks

class MobileFullReport(models.Model):
    address = models.CharField(max_length=100,blank=False,null=False)
    number = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    real_loc = models.BooleanField(default=True)

    def getSimpleObject(self):
        ranks=[ (i.rid, i.getRank() ) for i in list(SingleRank.objects.filter(owner_report=self) ) ]
        self.ranks=ranks
        return self

        










