from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

_PROFESIONAL = (
    (0, _("enfermera especialista en geriatria")),
    (1, _("enfermera otros")),
    (2, _("médico general")),   
    (3, _("equipo multidisciplinar")),  
    (4, _("médico residente")),
    (5, _("otros")),
)  

### Proyecto
#         
class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()


    def __str__(self):
        return self.nombre 

    class Meta:
        verbose_name_plural = "Instituciones"

# class CustomUser(AbstractUser):
#     pass
#     # add additional fields in here

#     def __str__(self):
#         return self.username

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, default=True, blank=True, on_delete=models.DO_NOTHING)
    perfil = models.IntegerField(verbose_name = _("Perfil profesional"), choices = _PROFESIONAL, blank= True, null = True) 
    cargo = models.CharField(max_length=255, default='')
    lugar_trabajo = models.CharField(max_length=255, default='')
    
    # avatar = models.ImageField(
    #     upload_to = 'assets/images',
    #     default = 'no-img.jpg',
    #     blank=True
    # )
    # first_name = models.CharField(max_length=255, default='')
    # last_name = models.CharField(max_length=255, default='')
    # email = models.EmailField(default='none@email.com')
    # birth_date = models.DateField(default='1999-12-31')
    # bio = models.TextField(default='')
    # city = models.CharField(max_length=255, default='')
    # state = models.CharField(max_length=255, default='')
    # country = models.CharField(max_length=255, default='')
    # favorite_animal = models.CharField(max_length=255, default='')
    # hobby = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'], institucion_id=1)

post_save.connect(create_profile, sender=User)
