from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from urllib.parse import urlencode
from django.contrib.messages import info, warning, success
from .models import Product
from .forms import ProductFilterForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success, warning, info, error
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def index_view(request):
    products = Product.objects.all()

    if 'reset' in request.GET:
        if 'sortfilt' in request.session:
            request.session.pop('sortfilt')
        return redirect(reverse('index'))

    settings = request.session.get('sortfilt', {})

    fromsettings = False
    sortorder = request.GET.get('sort', '')
    if len(sortorder) == 0:
        sortorder = settings.get('sort', 'name')
        fromsettings = True
    products = products.order_by(sortorder)
    settings['sort'] = sortorder

    search_form = ProductFilterForm(request.GET)
    # ignore form errors; just get any cleaned data available
    if search_form.is_valid():
        pass

    search_string = search_form.cleaned_data.get('product_search', None)
    if search_string:
        products = products.filter(name__icontains=search_string)
        settings['product_search'] = search_string
    elif 'product_search' in settings:
        val = settings.get('product_search')
        products = products.filter(name__icontains=val)
        fromsettings = True

    min_price = search_form.cleaned_data.get('min_price', None)
    if min_price:
        products = products.filter(price__gte=min_price)
        settings['min_price'] = float(min_price)
    elif 'min_price' in settings:
        val = settings.get('min_price')
        products = products.filter(price__gte=val)
        fromsettings = True

    max_price = search_form.cleaned_data.get('max_price', None)
    if max_price:
        products = products.filter(price__lte=max_price)
        settings['max_price'] = float(max_price)
    elif 'max_price' in settings:
        val = settings.get('max_price')
        products = products.filter(price__lte=val)
        fromsettings = True

    avg_rating = search_form.cleaned_data.get('avg_rating', None)
    if avg_rating:
        products = products.annotate(avgstars=Avg('review__stars')).filter(avgstars__gte=avg_rating)
        settings['avg_rating'] = float(avg_rating)
    elif 'avg_rating' in settings:
        val = settings.get('avg_rating')
        products = products.filter(price__gte=val)
        fromsettings = True

    request.session['sortfilt'] = settings


    if fromsettings:
        url = "{}?{}".format(reverse('index'), urlencode(settings))
        return redirect(url)

    return render(request, "products/index.html", {'products':products, 'search_form':ProductFilterForm(initial=search_form.cleaned_data)})
    # def search_form_helper(search_form, products):
    #     if 'product_search' in search_form:
    #         search_string = search_form['product_search']
    #         products = products.filter(name__icontains=search_string)
    #     if 'max_price' in search_form:
    #         search_string = search_form['max_price']
    #         products = products.filter(price__lte=float(search_string))
    #     if 'min_price' in search_form:
    #         search_string = search_form['min_price']
    #         products = products.filter(price__gte=float(search_string))

    #     return products
    # search_form = ProductFilterForm(request.GET)
    # products = Product.objects.all()

    # print(request.META['QUERY_STRING'])
    



    # # for this form, we don't really care that all the data are valid,
    # # but we do need to call is_valid to force the form object to
    # # put all the form data into the "cleaned_data" dictionary-like
    # # object.   for any form entries that *are* valid, a key will exist
    # # in the cleaned_data dictionary (otherwise, there's no key).
    # if search_form.is_valid():
    #     pass



    # # was 'product_search' filled out in the search form?
    # if not 'reset' in request.GET:

    #     if 'sort' in request.GET:
    #         request.session['sort'] = request.GET['sort']
    #         products = products.order_by(request.GET['sort'])

    #     else:
    #         if 'sort' in request.session:
    #             products = products.order_by(request.session['sort'])



    #     if 'product_search' in search_form.cleaned_data or 'max_price' in search_form.cleaned_data or 'min_price' in search_form.cleaned_data:
    #         for key in search_form.cleaned_data:
    #             if key == 'min_price' or key == 'max_price':
    #                 search_form.cleaned_data[key] = float(search_form.cleaned_data[key])
    #         products, request.session['filter'] = search_form_helper(search_form.cleaned_data, products), search_form.cleaned_data
    #     else:
    #         if 'filter' in request.session:
    #             products = search_form_helper(request.session['filter'], products)


    #     if 'filter' in request.session and 'sort' in request.session:
    #         rest_query = '{}={}&{}={}&{}={}&{}={}'.format('sort', request.session.get('sort', ''), 'product_search', request.session['filter'].get('product_search', ''), 'min_price', request.session['filter'].get('min_price', ''), 'max_price', request.session['filter'].get('max_price', ''))
    #         if request.META['QUERY_STRING'] != rest_query:
    #             return redirect(reverse('index') + '?{}'.format(rest_query))
                
        


    # else:
    #     products = Product.objects.all()
    #     request.session.flush()

    # return render(request, "products/index.html", {'products':products, 'search_form':ProductFilterForm()})    

def details_view(request, id):
    
    product = get_object_or_404(Product, id=id)
    reviews = product.review_set.all()
    count = product.review_set.count()
    return render(request, "products/details.html", {'product':product, 'reviews': reviews, 'count': count})


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect('/products/')
        
    return render_to_response('login.html', context_instance=RequestContext(request))

@login_required
def review_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            product.review_set.create(stars=form.cleaned_data['stars'], review_text=form.cleaned_data['review_text'], user=request.user)
            success(request, "Product review added.")
            return redirect('details', id=product.id) #?
        else:
            error(request, "Review failed to post.")
    else:
        
        form = ReviewForm()
    return render(request, "products/review.html", {'form':form, 'product':product})


