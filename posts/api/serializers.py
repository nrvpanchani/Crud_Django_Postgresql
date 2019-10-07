from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentListSerializer, CommentSerializer
from comments.models import Comment
from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
	user = UserDetailSerializer()
	class Meta:
		model = Post
		fields = [
			'user',
			'title',
			'content',
			'publish',
		]
detail_url = HyperlinkedIdentityField(
		view_name='posts-api:detail',
		lookup_field='slug'
		)
class PostListSerializer(ModelSerializer):
	url = detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'slug',
			'title',
			'content',
			'publish',
			'image',
			'user',
		]
	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None

		return image

class PostDetailSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'slug',
			'content',
			'image',
			'publish',
			'user',
			'comments',
		]

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None

		return image

	def get_comments(self, obj):
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentSerializer(c_qs, many=True).data
		return comments