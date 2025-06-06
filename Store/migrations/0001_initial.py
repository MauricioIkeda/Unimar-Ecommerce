# Generated by Django 5.2.1 on 2025-05-28 19:28

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Carrinho",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="carrinho",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "valor_total_pedido",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "status_pagamento",
                    models.CharField(default="pendente", max_length=50),
                ),
                ("data", models.DateTimeField(auto_now_add=True)),
                (
                    "comprador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_buyer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vendedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_seller",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50)),
                (
                    "preco",
                    models.DecimalField(decimal_places=2, default=0, max_digits=6),
                ),
                (
                    "descricao",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "quantidade",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("imagem", models.ImageField(upload_to="uploads/produtos/")),
                (
                    "categoria",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Store.categoria",
                    ),
                ),
                (
                    "vendedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produtos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantidade",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="Store.order",
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Store.produto"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemCarrinho",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantidade", models.PositiveIntegerField(default=1)),
                (
                    "carrinho",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="Store.carrinho",
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Store.produto"
                    ),
                ),
            ],
        ),
    ]
