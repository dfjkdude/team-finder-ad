import re

from django.forms import ValidationError
from django.shortcuts import redirect


class GitHubURLValidationMixin:
    cleaned_data: dict

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        pattern = r'^https://github\.com/[a-zA-Z0-9_-]+'
        if github_url is None:
            return github_url
        elif re.match(pattern, github_url):
            return github_url
        raise ValidationError("Недопустимый формат записи ссылки на GitHub")


class ProjectOwnerRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.is_staff:
            return redirect('projects:detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)   