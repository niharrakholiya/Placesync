from django.apps import apps
from django.contrib import admin

# Get all models from the current app
models = apps.get_app_config('authentication').get_models()

# Loop through all models
for model in models:
    # Create a dynamic admin class
    class ModelAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]

    # Register the model with the dynamic admin class
    admin.site.register(model,ModelAdmin)