from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self) :
        post = Post.objects.get(id = self.kwargs['pk'])
       
        #adminは全権限を持つものとしてadminであれば
        #全ユーザーのPOSTを削除、更新できるように追加。
        if str(self.request.user) == 'admin' :
            return True
        elif post.author == self.request.user :
            return True
        else :
            return False
        # return post.author == self.request.user
        
class Index(TemplateView):
    template_name = 'myapp/index.html'
    
    #このように決まってる
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        #上のpost_listをHTMLで渡してくださいという意味で下のように書く
        
        context = {
            'post_list' : post_list,
        }
        return context
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    
    #成功した場合移動する
    success_url = reverse_lazy('myapp:index')
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)
    
    def get_success_url(self) -> str:
        messages.success(self.request, 'Postを登録しました。')
        return resolve_url('myapp:index')
    
class PostDetail(DetailView):
    #DetailViewとかで送るだけならOBJECT形式でこのままでいいだが
    model = Post
    
    # get_context_dataを使った場合OBJECTの形式をし直す必要がある
    def get_context_data(self,*args, **kwargs) :
        #detailの情報を取ってFILTERで同じものを探す
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5]
        params = {
            'object' : detail_data,
            'category_posts' : category_posts,
        }
        return params


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm
    def get_success_url(self) -> str:
        messages.info(self.request, 'Postを更新しました')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin, DeleteView):
    model =Post
    
    def get_success_url(self) -> str:
        messages.info(self.request, 'Postを削除しました')
        return resolve_url('myapp:index')

class PostList(ListView):
    model = Post
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class Login(LoginView):
    form_class=LoginForm
    template_name = 'myapp/login.html'
    
    
class Logout(LogoutView):
    template_name = 'myapp/logout.html'
    
   
    
    
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')
    
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザ登録をしました')
        return HttpResponseRedirect(self.get_success_url())
    
#関数には@login_required
#classにはLoginRequiredMixin
@login_required
def Like_add(request, post_id):
    post = Post.objects.get(id= post_id)
    #likeのログインしたユーザーが開いたPOSTのデータを取って数えてくれ
    is_liked = Like.objects.filter(user=request.user).filter(post= post_id).count()
    if is_liked > 0:
        messages.info(request, 'すでにお気に入り追加済み')
        return redirect('myapp:post_detail', post.id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    
    messages.success(request, 'お気に入りに追加しました!')
    return redirect('myapp:post_detail', post.id)


class CategoryList(ListView):
    model = Category
    
    
class CategoryDetail(DetailView):
    model = Category
    #urlとして使用するために
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'
    
    #postも全部とるのてdjangoで決まってるget_context_dataをつかう
    def get_context_data(self, *args, **kwargs):
        #data一つでもあるばあいGET、０の可能もあるとFILTER
        # context = super().get_context_data(**kwargs)
        detail_data = Category.objects.get(name_en = self.kwargs['name_en'])
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')
        
        params = {
            'object' : detail_data,
            'category_posts' : category_posts,
        }
        return params
    


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)
        
        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            #大文字Qは　OR条件のいみ
            #__icontains = freeword, freewordの値が含まれているのか
            search_list = Post.objects.filter(Q(title__icontains = freeword)|Q(content__icontains = freeword))
            
        parmas = {
            'search_list' : search_list,
            
        }
        return render(request, 'myapp/search.html', parmas)