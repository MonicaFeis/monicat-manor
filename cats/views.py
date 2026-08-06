from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

from .models import Cat, Reaction, DailyPet, Comment
from .forms import CatForm, CommentForm

CATS_PER_SCENE = 12


def scene(request):
    """Main landing / scene view showing all public cats in the manor."""
    # Explicit order_by prevents UnorderedObjectListWarning & 500 errors
    all_cats = Cat.objects.filter(is_public=True).order_by('-created_on')
    
    paginator = Paginator(all_cats, CATS_PER_SCENE)
    page_number = request.GET.get('page')
    cats = paginator.get_page(page_number)

    return render(request, 'cats/scene.html', {
        'cats': cats,
    })


def gallery(request):
    """Grid view displaying public cat portraits with reaction/pet counts."""
    cats_list = Cat.objects.filter(is_public=True).annotate(
        reaction_count=Count('reactions', distinct=True),
        pet_count=Count('pets', distinct=True)
    ).order_by('-created_on')

    paginator = Paginator(cats_list, 9)
    page_number = request.GET.get('page')
    cats = paginator.get_page(page_number)

    return render(request, 'cats/gallery.html', {
        'cats': cats,
    })


def cat_detail(request, pk):
    """Detail page for an individual cat portrait with comments & interactions."""
    cat = get_object_or_404(Cat, pk=pk)
    
    # Restrict private cats to owner only
    if not cat.is_public and cat.owner != request.user:
        messages.error(request, "This cat portrait is private.")
        return redirect('scene')

    comments = cat.comments.all().order_by('created_on')
    has_reacted = False
    has_petted_today = False

    if request.user.is_authenticated:
        has_reacted = Reaction.objects.filter(cat=cat, user=request.user).exists()
        has_petted_today = DailyPet.objects.filter(
            cat=cat, 
            user=request.user, 
            date=timezone.localdate()
        ).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to leave a comment.")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.cat = cat
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('cat_detail', pk=cat.pk)
    else:
        form = CommentForm()

    return render(request, 'cats/cat_detail.html', {
        'cat': cat,
        'comments': comments,
        'form': form,
        'has_reacted': has_reacted,
        'has_petted_today': has_petted_today,
    })


@login_required
def cat_create(request):
    """Create a new cat portrait entry."""
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            messages.success(request, f"{cat.name} joined MoniCat Manor!")
            return redirect('cat_detail', pk=cat.pk)
    else:
        form = CatForm()

    return render(request, 'cats/cat_form.html', {
        'form': form,
        'title': 'Add a Cat',
    })


@login_required
def cat_update(request, pk):
    """Edit an existing cat portrait (owner only)."""
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {cat.name}'s profile!")
            return redirect('cat_detail', pk=cat.pk)
    else:
        form = CatForm(instance=cat)

    return render(request, 'cats/cat_form.html', {
        'form': form,
        'cat': cat,
        'title': f'Edit {cat.name}',
    })


@login_required
def cat_delete(request, pk):
    """Delete a cat portrait (owner only)."""
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)

    if request.method == 'POST':
        cat_name = cat.name
        cat.delete()
        messages.success(request, f"{cat_name} left the manor.")
        return redirect('scene')

    return render(request, 'cats/cat_confirm_delete.html', {'cat': cat})


@login_required
def react_to_cat(request, pk):
    """Toggle or record a permanent reaction ('paw'/like) on a cat."""
    cat = get_object_or_404(Cat, pk=pk)
    reaction, created = Reaction.objects.get_or_create(cat=cat, user=request.user)

    if created:
        messages.success(request, f"You reacted to {cat.name}!")
    else:
        reaction.delete()
        messages.info(request, f"Removed reaction from {cat.name}.")

    return redirect('cat_detail', pk=cat.pk)


@login_required
def pet_cat(request, pk):
    """Give a cat a daily pet (resets daily)."""
    cat = get_object_or_404(Cat, pk=pk)
    today = timezone.localdate()

    pet, created = DailyPet.objects.get_or_create(
        cat=cat, 
        user=request.user, 
        date=today
    )

    if created:
        messages.success(request, f"You petted {cat.name} today! 🐾")
    else:
        messages.info(request, f"You already petted {cat.name} today!")

    return redirect('cat_detail', pk=cat.pk)


# ---------- Sign up ----------

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')