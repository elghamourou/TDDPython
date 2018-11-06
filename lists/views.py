from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item
# Create your views here.


def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/')


    items = Item.objects.all()
    items2 = []
    for i, item in enumerate(items):
        items2.append([i+1, item])
    return render(request, 'home.html',{'items':items2})