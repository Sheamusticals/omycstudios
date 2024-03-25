from django.shortcuts import render ,get_object_or_404,redirect
from .forms import ContactForm,CommentForm
from .models import *
from django.db.models import Count
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.paginator import Paginator



def index(request):
    brands = brand.objects.all()
    types = service_type.objects.all()
    services = service.objects.all()
    context = {'brands':brands,'services':services,'types':types}
    return render (request,'index.html',context)


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        else:
           
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
      
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})



def about(request):
    return render (request,'about.html')



def blog(request):
    # Fetch all blog posts
    blogs = Blog.objects.all().order_by('-date')
    
    # Annotate queryset with year and month information for archive
    archive_dates = Blog.objects.annotate(year=ExtractYear('date'), month=ExtractMonth('date')).values('year', 'month').annotate(count=Count('id'))

    # Paginate blog posts
    paginator = Paginator(blogs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate comment count for each blog post
    comments_count = Comment.objects.values('blog').annotate(comment_count=Count('id'))
    comments_count_mapping = {item['blog']: item['comment_count'] for item in comments_count}

    # Assign comment count to each blog post
    for blog in blogs:
        blog.comment_count = comments_count_mapping.get(blog.id, 0)
    
    # Fetch types for other purposes (if needed)
    types = Type.objects.all()

    # Prepare context data
    context = {
        'blogs': blogs,
        'types': types,
        'archive_dates': archive_dates,
        'page_obj': page_obj,
    }

    # Render the template with the context data
    return render(request, 'blog.html', context)



def post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return JsonResponse({'success': True})
        else:
     
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)


    form = CommentForm()
    return render(request, 'post.html', {'blog': blog, 'form': form, 'comments': comments})
def blog_by_type(request, type_id):
   
    blog_type = Type.objects.get(pk=type_id)

 
    blogs = Blog.objects.filter(type=blog_type).order_by('-date')

    context = {'blog_type': blog_type, 'blogs': blogs}
    return render(request, 'blog_by_type.html', context)

def archive(request, year=None, month=None):
    blogs = Blog.objects.all()
    
    paginator = Paginator(blogs,12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if year is not None and month is not None:
        archive_dates = Blog.objects.filter(date__year=year, date__month=month).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    elif year is not None:
        archive_dates = Blog.objects.filter(date__year=year).annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    else:
        archive_dates = Blog.objects.annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).values('year', 'month').annotate(count=Count('id'))
    


  
    context = {'archive_dates': archive_dates, 'blogs': blogs,'page_obj':page_obj}
    return render(request, 'archive.html', context)

def tutorial(request):
    tutorials = Tutorial.objects.all().order_by('-date')
    
    paginator = Paginator(tutorials,12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'tutorials':tutorials,'page_obj':page_obj}
    return render (request,'tutorial.html',context)