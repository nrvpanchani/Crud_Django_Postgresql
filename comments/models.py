from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your models here.

class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = instance.id
		qs = super(CommentManager, self).filter(content_type=content_type, object_id= object_id).filter(parent=None)
		return qs

	def create_by_model_type(self, model_type, slug, comment_text, user, parent_obj=None):
		model_qs = ContentType.objects.filter(model=model_type)
		if model_qs.exists():
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(slug=slug)
			if obj_qs.exists() and obj_qs.count() == 1:
				instance = self.model()
				instance.comment_text = comment_text
				instance.user = user
				instance.content_type = model_qs.first()
				instance.object_id = obj_qs.first().id
				if parent_obj:
					instance.parent = parent_obj
				instance.save()
				return instance
		return None

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
	comment_text = models.TextField()
	comment_at = models.DateTimeField(auto_now_add=True)

	objects = CommentManager()

	class Meta:
		ordering = ["-comment_at"]

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("thread", kwargs={"id":self.id})

	def get_delete_url(self):
		return reverse("delete", kwargs={"id":self.id})

	def children(self):#replies
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True
	


