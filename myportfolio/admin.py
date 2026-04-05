from django.contrib import admin
from django import forms
from .models import Project, ContactMessage


STACK_LABELS_BY_VALUE = dict(Project.STACK_CHOICES)


def _build_choices(values):
    return [(v, STACK_LABELS_BY_VALUE[v]) for v in values]


class GroupedStackCheckboxSelect(forms.CheckboxSelectMultiple):
    template_name = "admin/widgets/grouped_stack_checkboxes.html"


class ProjectAdminForm(forms.ModelForm):
    BACKEND_VALUES = [
        "python", "django", "drf", "flask", "fastapi", "nodejs", "express", "celery",
    ]
    FRONTEND_VALUES = [
        "javascript", "typescript", "react", "nextjs", "vuejs", "html5", "css3", "tailwindcss", "bootstrap",
    ]
    DATABASE_VALUES = [
        "postgresql", "mongodb", "mysql", "sqlite", "redis",
    ]
    OTHER_VALUES = [
        "docker", "kubernetes", "nginx", "linux", "github", "git", "postman", "pytest",
        "pandas", "numpy", "sklearn", "tensorflow", "pytorch", "aws", "gcp", "firebase", "figma",
    ]

    STACK_GROUPED_CHOICES = [
        ("Backend", _build_choices(BACKEND_VALUES)),
        ("Frontend", _build_choices(FRONTEND_VALUES)),
        ("Database", _build_choices(DATABASE_VALUES)),
        ("Other", _build_choices(OTHER_VALUES)),
    ]

    stack_choices = forms.MultipleChoiceField(
        label="Stack",
        choices=STACK_GROUPED_CHOICES,
        required=False,
        widget=GroupedStackCheckboxSelect,
        help_text="Stack texnologiyalarini belgilang.",
    )

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing = [item.lower() for item in self.instance.get_stack_list()]
            choices_map = {label.lower(): value for value, label in Project.STACK_CHOICES}
            self.fields["stack_choices"].initial = [
                choices_map[item] for item in existing if item in choices_map
            ]

    def clean(self):
        cleaned = super().clean()
        selected = cleaned.get("stack_choices") or []
        selected = list(dict.fromkeys(selected))
        labels_by_value = dict(Project.STACK_CHOICES)
        cleaned["stack"] = ", ".join(labels_by_value[val] for val in selected)
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get("stack_choices") or []
        selected = list(dict.fromkeys(selected))
        labels_by_value = dict(Project.STACK_CHOICES)
        instance.stack = ", ".join(labels_by_value[val] for val in selected)
        if commit:
            instance.save()
        return instance

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ("title", "category", "button_type", "is_active", "order", "created_at")
    list_filter = ("category", "is_active", "button_type")
    search_fields = ("title", "stack", "description")
    list_editable = ("is_active", "order")
    fields = (
        "category",
        "title",
        "description",
        "stack_choices",
        "image",
        "button_type",
        "button_url",
        "button_choice",
        "button_choice_url",
        "is_active",
        "order",
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "phone", "message")
    list_editable = ("is_read",)