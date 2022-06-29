import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from . import models, forms


"""小カテゴリ動的生成"""
def ajax_get_smallcategory(request):
    pk = request.GET.get('pk')
    if not pk:
        category_list = models.SmallCategory.objects.all()
    else:
        category_list = models.SmallCategory.objects.filter(largecategory_id=pk)
    category_list = [{'pk': category.pk, 'name': category.name}
                     for category in category_list]
    return JsonResponse(
        {'categoryList': category_list}
    )


"""大カテゴリ自動選択"""
def ajax_select_largecategory(request):
    pk = request.GET.get('pk')
    if not pk:
        largecategory_id = None
    else:
        smallcategory = models.SmallCategory.objects.get(id=pk)
        largecategory_id = smallcategory.largecategory_id
    return JsonResponse({'pk': largecategory_id})


"""素材modelformset生成"""
def modelformset_create(form, extra, can_delete):
    Materials_FormSet = modelformset_factory(
        model=models.Materials,
        form=form,
        extra=extra,
        max_num=10,
        can_delete=can_delete
    )
    return Materials_FormSet


"""素材formset生成(初期値設定用)"""
def formset_create(form, extra, can_delete):
    Materials_FormSet = formset_factory(
        form=form,
        extra=extra,
        max_num=10,
        can_delete=can_delete
    )
    return Materials_FormSet


"""Topページ仮"""
class IndexView(TemplateView):
    template_name = 'index.html'


"""製品一覧"""
class ProductListView(ListView):
    template_name = os.path.join('product', 'product_list.html')
    model = models.BaseProducts

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-create_at')
        return qs


"""製品基底情報　初回登録"""
class BaseProductRegistView(CreateView):
    template_name = os.path.join('product', 'baseproduct_regist.html')
    form_class = forms.BaseProductsRegistForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baseproducts_form'] = self.form_class
        return context

    def form_valid(self, form):
        baseproduct = form.save(commit=False) # 多対多レコード保存には元のフォームが必要なため、別の変数に格納する。
        baseproduct.save()
        form.save_m2m()  # 元々のフォームに対して「save_m2m()」することで多対多レコードの保存が可能。
        if 'button_1' in self.request.POST:
            return redirect('product:index')
        elif 'button_2' in self.request.POST:
            return redirect('product:product_regist', pk=baseproduct.id)


"""製品基底情報 更新"""
class BaseProductUpdateView(UpdateView):
    template_name = os.path.join('product', 'baseproduct_update.html')
    model = models.BaseProducts
    form_class = forms.BaseProductsUpdateForm

    def get_success_url(self):
        return reverse_lazy('product:product_list')


"""製品基底情報 詳細"""
class BaseProductDetailView(DetailView):
    model = models.BaseProducts
    template_name = os.path.join('product', 'baseproduct_detail.html')


"""製品詳細情報　初回登録"""
class ProductRegistView(CreateView):
    template_name = os.path.join('product', 'product_regist.html')
    form_class = forms.ProductRegistForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baseproduct'] = models.BaseProducts.objects.get(pk=self.kwargs.get('pk'))
        context['products_form'] = self.get_form()
        context['pictures_form'] = forms.PicturesForm()
        Materials_FormSet = modelformset_create(form=forms.MaterialsForm, extra=3, can_delete=False)
        context['materials_formset'] = Materials_FormSet(queryset=models.Materials.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        products_form = self.get_form()
        pictures_form = forms.PicturesForm(self.request.POST or None, self.request.FILES or None)
        Materials_FormSet = modelformset_create(form=forms.MaterialsForm, extra=3, can_delete=False)
        materials_formset = Materials_FormSet(self.request.POST or None, queryset=models.Materials.objects.none())
        if products_form.is_valid() and pictures_form.is_valid() and materials_formset.is_valid():
            products_form = products_form.save(commit=False)
            products_form.base_product_id = self.kwargs.get('pk')
            products_form.save()
            if self.request.FILES:
                pictures_form = pictures_form.save(commit=False)
                pictures_form.product_id = products_form.id
                pictures_form.save()
            materials_formset = materials_formset.save(commit=False)
            for material_form in materials_formset:
                material_form.product_id = products_form.id
                material_form.save()
            if 'button_1' in self.request.POST:
                return redirect('product:product_list')
            elif 'button_2' in self.request.POST:
                return redirect('product:product_copy', pk=products_form.id)
        else:
            context = self.get_context_data()
            context['products_form'] = products_form
            context['pictures_form'] = pictures_form
            context['materials_formset'] = materials_formset
            return self.render_to_response(context)


"""製品詳細情報　引継登録"""
class ProductTakeOverView(CreateView):
    template_name = os.path.join('product', 'product_copy.html')
    form_class = forms.ProductTakeoverForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    """form_classの初期値を設定"""
    def get_initial(self):
        initial = super().get_initial()
        takeover_product = get_object_or_404(models.Products, pk=self.kwargs.get('pk'))
        initial['detail_name'] = takeover_product.detail_name
        initial['detail_code'] = takeover_product.detail_code
        initial['color'] = takeover_product.color
        initial['gender'] = takeover_product.gender
        initial['tags'] = takeover_product.tags
        initial['memo'] = takeover_product.memo
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Products.objects.get(pk=self.kwargs.get('pk'))
        context['products_form'] = self.get_form()
        context['pictures_form'] = forms.PicturesForm()
        materials = models.Materials.objects.filter(product_id=self.kwargs.get('pk'))
        Materials_FormSet = formset_create(form=forms.Materials_copyForm, extra=0, can_delete=False)
        context['materials_formset'] = Materials_FormSet(
            initial=[
                {'material_name': material.material_name, 'volume': material.volume} for material in materials
            ]
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        takeover_product = get_object_or_404(models.Products, pk=self.kwargs.get('pk'))
        products_form = self.get_form()
        pictures_form = forms.PicturesForm(self.request.POST or None, self.request.FILES or None)
        Materials_FormSet = formset_create(form=forms.Materials_copyForm, extra=3, can_delete=False)
        materials_formset = Materials_FormSet(self.request.POST or None)
        if products_form.is_valid() and pictures_form.is_valid() and materials_formset.is_valid():
            products_form = products_form.save(commit=False)
            products_form.base_product_id = takeover_product.base_product_id
            products_form.save()
            if self.request.FILES:
                pictures_form = pictures_form.save(commit=False)
                pictures_form.product_id = products_form.id
                pictures_form.save()
            for material_form in materials_formset:
                material_name = material_form.cleaned_data.get('material_name')
                volume = material_form.cleaned_data.get('volume')
                models.Materials.objects.create(material_name=material_name, volume=volume, product_id=products_form.id)
            if 'button_1' in self.request.POST:
                return redirect('product:product_list')
            elif 'button_2' in self.request.POST:
                return redirect('product:product_copy', pk=products_form.id)
        else:
            context = self.get_context_data()
            context['products_form'] = products_form
            context['pictures_form'] = pictures_form
            context['materials_formset'] = materials_formset
            return self.render_to_response(context)


"""製品詳細情報　編集"""
class ProductUpdateView(UpdateView):
    template_name = os.path.join('product', 'product_update.html')
    model = models.Products
    form_class = forms.ProductUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['product'] = models.Products.objects.get(
            pk=self.kwargs.get('pk'))
        context['pictures'] = models.Pictures.objects.filter(
            product_id=self.kwargs.get('pk'))
        context['products_form'] = self.get_form()
        context['pictures_form'] = forms.PicturesForm(
            instance=self.object)
        Materials_FormSet = modelformset_create(
            form=forms.MaterialsForm, extra=0, can_delete=True)
        context['materials_formset'] = Materials_FormSet(
            queryset=models.Materials.objects.filter(product_id=self.kwargs.get('pk')))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        products_form = forms.ProductUpdateForm(self.request.POST or None, instance=self.object)
        pictures_form = forms.PicturesForm(
            self.request.POST or None, self.request.FILES or None)
        Materials_FormSet = modelformset_create(
            form=forms.MaterialsForm, extra=0, can_delete=True)
        materials_formset = Materials_FormSet(
            request.POST or None, queryset=models.Materials.objects.filter(product_id=self.kwargs.get('pk')))
        if products_form.is_valid() and pictures_form.is_valid() and materials_formset.is_valid():
            products_form = products_form.save(commit=False)
            products_form.save()
            if request.FILES:
                pictures_form = pictures_form.save(commit=False)
                pictures_form.product_id = self.kwargs.get('pk')
                pictures_form.save()
            formset = materials_formset.save(commit=False)
            if materials_formset.deleted_objects:
                for file in materials_formset.deleted_objects:
                    file.delete()
            for material_form in formset:
                material_form.product_id = self.kwargs.get('pk')
                material_form.save()
            return redirect('product:product_detail', pk=self.kwargs.get('pk'))
        else:
            context = self.get_context_data()
            context['product'] = models.Products.objects.get(
                pk=self.kwargs.get('pk'))
            context['pictures'] = models.Pictures.objects.filter(
                product_id=self.kwargs.get('pk'))
            context['products_form'] = products_form
            context['pictures_form'] = pictures_form
            context['materials_formset'] = materials_formset
            return self.render_to_response(context)


"""製品詳細情報 詳細"""
class ProductDetailView(DetailView):
    model = models.Products
    template_name = os.path.join('product', 'product_detail.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = models.Pictures.objects.filter(
            product_id=self.object.pk)
        context['materials'] = models.Materials.objects.filter(
            product_id=self.object.pk)
        return context


"""設定TOP"""
class ConfigTopView(TemplateView):
    template_name = os.path.join('product', 'config_top.html')


"""カテゴリ登録"""
class CategoryRegistView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {
            'largecategory_form': forms.LargeCategoryForm(),
            'largecategory_list': models.LargeCategory.objects.all(),
            'smallcategory_form': forms.SmallCategoryForm(),
        }

    def get(self, request, *args, **kwargs):
        return render(request, 'product/category_regist.html', self.context)

    def post(self, request, *args, **kwargs):
        if 'largecategory_button' in self.request.POST:
            largecategory_form = forms.LargeCategoryForm(request.POST or None)
            if largecategory_form.is_valid():
                largecategory_form.save()
                return redirect('product:category_regist')
            else:
                self.context['largecategory_form'] = largecategory_form
                return render(request, 'product/category_regist.html', self.context)
        if 'smallcategory_button' in self.request.POST:
            smallcategory_form = forms.SmallCategoryForm(request.POST or None)
            if smallcategory_form.is_valid():
                smallcategory_form.save()
                return redirect('product:category_regist')
            else:
                self.context['smallcategory_form'] = smallcategory_form
                return render(request, 'product/category_regist.html', self.context)


"""カテゴリー（大）編集"""
class LargeCategoryUpdateView(UpdateView):
    model = models.LargeCategory
    form_class = forms.LargeCategoryForm
    template_name = os.path.join('product', 'largecategory_update.html')
    success_url = reverse_lazy('product:category_regist')


"""カテゴリー（大）削除"""
class LargeCategoryDeleteView(DeleteView):
    model = models.LargeCategory
    template_name = os.path.join('product', 'largecategory_delete.html')
    success_url = reverse_lazy('product:category_regist')


"""カテゴリー（小）編集"""
class SmallCategoryUpdateView(UpdateView):
    model = models.SmallCategory
    form_class = forms.SmallCategoryForm
    template_name = os.path.join('product', 'smallcategory_update.html')
    success_url = reverse_lazy('product:category_regist')


"""カテゴリー（小）削除"""
class SmallCategoryDeleteView(View):

    def get(self, request, *args, **kwargs):
        if 'smallcategorySelect' in self.request.GET:
            post_pks = self.request.GET.getlist('smallcategorySelect')
            post_pks_int = list(map(int, post_pks))
            delete_categories = models.SmallCategory.objects.filter(pk__in=post_pks_int)
            return render(request, 'product/smallcategory_delete.html', {'delete_categories': delete_categories})
        else:
            return render(request, 'product/smallcategory_delete.html')

    def post(self, request, *args, **kwargs):
        post_pks = self.request.GET.getlist('smallcategorySelect')
        post_pks_int = list(map(int, post_pks))
        delete_categories = models.SmallCategory.objects.filter(pk__in=post_pks_int)
        if delete_categories:
            delete_categories.delete()
            return redirect('product:category_regist')
        else:
            return redirect('product:smallcategory_delete')



"""製作者登録"""
class CreatorRegistView(CreateView):
    model = models.Creator
    form_class = forms.CreatorForm
    template_name = os.path.join('product', 'creator_regist.html')
    success_url = reverse_lazy('product:creator_regist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creator_list'] = models.Creator.objects.all()
        return context

    def form_valid(self, form):
        return super().form_valid(form)


"""製作者編集"""
class CreatorUpdateView(UpdateView):
    model = models.Creator
    form_class = forms.CreatorForm
    template_name = os.path.join('product', 'creator_update.html')
    success_url = reverse_lazy('product:creator_regist')


"""製作者削除"""
class CreatorDeleteView(DeleteView):
    model = models.Creator
    template_name = os.path.join('product', 'creator_delete.html')
    success_url = reverse_lazy('product:creator_regist')