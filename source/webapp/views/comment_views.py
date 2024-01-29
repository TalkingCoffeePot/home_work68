from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from webapp.models import Comment, Article
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from webapp.forms import CommentForm
from django.http import JsonResponse


def comment_like_view(request):
    comment = Comment.objects.get(id=request.POST.get('commentid'))
    icon = ''
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        icon = '<i class="bi bi-heart text-danger fs-2"></i>'
    else:
        comment.likes.add(request.user)
        icon = '<i class="bi bi-heart-fill text-danger fs-2"></i>'
    return JsonResponse({'count': comment.likes.count(), 'icon': icon})

class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comments/comment_create.html'
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect('webapp:article_view', pk=article.pk)


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'comments/comment_update.html'
    model = Comment
    form_class = CommentForm
    permission_required = 'webapp.change_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})
