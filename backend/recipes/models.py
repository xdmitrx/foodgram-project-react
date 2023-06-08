from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

from colorfield.fields import ColorField

from users.models import User

from . import constants


class Ingredient(models.Model):
    """Model for Ingredient entity."""
    name = models.CharField(verbose_name='Ингредиент',
                            max_length=64,
                            )
    slug = models.SlugField(verbose_name='Слаг',
                            max_length=100,
                            editable=False,
                            )
    measurement_unit = models.TextField(verbose_name='Единицы измерения',
                                        max_length=64,
                                        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Model for Tag entity."""
    name = models.CharField(verbose_name='Тэг',
                            max_length=64,
                            )
    slug = models.SlugField(verbose_name='Слаг тэга',
                            max_length=100,
                            editable=False,
                            )
    color = ColorField(verbose_name='Цвет',
                       default='#FF0000',
                       )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model for Recipe entity."""
    name = models.CharField(verbose_name='Название блюда',
                            max_length=128,
                            unique=True,
                            )
    slug = models.SlugField(verbose_name='Слаг',
                            max_length=100,
                            editable=False,
                            )
    author = models.ForeignKey(User,
                               verbose_name='Автор рецепта',
                               db_index=True,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               )
    image = models.ImageField(verbose_name='Изображение блюда',
                              upload_to='recipes/',
                              )
    text = models.TextField(verbose_name='Описание блюда',
                            max_length=8196,
                            )
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientValue',
                                         db_index=True,
                                         related_name='recipes',
                                         verbose_name='Ингредиенты',
                                         )
    tags = models.ManyToManyField(Tag,
                                  db_index=True,
                                  related_name='recipes',
                                  verbose_name='Тэги',
                                  )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MaxValueValidator(constants.MAX_COOKING_TIME),
            MinValueValidator(constants.MIN_COOKING_TIME)
        ]
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientValue(models.Model):
    """Model for value of each ingredient in recipe entity."""
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Связанные игредиенты',
                                   db_index=True,
                                   on_delete=models.CASCADE,
                                   )
    recipe = models.ForeignKey(Recipe,
                               verbose_name='В каких рецептах',
                               db_index=True,
                               on_delete=models.CASCADE,
                               related_name='ingredient_list',
                               )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(constants.MAX_INGREDIENT_VALUE),
            MinValueValidator(constants.MIN_INGREDIENT_VALUE)
        ]
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
            f' - {self.amount} '
        )


class Favorites(models.Model):
    """Model for Favorites entity."""
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             related_name='favorites',
                             on_delete=models.CASCADE,
                             )
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Избранные рецепты',
                               related_name='favorites',
                               on_delete=models.CASCADE,
                               )

    class Meta:
        ordering = ['user']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_favorite')]

    def __str__(self):
        return f'{self.user} favorite recipes'


class Cart(models.Model):
    """Model for Cart entity."""
    user = models.ForeignKey(User,
                             verbose_name='Владелец списка',
                             related_name='shopping_cart',
                             on_delete=models.CASCADE,
                             )
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепты в списке покупок',
                               related_name='shopping_cart',
                               on_delete=models.CASCADE,
                               )

    class Meta:
        ordering = ['user']
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_cart')]

    def __str__(self):
        return f'{self.user} added "{self.recipe}" to his shopping cart'
