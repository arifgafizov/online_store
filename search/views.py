import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from products.documents import ProductDocument
from products.models import Product
from products.paginations import ProductPageNumberPagination
from products.serializers import ProductSearchSerializer


class PaginatedElasticSearchAPIView(GenericAPIView):
    serializer_class = None
    document_class = None
    permission_classes = [AllowAny]
    pagination_class = ProductPageNumberPagination

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class SearchProducts(PaginatedElasticSearchAPIView):
    queryset = Product.available_objects.all()
    serializer_class = ProductSearchSerializer
    document_class = ProductDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'title',
                    'description',
                ], fuzziness='auto')
