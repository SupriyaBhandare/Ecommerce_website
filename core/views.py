from django.shortcuts import render,redirect
from core.forms import *
from django.contrib import messages
from core.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.

def index(request):
    # products = Product.objects.all()
    return render(request,'core/index.html')

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # Query - icontains= case insensitive string search
        searched = Product.objects.filter(name__icontains = searched) 

        if not searched:
            messages.success(request,"That Product does not exist..Please try agaian!!")
            return render(request,'core/search.html')
        else:
           return render(request,'core/search.html',{'searched':searched})
    else:
        return render(request,'core/search.html')


def product(request):
    products = Product.objects.all()
    return render(request,'core/product.html', {'products':products})

def manage_data (request):
    return render(request,'core/managedata.html')

############### Product CRUD Operations ###############################################

class ProductListView(ListView):
    model = Product
    template_name = 'core/productdata.html'
    
class ProductUpdateview(UpdateView):
    model = Product
    template_name = 'core/edit_product.html'
    fields = ['name', 'category','desc','price','product_available_cnt','img']
    success_url = reverse_lazy('productdata')

class ProductDeleteview(DeleteView):
    model = Product
    template_name = 'core/delete_product.html'
    success_url = reverse_lazy('productdata')

################# Views function for products ############################################### 
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Data saved succesfully")
            messages.success(request, 'Product added successfully!')
            return redirect('productdata')
        else:
            print("Not working")
            messages.error(request, 'Failed to add product. Please check the form.')
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form':form})


def prod_desc(request,pk):
    product= Product.objects.get(pk=pk)
    return render(request, 'core/prod_desc.html', {'product':product})

    
##################### Category CRUD Operations ####################################

class manage_categorydata (ListView):
    model = Category
    template_name = 'core/categorydata.html'

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'core/add_category.html'
    fields = ['category_name']
    success_url = reverse_lazy('categorydata')

class CategoryUpdateview(UpdateView):
    model = Category
    template_name = 'core/edit_category.html'
    fields = ['category_name']
    success_url = reverse_lazy('categorydata')

class CategoryDeleteview(DeleteView):
    model = Category
    template_name = 'core/delete_category.html'
    success_url = reverse_lazy('categorydata')

################# For Cart items ####################################################

class CartItemsListView(ListView):
    model = OrderItem
    template_name = 'core/cartitems.html'

class OrderedItemsListView(ListView):
    model = Order
    template_name = 'core/ordereditems.html'

    def get_queryset(self):
        # Exclude orders where the user has not ordered any items
        return Order.objects.exclude(items__isnull=True)
 
def add_to_cart(request,pk):
    #Get product = id
    product = Product.objects.get(pk=pk)

    #create order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )

    #get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"Added quantity item")
            return redirect("prod_desc", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item Added to cart")
            return redirect("prod_desc", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item Added to cart")
        return redirect("prod_desc", pk=pk)



def orderlist(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user = request.user, ordered=False)
        return render(request,'core/orderlist.html',{'order':order})
    return render(request,'core/orderlist.html',{'message':"Your Cart is Empty"})
    

def add_item(request,pk):
    #Get product = id
    product = Product.objects.get(pk=pk)

    #create order item
    order_item, created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
    )

    #get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.product_available_cnt:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,"Added quantity item")
                return redirect("orderlist")
            else:
                messages.info(request,"Sorry, Product is out of stock")
                return redirect("orderlist")
        else:
            order.items.add(order_item)
            messages.info(request,"Item Added to cart")
            return redirect("prod_desc", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item Added to cart")
        return redirect("prod_desc", pk=pk)

def remove_item(request,pk):
    item = get_object_or_404(Product, pk=pk)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item = OrderItem.objects.filter(product=item,user=request.user, ordered=False,)[0]
            if order_item.quantity > 1 :
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request,"Item quantity updated")
            return redirect("orderlist")
        else:
            return redirect("orderlist")
    else:
        messages.info(request,"You dont have any order")
        return redirect("orderlist")


def checkout(request):
    if CheckoutAdd.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html',{'payment_allow': "allow"})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            if form.is_valid():
                address = form.cleaned_data.get('address')
                address2 = form.cleaned_data.get('address2')
                phone_no = form.cleaned_data.get('phone_no')
                state = form.cleaned_data.get('state')
                zipcode = form.cleaned_data.get('zipcode')

                checkout_address = CheckoutAdd(
                    user=request.user,
                    address=address,
                    address2=address2,
                    phone_no=phone_no,
                    state=state, 
                    zipcode=zipcode
                )

                checkout_address.save()
                return render(request, 'core/checkout.html', {"payment_allow": "allow"})
        except ObjectDoesNotExist:
            messages.warning (request, "Failed Chekout")
            return redirect('checkout')
    else:       
        form = CheckoutForm()
        return render (request, 'core/checkout.html', { 'form': form})
    

