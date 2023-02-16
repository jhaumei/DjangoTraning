from django.shortcuts import render
from .models import Vendor
from .forms import VendorForm
from .forms import RawVendorForm
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView
from django import forms
from django.utils.translation import gettext_lazy as _

# Create your views here.
def vendor_index(request):
    vendor_list = Vendor.objects.all()
    # 建立Dict對應到Vendor的資料
    context = {'vendor_list': vendor_list}
    return render(request, 'vendors/info.html', context)

def vendor_create_view(request):
    form = VendorForm(request.POST or None)
    if form.is_valid():
        form.save()
        # 清空form
        form = VendorForm()

    context = {
        'form': form
    }
    return render(request, "vendors/vendor_create.html", context)

def vendor_create_view_2(request):
    form = RawVendorForm(request.POST or None)
    if form.is_valid():
        # 因為 create 裡面所帶的參數為 **kwargs，故傳入 Dict 就必須加上 ** 來 unpack
        # form 不像是 modelform 一樣具備 save() 可以直接儲存資料的功能，所以只能透過ORM的方式來存取
        Vendor.objects.create(**form.cleaned_data)
        form = RawVendorForm()

    context = {
        'form' : form
    }
    return render(request, "vendors/vendor_create.html", context)

# urls 裡面放置的參數，必須要與我們函式傳入的參數相同
def singleVendor(request, v_id):
    vendor_one = get_object_or_404(Vendor, id=v_id)
    # try:
    #     vendor_one = Vendor.objects.get(id=v_id)
    # except Vendor.DoesNotExist:
    #     raise Http404

    context = {
        'vendor_one': vendor_one
    }

    return render(request, 'vendors/details.html', context)

# 繼承ListView
class VendorListView(ListView):
    # model: 要使用哪個model(要使用哪個資料庫)，與 queryset = Vendor.objects.all()是同義的
    model = Vendor
    # template_name: 使用哪一個 template，命名之後才能覆寫
    template_name = 'vendor/vendor_list.html'

# 繼承DetailView
class VendorDetailView(DetailView):
    model = Vendor
    # queryset = Vendor.objects.all()
    template_name = 'vendor/vendor_detail.html'

class VendorCreateView(CreateView):
    # form_class = VendorModelForm
    # model + fields: 透過 我們所想要使用的 資料 及 資料欄位來建立表格
    model = Vendor
    fields = '__all__'
    # 資料欄位只會顯示vendor_name, store_name
    # fields = ['vendor_name', 'store_name']
    template_name = 'vendor/vendor_create.html'

# form_class : 我們也可以透過綁定 ModelForm 的方式來更簡化撰寫的過程
class VendorModelForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
            # fields = (
            #         'vendor_name',
            #         'store_name',
            #         'phone_number',
            #         'address',
            # )
        labels = {
            'vendor_name': _('攤販名稱'),
            'store_name' : _('店名'),
        }

class VendorCreateView_2(CreateView):
    form_class = VendorModelForm
    # model = Vendor
    # fields = '__all__'
    template_name = 'vendor/vendor_create.html'

class VendorUpdateView(UpdateView):
    form_class = VendorModelForm
    template_name = 'vendors/vendor_create.html'
    queryset = Vendor.objects.all() # 重要，因為UpdateView 會呼叫 get_object()；CreateView不會
