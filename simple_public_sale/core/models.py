from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Max
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from twisted.protocols.amp import Decimal

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
    def total_pagar_evento(self,evento_id):
        prendas=Prenda.objects.filter(arrematador=self,evento__pk=evento_id)
        total=0
        for prenda in prendas:
            total+=prenda.get_movimento_arremate().valor
        print(total)
        return total
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
    valor_inicial = models.DecimalField(decimal_places=2, max_digits=8,default=0)
    tipo_prenda = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    # arrematada = models.BooleanField(default=False)
    arrematador = models.ForeignKey(Participante,on_delete=models.CASCADE,related_name="arrematador",null=True,blank=True,default=True)
    url_image = models.ImageField(upload_to='prendas/imagens', null=True, blank=True)
    parent = models.OneToOneField('Prenda', on_delete=models.CASCADE, blank=True, null=True,verbose_name='Doação de')
    caracteristicas = models.ManyToManyField(Caracteristica,through='CaracteristicaPrenda')
    def __str__(self):
        return '%s [doado por: %s]'%(self.tipo_prenda.nome,self.doador.apelido)
    
    def get_prenda_clone(self):

        if not self.arrematador:
            raise ValidationError("Esta Prenda ainda nao foi arrematada")


        prenda = Prenda()


        prenda.doador = self.get_arrematador()
        prenda.valor_inicial = self.valor_inicial
        prenda.evento = self.evento
        prenda.tipo_prenda = self.tipo_prenda
        prenda.url_image = self.url_image
        prenda.arrematador = None
        prenda.parent=self
        prenda.save()


        for caracteristica_prenda in self.caracteristicaprenda_set.all():
            new_caracteristica_prenda=copy.copy(caracteristica_prenda)
            new_caracteristica_prenda.pk=None
            new_caracteristica_prenda.prenda_id=prenda.id
            new_caracteristica_prenda.save()

        return prenda

    def get_arrematador(self):
        movimentos=self.movimento_set.all()
        if self.arrematador and movimentos:
            print("oioi")
            return movimentos.order_by('-valor').first().arrematador

        return None
    def get_arrematador_atual(self):
        movimentos=self.movimento_set.all()
        if movimentos:
            print("oioi")
            return movimentos.order_by('-valor').first().arrematador

        return None
    def is_doada(self):
        return Prenda.objects.filter(parent=self).count()

    def get_movimento_arremate(self):
        if self.arrematador:

            return self.movimento_set.all().order_by('-valor').first()

        return None
    def get_maior_movimento(self):
        movimentos=self.movimento_set.all()
        if movimentos:

            return movimentos.order_by('-valor').first()
        return None
    def last_three_movements(self):
        return self.movimento_set.all().order_by("-data_ocorrencia", "-valor")[0:3]
    def get_doador_primario(self):
        doador_primario=None
        prenda = self
        while(True):
            if prenda.parent==None:
                return prenda.doador

            prenda=prenda.parent
    def get_caracteristicas_json(self):
        caracteristicas=[]
        for caracteristica in self.caracteristicaprenda_set.all():
            valor=caracteristica.valor
            chave = caracteristica.caracteristica.caracteristica
            caracteristica = {"caracteristica":chave,"valor":valor}
            caracteristicas.append(caracteristica)

        return caracteristicas
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

@receiver(pre_save, sender=Evento)
def post_save_evento(sender,instance, **kwargs):
    assert isinstance(instance, Evento)
    if not instance.grupo:
        grupo=GrupoEvento()
        grupo.nome = instance.nome
        grupo.evento=instance
        grupo.online=True
        grupo.save()
        print(grupo)
        instance.grupo=grupo


@receiver(pre_save, sender=Movimento)
def pre_save_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)

    if instance.prenda.arrematador:
        raise ValidationError("Não é possível enviar mais lances, esta prenda já foi arrematada.")

    maior_movimento= instance.prenda.get_maior_movimento()
    if maior_movimento and float(instance.valor) <= float(maior_movimento.valor):
        raise ValidationError("Este lance é menor que o maior lance atual!")

@receiver(post_save, sender=Movimento)
def post_save_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)

    instance.send_to_stream()

@receiver(post_delete, sender=Movimento)
def pre_delete_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)
    if instance.prenda.arrematador:
        raise ValidationError("Não é possível remover lances de uma prenda arrematada.")

@receiver(post_delete, sender=Movimento)
def post_delete_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)
    instance.send_to_stream()

# @receiver(pre_save, sender=Prenda)
# def pre_delete_movimento(sender,instance, **kwargs):
#     assert isinstance(instance, Prenda)
#     if instance.parent.is_doada():
#         raise ValidationError("Esta Prenda ja foi doada anteriormente2")
@receiver(pre_save, sender=Participante)
def pre_save_arrematador(sender,instance, **kwargs):
    assert isinstance(instance, Participante)
    instance.apelido=instance.apelido.upper()

@receiver(pre_save, sender=CaracteristicaPrenda)
def pre_save_caracteristica_prenda(sender,instance, **kwargs):
    assert isinstance(instance, CaracteristicaPrenda)
    if(instance.prenda.caracteristicaprenda_set.count()>=3):
        raise IntegrityError("Cada prenda tem um limite de 3 caracteristicas.")

@receiver(pre_save, sender=Prenda)
def pre_save_prenda(sender,instance, **kwargs):
    assert isinstance(instance, Prenda)
    if instance.parent:
        print(instance.parent.arrematador)
        if not instance.parent.arrematador:
            raise ValidationError("Uma prenda doada precisa vir de outra arrematada.")


    if not instance.arrematador and Prenda.objects.filter(parent=instance) and instance.pk:

        raise ValidationError("Esta prenda foi doada, para desfazer o arremate é necessário primeiro desfazer a doação.")

    if instance.arrematador and not instance.movimento_set.all():
        raise ValidationError(
            "Esta prenda não possui nenhum lance.")

    if instance.movimento_set.all():

        instance.movimento_set.first().send_to_stream()