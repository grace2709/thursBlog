from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name= "posts/posts.html"
def post_list(request, tag_slug=None):

    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=Post.published.all(tags__in=[tag])
    #PAGINATION WITH THREE PAGEA
    paginator = Paginator(post_list,3)
    page_number = request.GET.get("page",1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,"posts/posts.html",{"posts":posts,"tag":tag})

def post_detail(request, post, year, month, day):

   post  =get_object_or_404(Post,status=Post.Status.PUBLISHED,
                           slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day
                            )
   comments = post.comments.filter(active=True)
   form = CommentForm()
   print(form.errors)
   #list of dimilar posts

   post_tags_ids = post.tags.values_list('id',flat=True)
   similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
   similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

   return render(request,"posts/post_detail.html",{"post":post,"form":form,"comments":comments,"similar_posts":similar_posts})


def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'canyanwu625@gmail.com',[cd['to']])
            sent = True

    else:
        form = EmailPostForm()
        return render(request,'posts/share.html',{"post":post,"form":form,"sent":sent})
#retrieve post by id

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment  = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            form = CommentForm()
        return render(request, "posts/comment.html", {"post":post, "form":form, "comment":comment})






