## EOX tenant

## EOX tenant migration notes

**Migrating from 0.\* version to 1.0.0**

From version **1.0.0**, middlewares **RedirectionsMiddleware** and **PathRedirectionMiddleware** are not longer supported in this plugin. These middlewares were moved to the **eox-core** plugin [here](https://github.com/eduNEXT/eox-core/). From this, you can have three cases:

 1. You have already installed eox-core alongside eox-tenant. In this case you need to:
- Upgrade eox-core to version **2.0.0** (previous releases are not compatible with eox-tenant 1.0.0)
- Run the plugin migrations as indicated below:
```
   $ python manage.py lms migrate eox_tenant --settings=<your app settings>
   $ python manage.py lms migrate eox_core --fake-initial --settings=<your app settings>
```
2. You only have installed eox-tenant and you want to keep the functionality the aforementioned middlewares offer. You need to:
- Install eox-core version **2.0.0** as edx-platform requirement. You can use *Ansible* to add this plugin as an extra requirement.
 - Run the plugin migrations as indicated below:
```
   $ python manage.py lms migrate eox_tenant --settings=<your app settings>
   $ python manage.py lms migrate eox_core --fake-initial --settings=<your app settings>
```

3. In the case your are not using the redirection middlewares, and only have eox-tenant installed, you can simply apply the database migrations for the eox-tenant plugin:

```
   $ python manage.py lms migrate eox_tenant --settings=<your app settings>
```

The table corresponding to the Redirection model will not be deleted but it will be discarded from the Django state
