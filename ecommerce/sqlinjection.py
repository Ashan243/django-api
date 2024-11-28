from django.db.migrations import RunSQL
from django.db import connection
from django.http import JsonResponse


def create_query(request, item):
    
    query = """
        SELECT * FROM ecommerce_products WHERE id = %s 
    """
    with connection.cursor() as c:
        c.execute(query, [item])
        product_item = c.fetchall()
    return JsonResponse(product_item, safe=False)

class SearchForTwoThings(RunSQL):
    
    def find(request, params1, params2, metatag):
       return f""" IN (SELECT {params1} FROM ecommerce_category WHERE {params2}= {metatag})"""
   
   
   