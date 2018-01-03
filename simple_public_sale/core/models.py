from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from channels_core.models import GrupoEvento
from core.utils import send_to_evento


class Doador(models.Model):
    nome_doador = models.CharField(max_length=100)
    apelido_doador = models.CharField(max_length=100)
    cpf_cnpj_doador = models.CharField(max_length=14)
    
class Evento(models.Model):
    nome_evento = models.CharField(max_length=100)
    data_evento = models.DateTimeField(null=True,blank=True)
    url_image = models.ImageField(upload_to='imagens')
    grupo = models.OneToOneField(GrupoEvento, null=True, blank=True, on_delete=models.CASCADE)

    def is_online(self):
        return self.grupo.online
    
class TipoPrenda(models.Model):
    descricao = models.CharField(max_length=100)
    url_image = models.ImageField(upload_to='tipos/imagens',null=True,blank=True)

class Caracteristica(models.Model):
    caracteristica = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)

class Prenda(models.Model):
    doador_fk = models.ForeignKey(Doador, on_delete=models.CASCADE)
    valor_inicial = models.DecimalField(decimal_places=2, max_digits=4)
    tipo_prenda_fk = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento_fk = models.ForeignKey(Evento, on_delete=models.CASCADE)
    arrematada = models.BooleanField(default=False)
    caracteristicas = models.ManyToManyField(Caracteristica,through='CaracteristicaPrenda')

class CaracteristicaPrenda(models.Model):
    prenda = models.ForeignKey(Prenda,on_delete=models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica,on_delete=models.CASCADE)
    valor = models.CharField(max_length=100)

class Arrematador(models.Model):
    nome_arrematador = models.CharField(max_length=100,unique=True,db_index=True)
    cpf_cnpj_arrematador = models.CharField(max_length=14,null=True,blank=True)
    rg_arrematador = models.CharField(max_length=50,null=True,blank=True)
    endereco_arrematador = models.CharField(max_length=200,null=True,blank=True)
    
class Movimento(models.Model):
    data_movimento = models.DateField(auto_now=True,editable=False)
    arrematador_fk = models.ForeignKey(Arrematador, on_delete=models.CASCADE)
    valor_arremate = models.DecimalField(decimal_places=2, max_digits=4)
    prenda_fk = models.ForeignKey('Prenda', on_delete=models.CASCADE)
    def send_to_stream(self):
        if self.prenda_fk.evento_fk.is_online():
            prenda = self.prenda_fk
            send_to_evento(prenda=prenda)
            print("Stream Atualizada")
        else:
            print("Stream Offline")
        return False


@receiver(post_save, sender=Movimento)
def post_save_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)

    instance.send_to_stream()


@receiver(pre_delete, sender=Movimento)
def pre_delete_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)
    instance.send_to_stream()
