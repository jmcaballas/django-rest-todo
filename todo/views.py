from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ToDo
from .serializers import ToDoSerializer


class ToDoList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = ToDo.objects.filter(user=request.user.id)
        headers = {}
        headers['X-Total-Count'] = len(todos)
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data, headers=headers, status=status.HTTP_200_OK)

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


class ToDoDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        try:
            return ToDo.objects.get(id=todo_id, user=user_id)
        except ToDo.DoesNotExist:
            return none

    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ToDoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'due': request.data.get('due'),
            'completed': request.data.get('completed'),
            'user': request.data.get('user'),
        }
        serializer = ToDoSerializer(instance=todo_instance, data=data)
        
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        serializer = ToDoSerializer(instance=todo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        todo_instance.delete()
        
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )
