from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from comments.models import Comment
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from .serializers import CommentListSerializer, CommentDetailSerializer, create_commet_serializer


class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	#serializer_class = PostCreateUpdateSerializer
	#permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		model_type = self.request.GET.get("type")
		slug = self.request.GET.get("slug")
		parent_id = self.request.GET.get("parent_id", None)

		return create_commet_serializer(
			model_type=model_type,
			slug=slug,
			parent_id=parent_id,
			user=self.request.user
			)

	# def perform_create(self, serializer):
	# 	serializer.save(user=self.request.user)

class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	permission_classes = [IsOwnerOrReadOnly]
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	lookup_field = 'slug'
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 	def perform_update(self, serializer):
# 		serializer.save(user=self.request.user)

# class PostDeteleAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = 'slug'
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentListAPIView(ListAPIView):
	serializer_class = CommentListSerializer
	#permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['comment_text', 'user__first_name']
	pagination_class = PostPageNumberPagination #PostLimitOffsetPagination
	
	def get_queryset(self, *args, **kwargs):
		queryset_list = Comment.objects.filter(id__gte=0)
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(comment_text__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
			).distinct()
		return queryset_list
