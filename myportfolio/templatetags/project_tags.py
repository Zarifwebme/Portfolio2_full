from django import template


register = template.Library()


ICON_BY_STACK = {
    "python": "devicon-python-plain",
    "django": "devicon-django-plain",
    "drf": "bi bi-diagram-3-fill",
    "flask": "devicon-flask-original",
    "fastapi": "devicon-fastapi-plain",
    "javascript": "devicon-javascript-plain",
    "typescript": "devicon-typescript-plain",
    "react": "devicon-react-original",
    "next.js": "devicon-nextjs-original",
    "vue.js": "devicon-vuejs-plain",
    "html5": "devicon-html5-plain",
    "css3": "devicon-css3-plain",
    "tailwindcss": "devicon-tailwindcss-original",
    "bootstrap": "devicon-bootstrap-plain",
    "node.js": "devicon-nodejs-plain",
    "express": "devicon-express-original",
    "postgresql": "devicon-postgresql-plain",
    "mongodb": "devicon-mongodb-plain",
    "mysql": "devicon-mysql-original",
    "sqlite": "devicon-sqlite-plain",
    "redis": "devicon-redis-plain",
    "celery": "bi bi-hourglass-split",
    "docker": "devicon-docker-plain",
    "kubernetes": "devicon-kubernetes-plain",
    "nginx": "devicon-nginx-original",
    "linux": "devicon-linux-plain",
    "github": "devicon-github-original",
    "git": "devicon-git-plain",
    "postman": "devicon-postman-plain",
    "pytest": "devicon-pytest-plain",
    "pandas": "devicon-pandas-original",
    "numpy": "devicon-numpy-original",
    "scikit-learn": "devicon-scikitlearn-plain",
    "tensorflow": "devicon-tensorflow-original",
    "pytorch": "devicon-pytorch-original",
    "aws": "devicon-amazonwebservices-original",
    "gcp": "devicon-googlecloud-plain",
    "firebase": "devicon-firebase-plain",
    "figma": "devicon-figma-plain",
}


def _parse_stack(raw_stack):
    if not raw_stack:
        return []
    normalized = str(raw_stack)
    for sep in (",", "·", "|"):
        normalized = normalized.replace(sep, ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


@register.filter
def stack_items(raw_stack):
    items = []
    for label in _parse_stack(raw_stack):
        key = label.lower()
        icon = ICON_BY_STACK.get(key, "bi bi-code-slash")
        items.append({"label": label, "icon": icon})
    return items
