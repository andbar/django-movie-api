from django.forms import modelform_factory
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from movie.models import Movie
import json
# Create your views here.

@csrf_exempt
def api_movie_list_create(request):
    if request.POST:
        title = request.POST.get("title")
        Movie.objects.create(title=title)
        return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
    all_movies = Movie.objects.all()
    data = [{"title": movie.title, "id": movie.id} for movie in all_movies]
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def api_movie_detail(request, pk):
    if request.method == 'DELETE':
        Movie.objects.get(id=pk).delete()
        return HttpResponse(json.dumps({"message": "Delete Successful"}), content_type="application/json")
    elif request.method == 'PUT':
        movie = Movie.objects.get(id=pk)
        body = QueryDict(request.body)
        title = body.get('title')
        movie.title = title
        movie.save()
        return HttpResponse(json.dumps({"message": "Update Successful"}), content_type="application/json")
    movie = Movie.objects.get(id=pk)
    serialized_movie = json.dumps({"id": movie.id, "title": movie.title})
    return HttpResponse(serialized_movie, content_type="application/json")

