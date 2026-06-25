from django import forms

from utils.mixins import GitHubURLValidationMixin
from .models import Project


class ProjectCreateForm(GitHubURLValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
