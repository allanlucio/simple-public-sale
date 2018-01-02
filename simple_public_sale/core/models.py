from django.db import models

from channels_core.models import GrupoEvento


class Doador(models.Model):
    nome_doador = models.CharField(max_length=100)
    apelido_doador = models.CharField(max_length=100)
    cpf_cnpj_doador = models.CharField(max_length=14)
    
class Evento(models.Model):
    nome_evento = models.CharField(max_length=100)
    data_evento = models.DateField()
    url_image = models.ImageField(upload_to='imagens')
    grupo = models.OneToOneField(GrupoEvento, null=True, blank=True, on_delete=models.CASCADE)
    
class TipoPrenda(models.Model):
    descricao = models.CharField(max_length=100)
    url_image = models.ImageField(upload_to='tipos/imagens',null=True,blank=True)
class Prenda(models.Model):
    doador_fk = models.ForeignKey(Doador, on_delete=models.CASCADE)
    valor_inicial = models.DecimalField(decimal_places=2, max_digits=4)
    tipo_prenda_fk = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento_fk = models.ForeignKey(Evento, on_delete=models.CASCADE)
    arrematada = models.BooleanField(default=False)

    
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