from django.http import JsonResponse, HttpResponse

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
         return HttpResponse("Hello post")
    else:
         return HttpResponse("Hello Get")
