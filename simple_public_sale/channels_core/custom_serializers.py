from django.core.serializers.json import DjangoJSONEncoder

# from core.models import TipoPrenda as tipo
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        print(obj)
        if isinstance(obj, str):
            print(obj)
            return str(obj)
        return super().default(obj)