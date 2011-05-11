from django import forms

# def get_user_form(user):
#   """return user's edit user form"""
#   
#   user_fields = EditUserModel.objects.filter(user = user).order_by('order')
#   class EditUserForm(forms.form):
#       def __init__(self, *args, **kwargs):
#           forms.Form.__init__(self, *args, **kwargs)
#           self.user = user
#           
#       def save(self):
#       
#           for field in user_fields:
#               setattr(EditUserForm, field.name, copy(type_mapping[field.type]))
#                 
#                 return type('EditUserForm', (forms.Form, ), dict(EditUserForm.__dict__))