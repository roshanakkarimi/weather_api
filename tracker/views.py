from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Project, Ticket, Comment
from .serializers import ProjectSerializer, TicketSerializer, CommentSerializer
from .permissions import IsProjectMember

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name","description"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title","description"]
    queryset = Ticket.objects.all()

    def get_queryset(self):
        qs = Ticket.objects.select_related("project","assignee","reporter").prefetch_related("comments")
        project_id = self.request.query_params.get("project")
        status = self.request.query_params.get("status")
        if project_id: qs = qs.filter(project_id=project_id)
        if status: qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=False, methods=["get"])
    def mine(self, request):
        qs = self.get_queryset().filter(Q(assignee=request.user) | Q(reporter=request.user))
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page, many=True)
        return self.get_paginated_response(ser.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]
    queryset = Comment.objects.all()

    def get_queryset(self):
        return Comment.objects.select_related("ticket","author")
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)