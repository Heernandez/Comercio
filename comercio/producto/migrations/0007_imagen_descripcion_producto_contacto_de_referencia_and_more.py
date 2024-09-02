# Generated by Django 5.0.4 on 2024-09-01 03:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("producto", "0006_remove_producto_contacto_de_referencia_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="imagen",
            name="descripcion",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="producto",
            name="contacto_de_referencia",
            field=models.CharField(default=10, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="producto",
            name="stock_disponible",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="subproducto",
            name="stock_disponible",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="imagen",
            name="imagen",
            field=models.ImageField(upload_to="imagenes/"),
        ),
        migrations.AlterField(
            model_name="producto",
            name="nombre",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="subproducto",
            name="nombre",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="subproducto",
            name="precio",
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
            preserve_default=False,
        ),
    ]
