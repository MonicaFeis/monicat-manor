from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Cat, Comment, Reaction, DailyPet

CATS_PER_SCENE = 8


# ---------- The shared scene (homepage) ----------

class SceneView(TemplateView):
    """The homepage: an illustrated scene populated with public cats,
    shown 8 at a time standing along the same background."""
    template_name = 'cats/scene.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        # Add ordering so PostgreSQL pagination doesn't fail
        all_cats = Cat.objects.filter(is_public=True).annotate(
            today_pet_count=Count('pets', filter=Q(pets__date=today))
        ).order_by('-created_at' if hasattr(Cat, 'created_at') else '-id')

        paginator = Paginator(all_cats, CATS_PER_SCENE)
        page_number = self.request.GET.get('page', 1)
        context['cats'] = paginator.get_page(page_number)

        # Separate explicit query for cat of the day
        cat_of_the_day = Cat.objects.filter(is_public=True).annotate(
            today_pet_count=Count('pets', filter=Q(pets__date=today))
        ).filter(today_pet_count__gt=0).order_by('-today_pet_count', 'id').first()

        context['cat_of_the_day'] = cat_of_the_day

        if self.request.user.is_authenticated:
            petted_ids = DailyPet.objects.filter(
                user=self.request.user, date=today
            ).values_list('cat_id', flat=True)
            context['petted_cat_ids'] = list(petted_ids)
        else:
            context['petted_cat_ids'] = []

        return context