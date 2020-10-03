from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator,Page, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User,auth
from django.views.generic import  ListView,View#,DetailView,TemplateView
from .models import *
from django.db.models import Q



"""class HomeView(ListView):
	model = Item
	paginate_by = 3
	template_name = 'catalog/home.html'
	context_object_name = 'items'  """


def home(request):
	slides = slider.objects.all().order_by('id')[:7]
	items_list = Item.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(items_list, 8)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	context = {'slides':slides,'items':items,}
	return render(request,'catalog/home.html',context)

def abouts(request):
	objects = about.objects.all()
	abt = about1.objects.all()

	context = {
		'objects':objects,
		'abt':abt
		}
	return render(request,'catalog/about.html',context)


class SearchResultsView(ListView):
    model = Item
    template_name = 'catalog/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query)|Q
            (description__icontains=query)
        )
        return object_list

"""class ProductDetail(DetailView):
	model = Item
	template_name = 'catalog/product.html'  """

def product(request,slug):
	object = get_object_or_404(Item, slug=slug)
	#item = Item.objects.all()
	prod = addition_info.objects.filter(slug=slug)
	context = {
		'object':object,
		'prod':prod
	}
	return render(request,'catalog/product.html',context)


class OrderSummaryView(View):
	def get(self,*args,**kwargs):
		order = Order.objects.get(user=self.request.user,ordered=False)
		context = {
			'order':order
		}
		return render(self.request, 'catalog/order_summary.html',context)


def checkout(request):
	return render(request,'catalog/checkout.html')



def add_to_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)
	order_item,created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.success(request, f"{item.title}'s quantity was updated")
			return redirect('product',slug=slug)
		else:
			order.items.add(order_item)
			order.save()
			messages.success(request, f"{item.title} was added to your cart" )
			return redirect('product',slug=slug)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user=request.user,ordered=False,ordered_date=ordered_date)
		order.items.add(order_item)
		order.save()
		messages.success(request, f"{item.title} was added to your cart")
		return redirect('order_summary')

def remove_from_cart(request,slug):
	item = get_object_or_404(Item,slug=slug)
	order_item, created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False,)
	order_qs = Order.objects.filter(user=request.user,ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item__slug=item.slug).exists():
			order.items.remove(order_item)
			order.save()
			messages.success(request, f"{item.title}  was removed from your cart")
			return redirect('order_summary')
		else:
			messages.info(request, f"{item.title} was not in your cart" )
			return redirect('order_summary')
	else:
		messages.info(request, "You don't have an active order!" )
		return redirect('product',slug=slug)



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                messages.success(request, 'Congrats for signing up!')
                return redirect('signup')
        else:
            messages.info(request, 'password does not match')
            return redirect('signup')

    else:
        return render(request,'registration/signup.html',{'title':'signup'})






