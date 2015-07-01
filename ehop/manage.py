# @copyright (C) 2014-2015
#Developpeurs 'BARDOU AUGUSTIN - BREZILLON ANTOINE - EUZEN DAVID - FRANCOIS SEBASTIEN - JOUNEAU NICOLAS - KIBEYA AISHA - LE CONG SEBASTIEN -
#              MAGREZ VALENTIN - NGASSAM NOUMI PAOLA JOVANY - OUHAMMOUCH SALMA - RIAND MORGAN - TREIMOLEIRO ALEX - TRULLA AURELIEN '
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL version 3

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ehop.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)