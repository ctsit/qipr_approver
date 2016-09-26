from django.http import JsonResponse, HttpResponse

def tags(request):
    if request.method == 'POST':
        #Get the string passed back and search for the right data
        postedValue = request.POST.get('tagString')
        return HttpResponse("Hello post " + postedValue) 
    else:
         return HttpResponse("Hello Get")
