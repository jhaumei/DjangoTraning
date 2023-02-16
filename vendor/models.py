from django.db import models
# added by me for VendorAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.
class Vendor(models.Model):
    vendor_name = models.CharField(max_length = 20)
    store_name = models.CharField(max_length = 10)
    phone_number = models.CharField(max_length = 20)
    address = models.CharField(max_length = 100)

    #覆寫__str__
    def __str__(self):
        return self.vendor_name

    def get_absolute_url(self):
        #return f"/vendor/{self.id}/"
        # vendor_id是url path name
        # vendors是app_name (避免 name 重複性的問題)
        return reverse("vendors:vendor_id", kwargs={"v_id": self.id})
        #return reverse("vendor_id", kwargs={"v_id": self.id})
    
    
class Food(models.Model):
    food_name = models.CharField(max_length = 30)
    price_name = models.DecimalField(max_digits = 3, decimal_places = 0)
    food_vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)

    def __str__(self):
        return self.food_name

# 為了在admin後臺可以看到vendor id
@admin.register(Vendor)    
class VendorAdmin(admin.ModelAdmin):
    # 沒有@admin.register(Vendor)的時候，這邊加完還要去admin.py註冊 -> 太麻煩
    #list_display = ('id', 'vendor_name')
    list_display = ['id', 'vendor_name', 'store_name', 'phone_number', 'address'] #一併將Vendor類別其它的欄位都加進來了

# filter food price
class MoreThanFifty(admin.SimpleListFilter):
    title = _('price')
    # URL最先要接的參數
    parameter_name = 'comparePrice'

    def lookups(self, request, model_admin):
        return(
            # 第一個對應下面querset self.value，也就是URL的request，第二個對應admin顯示文字
            ('>50', _('>50')),
            ('<=50', _('≤50')),
        )

    def queryset(self, request, querset):
        if self.value() == '>50':
            return querset.filter(price_name__gt=50)
        if self.value() == '<=50':
            return querset.filter(price_name__lte=50)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    # 顯示Food的所有欄位
    list_display = [field.name for field in Food._meta.fields]
    #list_filter = ('price_name',)
    # 另一種filter method -> 將MoreThanFifty填入
    list_filter = (MoreThanFifty,)
    # fields功能：限制 Admin 可以修改的欄位
    #exclude = ['food_name', 'food_vendor']
    fields = ['price_name']
    # 等同於於SQL的 WHERE ( food_name ILIKE '麵包' OR price_name ILIKE '麵包')
    search_fields = ['food_name', 'price_name']
    # 價格由小到大 # ordering = ('price_name',) 
    # 價格由大到小
    # 需要餵給 ordering 的值必須要為 list or tuple，而在 Python 中，括號可被解讀為 tuple or 單純的括號
    # 為了區別這個差異，所以當你要將某個參數設定為 tuple 型態且只有一個資料，後面要加上,告訴 Python 後方是一個 tuple，否則 ordering 就單純只是字串 'price_name'
    ordering = ('-price_name',) 