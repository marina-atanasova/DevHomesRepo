from django.db import models


class CityChoices(models.TextChoices):
    SOFIA = "Sofia", "Sofia"
    PLOVDIV = "Plovdiv", "Plovdiv"
    VARNA = "Varna", "Varna"
    BURGAS = "Burgas", "Burgas"
    RUSE = "Ruse", "Ruse"
    SHUMEN = "Shumen", "Shumen"
    VIDIN = "Vidin", "Vidin"

class DistrictChoices(models.TextChoices):
    MLADOST = "Mladost", "Mladost"
    DRUJBA = "Drujba", "Drujba"
    CENTER = "Center", "Center"
    VITOSHA = "Vitosha", "Vitosha"
    HIPODRUMA = "Hipodruma", "Hipodruma"
    NADEJA = "Nadeja", "Nadeja"
    LIULIN = "Liulin", "Liulin"
    BOROVO = "Borovo", "Borovo"
    OTHER = "Other", "Other"

class PropertyTypeChoices(models.TextChoices):
    Apartment = "Apartment", "Apartment"
    House = "House", "House"
    Garage = "Garage", "Garage"
    Office = "Office", "Office"
    Land = "Land", "Land"
    Other = "Other", "Other"

class BuildTypeChoices(models.TextChoices):
    Brick = "Brick", "Brick"
    Panel = "Panel", "Panel"
    EPK = "EPK", "EPK"
    Wood = "Wood", "Wood"
    Other = "Other", "Other"

class HeatingTypeChoices(models.TextChoices):
    Gas = "Gas", "Gas"
    Electricity = "Electricity", "Electricity"
    Parno ="Parno", "Parno"
    Floor = "Floor", "Floor"
    Other = "Other", "Other"

class AptExposureChoices(models.TextChoices):
    N = "N", "North"
    E = "E", "East"
    S = "S", "South"
    W = "W", "West"
