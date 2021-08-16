# from colorfield.fields import ColorField
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
# from django.db import models
#
# FoodgramUser = get_user_model()
#
#
# class Ingredient(models.Model):
#     """
#     One ingredient in recipe
#     """
#     name = models.CharField(
#         max_length=200,
#         unique=True,
#         verbose_name='Name',
#         db_index=True,
#     )
#
#     unit_of_measure = models.CharField(
#         max_length=20, verbose_name='measurement unit'
#     )
#
#     class Meta:
#         verbose_name = 'Recipe ingredient'
#         verbose_name_plural = 'Recipe ingredients'
#         ordering = ['name', ]
#
#     def __str__(self):
#         return self.name
#
#
# class Tag(models.Model):
#     name = models.CharField(
#         max_length=30,
#         unique=True,
#         verbose_name='Recipe tag name',
#     )
#     COLOR_CHOICES = [
#         ('#32cd32', 'green'),
#         ('#ff8c00', 'orange'),
#         ('#9370db', 'purple')
#     ]
#
#     color = ColorField(choices=COLOR_CHOICES)
#
#     slug = models.SlugField(
#         max_length=200,
#         unique=True,
#         verbose_name='Слаг'
#     )
#
#
# class Recipe(models.Model):
#     author = models.ForeignKey(
#         FoodgramUser,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='recipes'
#     )
#     title = models.CharField(
#         max_length=255,
#         verbose_name='Recipe title'
#     )
#     image = models.ImageField(
#         upload_to='recipe_images',
#         blank=True,
#         null=True,
#         verbose_name='Recipe image',
#         help_text='Image file only'
#     )
#     slug = models.SlugField(
#         unique=True,
#         max_length=60,
#         verbose_name='Recipes slug, a part of detail page URL',
#     )
#     description = models.TextField(
#         blank=True,
#         null=True,
#         help_text='Fill in the description',
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='RecipeIngredient',
#         blank=True,
#         help_text='Fill out some ingredients and it\'s values'
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         blank=True,
#     )
#     pub_date = models.DateTimeField(
#         verbose_name='Publication date',
#         auto_now_add=True,
#     )
#     is_active = models.BooleanField(
#         default=True,
#     )
#     time = models.PositiveIntegerField(
#         verbose_name='Cooking time in minutes',
#         validators=[MinValueValidator(1), ]
#     )

