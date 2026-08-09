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
    shown 10 at a time standing along the same background."""
    template_name = 'cats/scene.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()

        all_cats = Cat.objects.filter(is_public=True).annotate(
            today_pet_count=Count('pets', filter=Q(pets__date=today))
        )

        paginator = Paginator(all_cats, CATS_PER_SCENE)
        page_number = self.request.GET.get('page', 1)
        context['cats'] = paginator.get_page(page_number)

        cat_of_the_day = all_cats.filter(today_pet_count__gt=0).order_by(
            '-today_pet_count', '?'
        ).first()
        context['cat_of_the_day'] = cat_of_the_day

        if self.request.user.is_authenticated:
            petted_ids = DailyPet.objects.filter(
                user=self.request.user, date=today
            ).values_list('cat_id', flat=True)
            context['petted_cat_ids'] = list(petted_ids)
        else:
            context['petted_cat_ids'] = []

        return context


# ---------- Gallery (simple grid browsing) ----------

class GalleryView(ListView):
    model = Cat
    template_name = 'cats/gallery.html'
    context_object_name = 'cats'
    paginate_by = 12

    def get_queryset(self):
        return Cat.objects.filter(is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        cat_of_the_day = Cat.objects.filter(is_public=True).annotate(
            today_pet_count=Count('pets', filter=Q(pets__date=today))
        ).filter(today_pet_count__gt=0).order_by('-today_pet_count', '?').first()
        context['cat_of_the_day'] = cat_of_the_day
        return context


# ---------- My Cats (personal collection) ----------

class MyCatsView(LoginRequiredMixin, ListView):
    model = Cat
    template_name = 'cats/my_cats.html'
    context_object_name = 'cats'
    paginate_by = 12

    def get_queryset(self):
        return Cat.objects.filter(owner=self.request.user)


# ---------- Cat detail (full profile page) ----------

class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/cat_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_has_reacted'] = self.object.reactions.filter(
                user=self.request.user
            ).exists()
        else:
            context['user_has_reacted'] = False
        return context


# ---------- Create / Update / Delete a cat ----------

class CatCreateView(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'personality', 'coat_color', 'drawing_image', 'is_public']
    template_name = 'cats/cat_form.html'
    success_url = reverse_lazy('scene')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CatUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cat
    fields = ['name', 'personality', 'coat_color', 'drawing_image', 'is_public']
    template_name = 'cats/cat_form.html'

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.object.pk})


class CatDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cat
    template_name = 'cats/cat_confirm_delete.html'
    success_url = reverse_lazy('my_cats')

    def test_func(self):
        return self.get_object().owner == self.request.user


@login_required
def toggle_visibility(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)
    cat.is_public = not cat.is_public
    cat.save()
    return redirect('my_cats')


# ---------- Comments ----------

@login_required
def add_comment(request, pk):
    cat = get_object_or_404(Cat, pk=pk, is_public=True)
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            Comment.objects.create(cat=cat, author=request.user, body=body)
    return redirect('cat_detail', pk=cat.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'cats/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.object.cat.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'cats/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.object.cat.pk})


# ---------- Reactions ----------

@login_required
def toggle_reaction(request, pk):
    cat = get_object_or_404(Cat, pk=pk, is_public=True)
    reaction, created = Reaction.objects.get_or_create(cat=cat, user=request.user)
    reacted = True
    if not created:
        reaction.delete()
        reacted = False

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'reacted': reacted,
            'count': cat.reactions.count(),
        })
    return redirect('cat_detail', pk=cat.pk)


# ---------- Daily petting (Cat of the Day) ----------

@login_required
def pet_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk, is_public=True)
    today = timezone.localdate()
    pet, created = DailyPet.objects.get_or_create(cat=cat, user=request.user, date=today)

    today_count = cat.pets.filter(date=today).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'petted_today': True,
            'already_petted': not created,
            'today_count': today_count,
        })
    return redirect('cat_detail', pk=cat.pk)


# ---------- Sign up ----------

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')