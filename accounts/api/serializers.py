from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError, EmailField, CharField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
		]

class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')
	email2 = EmailField(label='Confirm Email')
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]
		extra_kwargs = {"password": {"write_only": True}}
	
	def validate(self, data):
		return data

	def validate_email2(self, value):
		data = self.get_initial()
		email1 = data.get("email")
		email2 = value
		if email1 != email2:
			raise ValidationError("Email must match")

		user_qs = User.objects.filter(email=email1)
		if user_qs.exists():
			raise ValidationError("Email already exists")

		return value

	def create(self, validated_data):
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]
		user_obj = User(
			username = username,
			email = email
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

class UserLoginSerializer(ModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	username = CharField(required=False, allow_blank=True)
	# email = EmailField(label='Confirm Email', required=False, allow_blank=True)
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'token',
		]
		extra_kwargs = {"password": {"write_only": True}}
	
	def validate(self, data):
		user_obj = None
		username = data.get("username", None)
		password = data["password"]
		if not username:
			raise ValidationError("A username is required for login")

		user = User.objects.filter(
				Q(username=username)
			).distinct()

		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			return ValidationError("This username not exists")

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again.")

		data["token"] = "Some random token"
		return data