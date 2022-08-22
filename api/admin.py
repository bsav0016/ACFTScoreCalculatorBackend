from django.contrib import admin
from .models import ACFTResult, User, PaymentSheet

admin.site.register(ACFTResult)
admin.site.register(User)
admin.site.register(PaymentSheet)
