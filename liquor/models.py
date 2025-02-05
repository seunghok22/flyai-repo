from django.db import models


class Brewery(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Breweries"
        db_table = 'breweries'


class TraditionalLiquor(models.Model):
    brewery = models.ForeignKey(
        Brewery, 
        on_delete=models.CASCADE, 
        related_name='liquors'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    characteristics = models.JSONField()
    alcohol_percentage = models.FloatField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'traditional_liquors'


class TopLiquor(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    characteristics = models.JSONField()
    rank = models.IntegerField()
    year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} (Rank: {self.rank})"

    class Meta:
        db_table = 'top_liquors'


class LiquorIngredient(models.Model):
    liquor = models.ForeignKey(
        TraditionalLiquor, 
        on_delete=models.CASCADE, 
        related_name='ingredients'
    )
    name = models.CharField(max_length=100)
    percentage = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.liquor.name}"

    class Meta:
        db_table = 'liquor_ingredients'


class SimilarLiquor(models.Model):
    liquor = models.ForeignKey(
        TraditionalLiquor, 
        on_delete=models.CASCADE, 
        related_name='similar_to'
    )
    similar_liquor = models.ForeignKey(
        TopLiquor, 
        on_delete=models.CASCADE, 
        related_name='similar_from'
    )
    similarity_score = models.FloatField()
    similarity_factors = models.JSONField()

    def __str__(self):
        return f"{self.liquor.name} similar to {self.similar_liquor.name}"

    class Meta:
        db_table = 'similar_liquors'