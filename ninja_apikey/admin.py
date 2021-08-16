from django.contrib import admin, messages

from .models import APIKey
from .security import generate_key


@admin.action(description="Revoke selected API keys")  # type: ignore
def revoke_key(modeladmin, request, queryset):
    queryset.update(revoked=True)  # pragma: no cover


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = [
        "prefix",
        "user",
        "label",
        "created_at",
        "expires_at",
        "revoked",
        "is_active",
    ]
    readonly_fields = ["prefix", "hashed_key", "created_at"]
    actions = [revoke_key]
    list_filter = ["revoked"]

    @admin.display  # type: ignore
    def is_active(self, obj: APIKey):
        return obj.is_valid  # pragma: no cover

    is_active.boolean = True  # Display property as boolean

    def save_model(self, request, obj: APIKey, form, change):
        if not obj.prefix:  # New API key
            key = generate_key()
            obj.prefix = key.prefix
            obj.hashed_key = key.hashed_key

            if request:
                messages.add_message(  # pragma: no cover
                    request,
                    messages.WARNING,
                    f"The API key for {obj} is '{key.prefix}.{key.key}'."
                    "You should store it somewhere safe: "
                    "you will not be able to see the key again.",
                )

        obj.save()
        return obj
