from django.core.paginator import Paginator
from django.http import JsonResponse
import psycopg2.extras


def respond_with_custom_pagination(request):
	
	API_CONN = psycopg2.connect(database="server", user="postgres", password="postgres", host="127.0.0.1", port="5432")
	API_CURSOR = API_CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
	
	data = fetchDetailsWithoutJoin(API_CONN, API_CURSOR, 'users')
	
	total_length = len(data)	
	
	items = request.GET['items']
	page = request.GET['page']

	valid_page = total_length/int(items)
	
	if valid_page < int(page):
		page = 1

	if int(items) <= 0:
		items = 10
	
	if int(page) <= 0:
		page = 1	 
	
	pages_possible = total_length/int(page)
	
	if not pages_possible:
		page = 1 	

	url = 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + '?'

	meta = {}
	meta['total'] = total_length
	meta['count'] = total_length
	meta['current_page'] = page
	meta['per_page'] = items
	meta['next_link'] = ''
	meta['previous_link'] = ''

	paginator = Paginator(data, items)
	results = paginator.page(page)

	if results.has_next():
		if (total_length - int(items)) < int(items):
			new_items = total_length - int(items)
		else:
			new_items = items	
		new_page = int(page) + 1
		next_link =  url + 'items' + '=' + str(new_items) + '&' + 'page' + '=' + str(new_page)
		meta['next_link'] = next_link
	
	if results.has_previous:
		page = int(page) - 1
		if not page:
			page = 1
		previous_link =  url + 'items' + '=' + str(items) + '&' + 'page' + '=' + str(page)
		meta['previous_link'] = previous_link

	results = results.object_list

	response = {}
	response['data'] = results	
	response['meta'] = meta

	return JsonResponse(response)



def fetchDetailsWithoutJoin(connection, cursor, tableName, params=None):
    # cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if params:
        fields = ', '.join(params.keys())
        values = ', '.join(['%%(%s)s' % x for x in params])
        query = 'SELECT * FROM %s WHERE (%s)=(%s)' %(tableName, fields, values)
    else:
        query = 'SELECT * FROM %s ' %(tableName)
    cursor.execute(query, params)
    connection.commit()
    return bind_column_name_with_data(cursor.fetchall())

def bind_column_name_with_data(data):
        result = []
        if len(data) == 1:
            return dict(data[0])
        for row in data:
            result.append(dict(row))
        return result