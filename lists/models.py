from django.db import models

# Create your models here.

class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.SET_DEFAULT)


# CASCADE: when you delete the UserProfile, all related Photos will be deleted too.
# This is the default. (So in answer to that aspect of your question, yes,
#  if you delete your user account the photos will be deleted automatically.)
#
# PROTECT: this will stop you from deleting a UserProfile with related Photos,
# raising a django.db.models.ProtectedError if you try. The idea would be that
# the user would need to disassociate or delete all Photos before they could delete
# their profile.
#
# SET_NULL: when you delete the UserProfile, all associated Photos will still exist
# but will no longer be associated with any UserProfile.
# This would require null=True in the ForeignKey definition.
#
# SET_DEFAULT: when you delete the UserProfile, all associated Photos will be changed
# to point to their default UserProfile as specified by the default attribute in the ForeignKey
# definition (you could use this to pass "orphaned" photos off to a certain
# user - but this isn't going to be common, SET_NULL or SET() will be much more common)
#
# SET(): when you delete the UserProfile, the target of the Photos
# ' ForeignKey will be set to the value passed in to the SET function,' \
# ' or what it returns if it is a callable. (Sorry, I haven't explained that well,
# but the docs have an example which explains better.)
#
# DO_NOTHING: when you delete the UserProfile, all related Photos will remain unaltered,
# thus having a broken reference, unless you have used some other SQL to take care of it.