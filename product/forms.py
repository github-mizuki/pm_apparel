from django import forms
from .models import BaseProducts, Products, Pictures, Materials, Creator, LargeCategory, SmallCategory, Seasons

"""基底製品form メインクラス"""
class BaseProductsForm(forms.ModelForm):
    product_name = forms.CharField(label='製品名（Base）')
    product_code = forms.CharField(label='製品コード（Base）')
    large_category = forms.ModelChoiceField(
        label='カテゴリー（大）',
        queryset=LargeCategory.objects,
        required=False
    )
    small_category = forms.ModelChoiceField(
        label='カテゴリー（小）',
        queryset=SmallCategory.objects,
        required=False
    )
    seasons = forms.ModelMultipleChoiceField(
        label='季節',
        queryset=Seasons.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    creator = forms.ModelChoiceField(
        label='製作者',
        queryset=Creator.objects,
        required=False
    )

    class Meta:
        model = BaseProducts
        fields = ['product_name', 'product_code', 'large_category',
                  'small_category', 'seasons', 'creator']


"""基底製品　初回登録form"""
class BaseProductsRegistForm(BaseProductsForm):

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        product_name_is_exists = BaseProducts.objects.filter(product_name=product_name).first()
        if product_name_is_exists:
            raise forms.ValidationError('その基底製品名は登録されています')
        return product_name

    def clean_product_code(self):
        product_code = self.cleaned_data.get('product_code')
        product_code_is_exists = BaseProducts.objects.filter(
            product_code=product_code).first()
        if product_code_is_exists:
            raise forms.ValidationError('その基底製品コードは登録されています')
        return product_code


"""基底製品　更新form"""
class BaseProductsUpdateForm(BaseProductsForm):

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        product_name_is_exists = BaseProducts.objects.filter(product_name=product_name).first()
        if product_name == self.instance.product_name:
            return product_name
        elif product_name_is_exists:
            raise forms.ValidationError('その基底製品名は登録されています')
        else:
            return product_name

    def clean_product_code(self):
        product_code = self.cleaned_data.get('product_code')
        product_code_is_exists = BaseProducts.objects.filter(product_code=product_code).first()
        if product_code == self.instance.product_code:
            return product_code
        elif product_code_is_exists:
            raise forms.ValidationError('その基底製品コードは登録されています')
        else:
            return product_code


"""カテゴリ（大）設定用フォーム"""
class LargeCategoryForm(forms.ModelForm):
    name = forms.CharField(label="カテゴリー（大）", required=True)

    class Meta:
        model = LargeCategory
        fields = ['name']


"""カテゴリ（小）設定用フォーム"""
class SmallCategoryForm(forms.ModelForm):
    name = forms.CharField(label="カテゴリー（小）", required=True)
    largecategory = forms.ModelChoiceField(
        label = "所属カテゴリー",
        queryset = LargeCategory.objects,
        required = True
    )

    class Meta:
        model = SmallCategory
        fields = ['name', 'largecategory']


"""製作者設定用フォーム"""
class CreatorForm(forms.ModelForm):
    creator_name = forms.CharField(label='製作者名', required=True)

    class Meta:
        model = Creator
        fields = ['creator_name']


"""製品詳細form メインクラス"""
class ProductForm(forms.ModelForm):
    detail_name = forms.CharField(label='製品名')
    detail_code = forms.CharField(label='製品コード')
    color = forms.CharField(label='カラー')
    gender = forms.ChoiceField(
        label='性別',
        choices=(
            ('male', '男性'),
            ('female', '女性'),
            ('unisex', '男女兼用'),
        )
    )
    tags = forms.CharField(label='タグ', required=False)
    memo = forms.CharField(label='備考', required=False, widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Products
        exclude = ['base_product']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        super().__init__(*args, **kwargs)


"""製品詳細　初回登録form"""
class ProductRegistForm(ProductForm):

    def clean_detail_name(self):
        detail_name = self.cleaned_data.get('detail_name')
        base_product_id = self.pk
        detail_name_is_exists = Products.objects.filter(base_product_id=base_product_id, detail_name=detail_name).first()
        if detail_name_is_exists:
            raise forms.ValidationError('その製品名は登録されています')
        return detail_name

    def clean_detail_code(self):
        detail_code = self.cleaned_data.get('detail_code')
        base_product_id = self.pk
        detail_code_is_exists = Products.objects.filter(base_product_id=base_product_id, detail_code=detail_code).first()
        if detail_code_is_exists:
            raise forms.ValidationError('その製品コードは登録されています')
        return detail_code


"""製品詳細　引継登録form"""
class ProductTakeoverForm(ProductForm):

    def clean_detail_name(self):
        detail_name = self.cleaned_data.get('detail_name')
        product = Products.objects.get(id=self.pk)
        base_product_id = product.base_product_id
        detail_name_is_exists = Products.objects.filter(
            base_product_id=base_product_id, detail_name=detail_name).first()
        if detail_name_is_exists:
            raise forms.ValidationError('その製品名は登録されています')
        return detail_name

    def clean_detail_code(self):
        detail_code = self.cleaned_data.get('detail_code')
        product = Products.objects.get(id=self.pk)
        base_product_id = product.base_product_id
        detail_code_is_exists = Products.objects.filter(
            base_product_id=base_product_id, detail_code=detail_code).first()
        if detail_code_is_exists:
            raise forms.ValidationError('その製品コードは登録されています')
        return detail_code


"""製品詳細　編集form"""
class ProductUpdateForm(forms.ModelForm):
    detail_name = forms.CharField(label='詳細名')
    detail_code = forms.CharField(label='詳細コード')
    color = forms.CharField(label='識別色')
    gender = forms.ChoiceField(
        label='対象性別',
        choices=(
            ('male', '男性'),
            ('female', '女性'),
            ('unisex', '男女兼用'),
        )
    )
    tags = forms.CharField(label='タグ', required=False)
    memo = forms.CharField(label='備考欄', required=False)

    class Meta:
        model = Products
        exclude = ['base_product']

    def clean_detail_name(self):
        print(self.instance.pk)
        print(self.instance.detail_name)
        detail_name = self.cleaned_data.get('detail_name')
        product = Products.objects.get(id=self.instance.pk)
        if product.detail_name == detail_name:
            return detail_name
        else:
            base_product_id = product.base_product_id
            detail_name_is_exists = Products.objects.filter(
                base_product_id=base_product_id, detail_name=detail_name).first()
            if detail_name_is_exists:
                raise forms.ValidationError('その製品名は登録されています')
            return detail_name

    def clean_detail_code(self):
        detail_code = self.cleaned_data.get('detail_code')
        product = Products.objects.get(id=self.instance.pk)
        if product.detail_code == detail_code:
            return detail_code
        else:
            base_product_id = product.base_product_id
            detail_code_is_exists = Products.objects.filter(
                base_product_id=base_product_id, detail_code=detail_code).first()
            if detail_code_is_exists:
                raise forms.ValidationError('その製品コードは登録されています')
            return detail_code


class PicturesForm(forms.ModelForm):
    picture = forms.FileField(label='写真', required=False)

    class Meta:
        model = Pictures
        exclude = ['product']


class MaterialsForm(forms.ModelForm):
    material_name = forms.CharField(label='素材名', required=False)
    volume = forms.CharField(label='数量', required=False)

    class Meta:
        model = Materials
        exclude = ['product']

    def clean(self):
        cleaned_data = super().clean()
        material_name = cleaned_data.get('material_name')
        volume = cleaned_data.get('volume')
        if (bool(material_name) ^ bool(volume)):
            raise forms.ValidationError('素材名と数量はセットで入力してください')


class Materials_copyForm(forms.Form):
    material_name = forms.CharField(label='素材名', required=False)
    volume = forms.CharField(label='数量', required=False)

    def clean(self):
        cleaned_data = super().clean()
        material_name = cleaned_data['material_name']
        volume = cleaned_data['volume']
        if (bool(material_name) ^ bool(volume)):
            raise forms.ValidationError('素材名と数量はセットで入力してください')
