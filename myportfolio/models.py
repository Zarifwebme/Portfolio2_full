from django.db import models
from django.core.exceptions import ValidationError


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
    STACK_CHOICES = [
        ("python", "Python"),
        ("django", "Django"),
        ("drf", "DRF"),
        ("flask", "Flask"),
        ("fastapi", "FastAPI"),
        ("javascript", "JavaScript"),
        ("typescript", "TypeScript"),
        ("react", "React"),
        ("nextjs", "Next.js"),
        ("vuejs", "Vue.js"),
        ("html5", "HTML5"),
        ("css3", "CSS3"),
        ("tailwindcss", "TailwindCSS"),
        ("bootstrap", "Bootstrap"),
        ("nodejs", "Node.js"),
        ("express", "Express"),
        ("postgresql", "PostgreSQL"),
        ("mongodb", "MongoDB"),
        ("mysql", "MySQL"),
        ("sqlite", "SQLite"),
        ("redis", "Redis"),
        ("celery", "Celery"),
        ("docker", "Docker"),
        ("kubernetes", "Kubernetes"),
        ("nginx", "Nginx"),
        ("linux", "Linux"),
        ("github", "GitHub"),
        ("git", "Git"),
        ("postman", "Postman"),
        ("pytest", "Pytest"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-learn"),
        ("tensorflow", "TensorFlow"),
        ("pytorch", "PyTorch"),
        ("aws", "AWS"),
        ("gcp", "GCP"),
        ("firebase", "Firebase"),
        ("figma", "Figma"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="complete")
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    stack = models.CharField(max_length=500, blank=True)  # "React, Node.js, Django" kabi
    button_type = models.CharField(max_length=20, choices=BUTTON_CHOICES, default="live")
    button_url = models.URLField(blank=True)
    button_choice = models.CharField(
        max_length=20,
        choices=[("none", "None"), ("github", "Github")],
        default="none",
        blank=True,
    )
    button_choice_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def get_stack_list(self):
        if not self.stack:
            return []
        separators = [",", "·", "|"]
        normalized = self.stack
        for sep in separators:
            normalized = normalized.replace(sep, ",")
        return [item.strip() for item in normalized.split(",") if item.strip()]

    def clean(self):
        super().clean()
        if self.button_type != "live" and self.button_choice != "none":
            raise ValidationError(
                {"button_choice": "Qo'shimcha tugma faqat Live tugma tanlanganda ishlaydi."}
            )
        if self.button_choice != "none" and not self.button_choice_url:
            raise ValidationError(
                {"button_choice_url": "Qo'shimcha tugma uchun URL kiriting."}
            )

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