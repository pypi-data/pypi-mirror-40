Really simple permission backend for django

Class based, No database

Inspired by [django-permission](https://github.com/lambdalisue/django-permission)

Tested with Django 1.10 - python 3.5

# Introduction

The app autodiscover perms.py module in your project's apps.

This modules should register PermissionLogic based class.

When calling django's has_perm method, it will run the corresponding method name in your PermissionLogic class.

See usage section below for comprehensive example.

# Usage

*settings.py*

```python
INSTALLED_APPS = (
  # ...
  'simple_perms',  # Add simple_perms app to your INSTALLED_APPS
  # ...
)

AUTHENTICATION_BACKENDS = (
    'simple_perms.PermissionBackend',  # Add permission backend before django's one
    'django.contrib.auth.backends.ModelBackend',
)
```

*project_app/perms.py*

```python
from simple_perms import register, PermissionLogic


class ProjectLogic(PermissionLogic):

    def add_project(self, user, project, perm):
        return True

    def change_project(self, user, project, perm):
        return user.is_admin() or project.owner == user

    delete_project = change_project

    def default_permission(self, user, project, perm):
      # Optional, default to global default permission, which default to False
      return user.is_admin()


register('project_app', ProjectLogic)
```

```python
user1.has_perm('project_app.add_project')  # True
user1.has_perm('project_app.change_project', user1_project)  # True
user1.has_perm('project_app.delete_project', user1_project)  # True
user2.has_perm('project_app.change_project', user1_project)  # False
admin.has_perm('project_app.change_project', user1_project)  # True
```

# Default permission

If a checked permission doesn't exists in registered PermissionLogic based classe, the backend will run the default_permission method of this class. If no default_permission defined, it default to the global default permission which default to False.

**Change global default permission**

*settings.py*

```python
SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION = 'path.to.custom_global_default_permission'
```

*path/to.py*
```python
def custom_global_default_permission(user, obj, perm):
    return user.is_admin()
```

global_default_permission and default_permission have the same arguments as others permissions : `(user, obj, perm)`


# Change autodiscovered module name

simple_perms autodiscover perms.py modules in every django's apps. You can change the module name to autodiscover using the SIMPLE_PERMS_MODULE_NAME setting :

```python
SIMPLE_PERMS_MODULE_NAME = 'permission'
```

# Run tests

```bash
python runtests.py
```

# Helper for your tests

```python

from django.test import TestCase
from simple_perms.helpers import AssertPermissions


class TestContractPermission(AssertPermissions, TestCase):
    def setUp(self):
        self.admin = UserFactory(role="admin")
        self.contract = ContractFactory()

    def test_permissions_for_admin(self):
        permissions = [
            { 'usr': 'admin', 'perm': 'contracts.add',    'args': (None,),           'result': True, },
            { 'usr': 'admin', 'perm': 'contracts.view',   'args': (self.contract, ), 'result': True, },
            { 'usr': 'admin', 'perm': 'contracts.change', 'args': (self.contract, ), 'result': True, },
        ]
        self.assertPerms(permissions)
```

Which fails:

``` text
======================================================================
FAIL: test_permissions_for_admin (contracts.tests.perms.TestContractPermission)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/django/contracts/tests/perms.py", line 48, in test_permissions_of_admin
    self.assertPerms(permissions)
  File "/app/django/django-simple_perms/simple_perms/helpers.py", line 37, in assertPerms
    raise e
  File "/app/django/django-simple_perms/simple_perms/helpers.py", line 66, in _test_permission_
    getattr(self, permission['usr']).has_perm(permission['perm'], *permission['args'])
AssertionError: ('PERM ERROR admin contracts.add:  False is not true', 'PERM ERROR admin contracts.view:  False is not true', 'PERM ERROR admin contracts.change:  False is not true')

----------------------------------------------------------------------
```
