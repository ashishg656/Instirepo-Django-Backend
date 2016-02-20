from django.contrib import admin
from ecommerce.models import *

admin.site.register(Product)
admin.site.register(ProductCategories)
admin.site.register(Orders)
admin.site.register(ProductComments)
admin.site.register(ProductFavourites)
admin.site.register(ProductViews)
admin.site.register(RecentlyViewedProducts)

# admin.site.register(Posts)
# admin.site.register(PollChoices)
