from collections import OrderedDict

from django.db import models


class Person(models.Model):
  """A model describing a person."""
  title = models.CharField(max_length=16)
  display_name = models.CharField(max_length=48)
  full_name = models.CharField(max_length=128)
  ref = models.CharField(max_length=32, null=True, blank=True, unique=True)
  brief_desc = models.CharField(max_length=256)
  # We don't use DateField because it doesn't allow us to keep null
  # some parts of the date if they are unknown.
  birth_year = models.SmallIntegerField(null=True, blank=True)
  birth_month = models.SmallIntegerField(null=True, blank=True)
  birth_day = models.SmallIntegerField(null=True, blank=True)
  death_year = models.SmallIntegerField(null=True, blank=True)
  death_month = models.SmallIntegerField(null=True, blank=True)
  death_day = models.SmallIntegerField(null=True, blank=True)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.display_name or self.full_name


class Book(models.Model):
  title = models.CharField(max_length=128, unique=True)
  brief_desc = models.CharField(max_length=256, null=True, blank=True)
  pub_year = models.SmallIntegerField(null=True, blank=True)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)


class HadithTag(models.Model):
  """A model describing a tag for hadiths."""
  name = models.CharField(max_length=32, unique=True)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.name


class Hadith(models.Model):
  """A model describing a hadith."""
  text = models.TextField()
  person = models.ForeignKey(Person)
  book = models.ForeignKey(Book, null=True)
  tags = models.ManyToManyField(HadithTag)
  added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True, auto_now_add=True)

  def __unicode__(self):
    return self.text[:100] + '...' if len(self.text) > 100 else self.text


class Chain(models.Model):
  hadith = models.ForeignKey(Hadith)


class ChainLink(models.Model):
  chain = models.ForeignKey(Chain)
  person = models.ForeignKey(Person)
  order = models.SmallIntegerField(null=False, blank=False)


class User(models.Model):
  fb_id = models.BigIntegerField(unique=True, db_index=True)
  permissions = models.BigIntegerField()

  @classmethod
  def get_unregistered_user(cls, fb_id):
    return User(fb_id=fb_id, permissions=0)

  def set_permission(self, perm_code, set_or_clear):
    if set_or_clear:
      self.permissions |= perm_code
    else:
      self.permissions &= ~perm_code

  def has_permission(self, perm_code):
    return (self.permissions & perm_code) == perm_code


class Permission(models.Model):
  name = models.CharField(max_length=128, unique=True)
  desc = models.CharField(max_length=512)
  code = models.BigIntegerField(unique=True)

  @classmethod
  def get_all(cls):
    if not hasattr(cls, 'cached_all'):
      cls.cached_all = cls.objects.all()
    return cls.cached_all

  @classmethod
  def get_code_by_name(cls, name):
    matches = filter(lambda perm: perm.name == name, cls.get_all())
    if len(matches) == 0:
      raise KeyError("Couldn't find a permission with the name '%s'" % name)
    return matches[0].code
