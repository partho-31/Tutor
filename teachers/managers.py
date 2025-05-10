from django.contrib.auth.models import UserManager

class CustomTeacherManager(UserManager):
    def create(self,email,password,**kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        if not extra_fields.get('superuser'):
            raise ValueError('Superuser must have is_superuser = True')

        return self.create(email, password, **extra_fields)