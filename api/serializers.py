from rest_framework import serializers

from api import models


class UserGroupSerializer(serializers.Serializer):
    # title = serializers.CharField(error_messages={'required': "标题不能为空"}, validators=[XXXValidator("验证"),])  # 要求带参数
    title = serializers.CharField(error_messages={'required': "title值不能为空"})  # 要求带参数 title
    email = serializers.EmailField(error_messages={'required': "请输入邮件", 'invalid': "email值不规范！！"})

    # "required:该请求需要带该参数， invalid：是否符合规范的数据"

    def validate(self, attrs):
        return attrs

    def validate_title(self, title):
        # if not self.data.get('titile').startswith("科大讯飞"):
        if not title.startswith("科大讯飞"):
            msg = "必须以'{}'开头".format('科大讯飞')
            raise serializers.ValidationError(msg)
        return title


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    # group = serializers.HyperlinkedIdentityField(view_name="group_view", lookup_field='group_id', lookup_url_kwarg='pk')
    # group = serializers.PrimaryKeyRelatedField()
    # roles = serializers.PrimaryKeyRelatedField()
    # Hyperlinked需要在实例化时添加context={'request': request}
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        # read_only_fields = ('group', 'role')
        depth = 2

    def validate(self, attrs):
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    class Meta:
        model = models.Role
        fields = '__all__'
