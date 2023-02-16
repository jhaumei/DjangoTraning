from django import forms
from .models import Vendor, Food
from django.utils.translation import gettext_lazy as _

# ModelFrom: 透過model創建form，讓我們能夠更方便地去處理資料庫
class VendorForm(forms.ModelForm):
    class Meta:
        # 要使用哪個model
        model = Vendor
        # 使用 Model 的哪些欄位
        fields = '__all__'
        # 對應
        labels = {
            'vendor_name': _('攤販名稱'),
        }

# 創建一個 Raw Form  # 創建Form就跟創建Model很像
# 有時候我們不需要直接將使用者所輸入的內容存進資料庫
# 而是針對使用者填入的內容做處理及判斷，最後再做出相對應的處理
class RawVendorForm(forms.Form):
    vendor_name = forms.CharField()
    store_name = forms.CharField()
    phone_number = forms.CharField()
    # 這裡沒有address
    