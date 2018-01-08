from django import forms



class MovimentoForm(forms.Form):
    nome_arrematador = forms.CharField(label="Arrematador", max_length=120)
    valor_arremate = forms.FloatField(label="Valor")




