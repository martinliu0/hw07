from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages import info, warning, success
from .models import Product
from .forms import ProductFilterForm

def index_view(request):

    search_form = ProductFilterForm(request.GET)
    products = Product.objects.all()

    print(request.META['QUERY_STRING'])
    



    # for this form, we don't really care that all the data are valid,
    # but we do need to call is_valid to force the form object to
    # put all the form data into the "cleaned_data" dictionary-like
    # object.   for any form entries that *are* valid, a key will exist
    # in the cleaned_data dictionary (otherwise, there's no key).
    if search_form.is_valid():
        pass



    # was 'product_search' filled out in the search form?
    if not 'reset' in request.GET:

        if 'sort' in request.GET:
            request.session['sort'] = request.GET['sort']
            products = products.order_by(request.GET['sort'])

        else:
            if 'sort' in request.session:
                products = products.order_by(request.session['sort'])



        if 'product_search' in search_form.cleaned_data or 'max_price' in search_form.cleaned_data or 'min_price' in search_form.cleaned_data:
            for key in search_form.cleaned_data:
                if key == 'min_price' or key == 'max_price':
                    search_form.cleaned_data[key] = float(search_form.cleaned_data[key])
            products, request.session['filter'] = search_form_helper(search_form.cleaned_data, products), search_form.cleaned_data
        else:
            if 'filter' in request.session:
                products = search_form_helper(request.session['filter'], products)


        # if 'filter' in request.session and 'sort' in request.session:
        #     rest_query = '{}={}&{}={}&{}={}&{}={}'.format('sort', request.session.get('sort', ''), 'product_search', request.session['filter'].get('product_search', ''), 'min_price', request.session['filter'].get('min_price', ''), 'max_price', request.session['filter'].get('max_price', ''))
        #     if request.META['QUERY_STRING'] != rest_query:
        #         return redirect('index', kwargs = {"abcd": rest_query})
                
        


    else:
        products = Product.objects.all()
        request.session.flush()

    return render(request, "products/index.html", {'products':products, 'search_form':ProductFilterForm()})    


def search_form_helper(search_form, products):
    if 'product_search' in search_form:
        search_string = search_form['product_search']
        products = products.filter(name__icontains=search_string)
    if 'max_price' in search_form:
        search_string = search_form['max_price']
        products = products.filter(price__lte=float(search_string))
    if 'min_price' in search_form:
        search_string = search_form['min_price']
        products = products.filter(price__gte=float(search_string))

    return products