from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext

from django.http import HttpResponse as hr
from django.shortcuts import render
from .models import myProduct, Contact, Orders, OrderUpdate
import math
import json
from .paytm import checksum

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


def index(request):

    allProds = []
    catprods = myProduct.objects.values('category', 'id')
   # print(catprods)
    cats = {item['category'] for item in catprods}
    #print(cats)
    for cat in cats:
        prod = myProduct.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + math.ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nslides), nslides])

   # params = {'tot_slides': nslides, 'range': range(1, nslides), 'product': products}
    #allprods = [[products, range(1, nslides), nslides], [products, range(1, nslides), nslides]]
    params = {'allprods': allProds}

    return render(request, 'shop/index.html', params)

def matchQuery(query, item):
    if query in item.description.lower() or query in item.name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = myProduct.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodTemp = myProduct.objects.filter(category=cat)
        prod = [item for item in prodTemp if matchQuery(query, item)]
        n = len(prod)
        if n!= 0:
            nslides = n // 4 + math.ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nslides), nslides])

    # params = {'tot_slides': nslides, 'range': range(1, nslides), 'product': products}
    # allprods = [[products, range(1, nslides), nslides], [products, range(1, nslides), nslides]]
    params = {'allprods': allProds}

    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        print("posted")
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        query = request.POST.get('query')
        new_contact = Contact(c_name=name, c_email=email, c_phone=phone, c_query=query)
        new_contact.save()
    return render(request, 'shop/contact.html')


def track(request):
    if request.method == 'POST':
        orderId = request.POST.get('order_id')
        email = request.POST.get('email')
        print(orderId, email)
        try:
            orders = Orders.objects.filter(order_id=orderId, o_email=email)

            if(len(orders)>0):
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,orders[0].items_json], default=str)
                print(response)
                return hr(response)

            else:
                return hr("{}")
        except Exception as e:
            print(f"Exception {e}")
            return hr('{}')
    return render(request, 'shop/track.html')

def product(request, id):
    prod = myProduct.objects.filter(id=id)
    print(prod)
    return render(request, 'shop/product.html', {'product': prod[0]})

def checkOut(request):
    if request.method == 'POST':
        print("posted")
        thank = True
        item_json = request.POST.get('item_json')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('add1') + " " + request.POST.get('add2')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        order = Orders(items_json=item_json, amount=amount, o_name=name, o_email=email, o_address=address, o_city=city, o_state=state, o_zip=zip_code, o_phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="your order has been placed")
        update.save()
        o_id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'o_id': o_id})
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(o_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handleRequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict })
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handleRequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            check = form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, check)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful!')
        else:
            print('order unsuccessful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentStatus.html', {'response': response_dict})