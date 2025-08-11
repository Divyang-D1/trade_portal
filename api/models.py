from django.contrib.auth.models import User
from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    scripcode = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_watchlist = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name_watchlist} ({self.user.username})"

    class Meta:
        unique_together = ('user', 'name_watchlist')

class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)

    class Meta:
        unique_together = ('watchlist', 'company')

    def __str__(self):
        return f"{self.company.company_name} in ({self.watchlist.name_watchlist})"