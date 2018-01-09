from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError

from .models import Movimento, Prenda



class MovimentoForm(forms.Form):
    nome_arrematador = forms.CharField(label="Arrematador", max_length=120)
    valor_arremate = forms.FloatField(label="Valor")

    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data', None)
        super(MovimentoForm, self).__init__(*args, **kwargs)




    def clean_valor_arremate(self):
        cleaned_data = super().clean()
        valor_arremate = cleaned_data.get('valor_arremate')

        movimento_anterior = Movimento.objects.filter(prenda_fk=self.data['prenda_id'])
        print(self.data)

        if movimento_anterior:
            print("passou")
            movimento_anterior=movimento_anterior[0]

            if Decimal(valor_arremate) <= movimento_anterior.valor_arremate:
                msg = "Valor do arremate menor do que o valor atual da prenda!"
                raise forms.ValidationError(msg)
        else:
            prenda = Prenda.objects.get(id = self.data['prenda_id'])
            print(prenda)

            if Decimal(valor_arremate) <= prenda.valor_inicial:
                msg = "Valor do arremate menor do que o valor inicial da prenda!"
                raise forms.ValidationError(msg)








