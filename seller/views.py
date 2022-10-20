from django.shortcuts import render

# Create your views here.
# Create your views here.
def seller_index(request):
    return render(request, template_name="seller.html")
