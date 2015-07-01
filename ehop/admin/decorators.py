# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def staff_member_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/connexion/'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    return user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )(view_func)
