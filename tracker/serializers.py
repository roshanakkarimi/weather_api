from rest_framework import serializers
from .models import Project, Ticket, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Comment
        fields = ["id","author","author_name","body","created_at","ticket"]
        read_only_fields = ["id","created_at"]

class TicketSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["id","created_at","updated_at","reporter"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["id","created_at","owner"]