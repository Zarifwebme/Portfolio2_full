from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ("complete", "Complete apps"),
        ("small", "Small projects"),
    ]
    BUTTON_CHOICES = [
        ("live", "Live"),
        ("github", "Github"),
        ("figma", "Figma"),
        ("cached", "Cached"),
        ("none", "None"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="complete")
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    stack = models.CharField(max_length=180, blank=True)  # "React Node.js ..." kabi
    button_type = models.CharField(max_length=20, choices=BUTTON_CHOICES, default="live")
    button_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"