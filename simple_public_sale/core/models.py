from django.db import models, IntegrityError
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from channels_core.models import GrupoEvento
from core.utils import send_to_evento

import copy
# class Doador(models.Model):
#     nome_doador = models.CharField(max_length=100)
#     apelido_doador = models.CharField(max_length=100)
#     cpf_cnpj_doador = models.CharField(max_length=14)
#     def __str__(self):
#         return self.nome_doador
class ParticipanteManager(models.Manager):
    def get_by_natural_key(self, apelido):
        return self.get(nome=apelido)

class Participante(models.Model):
    apelido = models.CharField(max_length=100,null=True,blank=True,unique=True,db_index=True)
    nome = models.CharField(max_length=100,null=True,blank=True)
    cpf_cnpj = models.CharField(max_length=14,null=True,blank=True)
    rg = models.CharField(max_length=50,null=True,blank=True)
    endereco = models.CharField(max_length=200,null=True,blank=True)

    objects=ParticipanteManager()
    def __str__(self):
        return self.apelido

    def natural_key(self):
        return (self.apelido)

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateTimeField(null=True,blank=True)
    url_image = models.ImageField(upload_to='imagens')
    grupo = models.OneToOneField(GrupoEvento, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome
    def is_online(self):
        return self.grupo.online
    
class TipoPrenda(models.Model):
    nome = models.CharField(max_length=100,default='',null=True,blank=True)
    descricao = models.CharField(max_length=100)
    url_image = models.ImageField(upload_to='tipos/imagens',null=True,blank=True)
    def __str__(self):
        return self.nome

class Caracteristica(models.Model):
    caracteristica = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)
    def __str__(self):
        return self.caracteristica

class Prenda(models.Model):
    doador = models.ForeignKey(Participante, on_delete=models.CASCADE)
    valor_inicial = models.DecimalField(decimal_places=2, max_digits=8)
    tipo_prenda = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    arrematada = models.BooleanField(default=False)

    url_image = models.ImageField(upload_to='prendas/imagens', null=True, blank=True)
    parent = models.ForeignKey('Prenda', on_delete=models.CASCADE, blank=True, null=True)
    caracteristicas = models.ManyToManyField(Caracteristica,through='CaracteristicaPrenda')

    def __str__(self):
        return self.tipo_prenda.nome
    def get_prenda_clone(self):
        prenda = copy.copy(self)
        # prenda.pk=None
        prenda.doador = self.get_arrematador()
        prenda.parent=self
        prenda.pk=None
        prenda.arrematada = False
        prenda.save()
        for caracteristica_prenda in self.caracteristicaprenda_set.all():
            new_caracteristica_prenda=copy.copy(caracteristica_prenda)
            new_caracteristica_prenda.pk=None
            new_caracteristica_prenda.prenda_id=prenda.id
            new_caracteristica_prenda.save()

    def get_arrematador(self):
        if self.arrematada:
            print("oioi")
            return self.movimento_set.all().order_by('-valor').first().arrematador

        raise IntegrityError("Esta prenda ainda nao foi arrematada")
    def last_three_movements(self):
        return self.movimento_set.all().order_by("-data_ocorrencia", "-valor")[0:3]

class CaracteristicaPrenda(models.Model):
    prenda = models.ForeignKey(Prenda,on_delete=models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica,on_delete=models.CASCADE)
    valor = models.CharField(max_length=100)
    class Meta:
        unique_together=('prenda','caracteristica')
    def __str__(self):
        return "%s - %s"%(self.caracteristica.caracteristica, self.prenda.tipo_prenda.nome)

class Movimento(models.Model):
    data_ocorrencia = models.DateField(auto_now=True,editable=False)
    arrematador = models.ForeignKey(Participante, on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=8)
    prenda = models.ForeignKey('Prenda', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s : R$ %s"%(self.arrematador.apelido,self.prenda.tipo_prenda.nome,self.valor)
    def send_to_stream(self):
        if self.prenda.evento.is_online():
            prenda = self.prenda
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

@receiver(pre_save, sender=Participante)
def pre_save_arrematador(sender,instance, **kwargs):
    assert isinstance(instance, Participante)
    instance.apelido=instance.apelido.upper()

@receiver(pre_save, sender=CaracteristicaPrenda)
def pre_save_caracteristica_prenda(sender,instance, **kwargs):
    assert isinstance(instance, CaracteristicaPrenda)
    if(instance.prenda.caracteristicaprenda_set.count()>=3):
        raise IntegrityError("Cada prenda tem um limite de 3 caracteristicas.")
