from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ToDo
from .serializers import ToDoSerializer


class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = ToDo.objects.filter(user=request.user.id)
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'due': request.data.get('due'),
            'completed': request.data.get('completed'),
            'user': request.data.get('user'),
        }
        serializer = ToDoSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
