from django.db import models


class Location(models.Model):
    Name = models.CharField(max_length=200,default='mule_app')
    Path = models.CharField(max_length=500,default='src/main/resources')
    def url(self):
        return self.Path

    def __str__(self):
        return self.Name

class Gatekeeper(models.Model):
    Name = models.CharField(max_length=50,default='Minor',verbose_name="Criticality Name")
    Max_Allowed = models.PositiveSmallIntegerField(default=1,help_text="Maximum Number of Bugs allowed")
    def __str__(self):
        return self.Name

class Rule(models.Model):
    Name = models.CharField(max_length=200,verbose_name="Rule Name")
    Description = models.CharField(max_length=200,help_text="Proper Description of the Rule to be displayed in the result page",verbose_name="Rule Description")
    Gatekeeper = models.ForeignKey(Gatekeeper,on_delete=models.CASCADE,help_text="Criticality of Rule")
    Location = models.ForeignKey(Location,on_delete=models.CASCADE,help_text="Location Path of the Rule on which Rule condition will be scanned",verbose_name="Root Path")
    def __str__(self):
        return self.Name


class Code_Rule(Rule):
    x_Comparator_Choices = (
        ("<","Less Than"),
        (">","Greater Than"),
        ("=","Equals to"),
        ("!=", "Not Equal to"),
        ("regex","Regex"),
    )
    Condition = models.CharField(max_length=200, default='example: ** boolean(//following::comment()) **')
    Comparator = models.CharField(max_length=200, choices=x_Comparator_Choices, default='=')
    Expected_Value = models.CharField(max_length=200, default='True')

class Security_Rule(Rule):
    s_Comparator_Choices = (
        ("<","Less Than"),
        (">","Greater Than"),
        ("=","Equals to"),
        ("!=", "Not Equal to"),
        ("regex","Regex"),
    )
    Condition = models.CharField(max_length=200, default='example: ** boolean(//following::comment()) ** ')
    Comparator = models.CharField(max_length=200, choices=s_Comparator_Choices, default='=')
    Expected_Value = models.CharField(max_length=200, default='True')

class Folder_Structure_Rule(Rule):
    f_Comparator_Choices = (
        ("=", "Equals to"),
        ("!=", "Not Equal to"),
        ("endsWith", "Ends With"),
        ("startsWith","Starts With"),
        ("contains","Contains "),
        ("notContains","Does not Contain"),
    )
    condition_choices = (
        ("fileName", "File Name"),
        ("directoryName","Folder Name"),
    )

    Condition = models.CharField(max_length=200,choices=condition_choices,default='fileName')
    Comparator = models.CharField(max_length=200, choices=f_Comparator_Choices, default='=')
    Expected_Value = models.CharField(max_length=200, default='global.xml')

class Raml_Rule(Rule):
    r_Comparator_Choices = (
        ("<", "Less Than"),
        (">", "Greater Than"),
        ("=", "Equals to"),
        ("!=", "Not Equal to"),
        ("regex", "Regex"),
    )
    Condition = models.CharField(max_length=200, default='example: ** boolean(//following::comment()) ** ')
    Comparator = models.CharField(max_length=200, choices=r_Comparator_Choices, default='=')
    Expected_Value = models.CharField(max_length=200, default='True')

class Platform_Rule(Rule):
    r_Comparator_Choices = (
        ("<", "Less Than"),
        (">", "Greater Than"),
        ("=", "Equals to"),
        ("!=", "Not Equal to"),
        ("regex", "Regex"),
    )
    Condition = models.CharField(max_length=200, default='example: ** boolean(//following::comment()) ** ')
    Comparator = models.CharField(max_length=200, choices=r_Comparator_Choices, default='=')
    Expected_Value = models.CharField(max_length=200, default='True')


class Level(models.Model):
    Name = models.CharField(max_length=200,default='squid game')
    Rules = models.ManyToManyField(Rule)
    def __str__(self):
        return self.Name
    def rules_list(self):
        return ',\n'.join([r.Name for r in self.Rules.all()])