from django.contrib.auth.hashers import check_password

from .models import User


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        # 根据邮箱找用户 ，找到了才判断密码
        # 取出email
        email = credentials.get('email', credentials.get('username', None))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            # 校验
            if user.check_password(credentials['password']):
                # 返回用户
                return user


    # 必须要定义get_user
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None