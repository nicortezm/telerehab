from users.models import Kinesiologo, Paciente
from users.views import is_kinesiologo, is_paciente


def profile_pic(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if is_kinesiologo(request.user):
                profile_obj = Kinesiologo.objects.get(user=request.user)
            # elif is_paciente(request.user):
            else:
                profile_obj = Paciente.objects.get(user=request.user)

            if profile_obj.profile_pic:
                pic = profile_obj.profile_pic
            else:
                pic = {}
        else:
            pic = {}
        return {'profile_pic': pic}
    else:
        return {}
