from django.db import models


# 基底クラス
class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 製品基底モデル
class BaseProducts(BaseModel):
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    small_category = models.ForeignKey('SmallCategory', on_delete=models.SET_NULL, null=True, blank=True)
    seasons = models.ManyToManyField('Seasons', through='SeasonsRelation')
    creator = models.ForeignKey('Creator', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'base_products'
        verbose_name_plural = 'BaseProducts'

    def __str__(self):
        return self.product_name


# 大カテゴリーモデル
class LargeCategory(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'largecategory'
        verbose_name_plural = 'LargeCategory'

    def __str__(self):
        return self.name


# 季節モデル
class Seasons(BaseModel):
    season = models.CharField(max_length=100)

    class Meta:
        db_table = 'seasons'
        verbose_name_plural = 'Seasons'

    def __str__(self):
        return self.season


# BaseProducts ←→ Seasons　中間モデル
class SeasonsRelation(BaseModel):
    baseproduct = models.ForeignKey('BaseProducts', on_delete=models.CASCADE)
    season = models.ForeignKey('Seasons', on_delete=models.CASCADE)


# 小カテゴリーモデル
class SmallCategory(BaseModel):
    name = models.CharField(max_length=100)
    largecategory = models.ForeignKey('LargeCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'smallcategory'
        verbose_name_plural = 'SmallCategory'

    def __str__(self):
        return self.name


# 製作者モデル
class Creator(BaseModel):
    creator_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'creator'
        verbose_name_plural = 'Creator'

    def __str__(self):
        return self.creator_name


# 製品詳細モデル
class Products(BaseModel):
    detail_name = models.CharField(max_length=100)
    detail_code = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    gender =  models.CharField(max_length=100)
    tags = models.CharField(null=True, blank=True, default=None, max_length=100)
    memo = models.TextField(null=True, blank=True, default=None, max_length=1000)
    base_product = models.ForeignKey('BaseProducts', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.detail_name


# アップロード画像モデル
class Pictures(BaseModel):
    picture = models.FileField(null=True, blank=True, default=None, upload_to='picture/%Y/%m/%d')
    product = models.ForeignKey('Products', on_delete=models.CASCADE)

    class Meta:
        db_table = 'pictures'
        verbose_name_plural = 'Pictures'

    def __str__(self):
        return self.product.base_product.product_name + ' / ' + self.product.detail_name


# 素材モデル
class Materials(BaseModel):
    material_name = models.CharField(null=True, blank=True, max_length=200)
    volume = models.CharField(null=True, blank=True, default=None, max_length=100)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)

    class Meta:
        db_table = 'materials'
        verbose_name_plural = 'Materials'

    def __str__(self):
        return self.material_name
