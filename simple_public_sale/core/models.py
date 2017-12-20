from django.db import models

class Doador(models.Model):
    nome_doador = models.CharField(max_length=100)
    apelido_doador = models.CharField(max_length=100)
    cpf_cnpj_doador = models.CharField(max_length=14)
    
class Evento(models.Model):
    nome_evento = models.CharField(max_length=100)
    data_evento = models.DateField()
    url_image = models.ImageField(upload_to='arquivos/imagens')
    
class TipoPrenda(models.Model):
    descricao = models.CharField(max_length=100)

class Prenda(models.Model):
    doador_fk = models.ForeignKey(Doador, on_delete=models.CASCADE)
    valor_inicial = models.DecimalField(decimal_places=2)
    tipo_prenda_fk = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento_fk = models.ForeignKey(Evento, on_delete=models.CASCADE)
    movimento_fk = models.OneToOneField('Movimento', on_delete=models.CASCADE)
    
class Arrematador(models.Model):
    nome_arrematador = models.CharField(max_length=100)
    cpf_cnpj_arrematador = models.CharField(max_length=14)
    rg_arrematador = models.CharField(max_length=50)
    endereco_arrematador = models.CharField(max_length=200)
    
class Movimento(models.Model):
    data_movimento = models.DateField()
    arrematador_fk = models.ForeignKey(Arrematador, on_delete=models.CASCADE)
    valor_arremate = models.DecimalField(decimal_places=2)
