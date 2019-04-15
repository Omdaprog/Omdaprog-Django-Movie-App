from django.shortcuts import render ,redirect
from django.contrib import messages
from airtable.airtable import Airtable
import os

AT = Airtable('apppzWhomfy2IdWfl',
              'Movies',
              api_key='keyJZjCM7eJRvrdPE')



# Create your views here.

def home_page(request):
    user_query = (str(request.GET.get('username', '')))
    search_result = AT.get_all(formula="FIND('"+user_query.lower() + "', LOWER({Name}))")
    stuff_for_frentend = {'search_result': search_result}
    return render(request, 'movie_app/movie_stuff.html', stuff_for_frentend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        response = AT.insert(data)
        messages.success(request, 'New movie added: {}'.format(response['fields'].get('Name')))
    return redirect('/')


def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        response = AT.update(movie_id, data)
        messages.success(request, 'Updated movie: {}'.format(response['fields'].get('Name')))
    return redirect('/')


def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, 'Deleted movie: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request,'Get an error when trying to delete a movie: {}'.format(e))    
    return redirect('/')





