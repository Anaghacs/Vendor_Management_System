from rest_framework.decorators import api_view
from rest_framework.response import Response


# www.example.com/api/index

@api_view(['GET'])
def index(request):
      vendors_details = {
            'name' : 'Anagha',
            'age' : 23,
            'job' : 'software engineer'
      }

      return Response(vendors_details)
