from asyncorm import models


BOOK_CHOICES = (("hard cover", "hard cover book"), ("paperback", "paperback book"))


SIZE_CHOICES = (("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"))
POWER_CHOICES = {"neo": "feo", "pow": "dow", "saw": "mao"}


def weight():
    return 85


class Publisher(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    json = models.JsonField(max_length=50, null=True)

    mac = models.MACAdressField(null=True, dialect="unix")
    inet = models.GenericIPAddressField(
        null=True, protocol="both", unpack_protocol="ipv4"
    )


class Author(models.Model):
    na = models.AutoField(db_column="uid")
    name = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=100, null=True, db_index=True)
    age = models.IntegerField()
    publisher = models.ManyToManyField(foreign_key="Publisher")


class Book(models.Model):
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=255, choices=BOOK_CHOICES)
    date_created = models.DateField(auto_now=True)
    author = models.ForeignKey(foreign_key="Author", null=True)
    price = models.DecimalField(default=25)
    quantity = models.IntegerField(default=1)

    @staticmethod
    def its_a_2():
        return 2

    class Meta:
        table_name = "library"
        ordering = ["-id"]
        unique_together = ["name", "content"]


class Reader(models.Model):
    name = models.CharField(max_length=15, default="pepito")
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    power = models.CharField(choices=POWER_CHOICES, max_length=2, null=True)
    weight = models.IntegerField(default=weight)
