from users.models import Kinesiologo, Paciente
from users.views import is_kinesiologo, is_paciente


def profile_pic(request):
    if request.user.is_authenticated:
        if is_kinesiologo(request.user):
            profile_obj = Kinesiologo.objects.get(user=request.user)
        else:
            # elif request.user.is_paciente:
            profile_obj = Paciente.objects.get(user=request.user)
        # elif request.user.is_admin:
        pic = profile_obj.profile_pic
        return {'profile_pic': pic}
    else:
        return {}
