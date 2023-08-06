"""
lmrob
======

"""


from .lmrob import *
from .lmrob import _psi_conv_cc, _psi2ipsi, _regularize_Mpsi, _convSS, _Mpsi, _lmrob_hat, _vcov_avar1, _vcov_w
from ._rinterface import initr
from .situation import (r_home_from_subprocess,
                        r_home_from_registry,
                        get_r_home, 
                        assert_python_version)


R_HOME = get_r_home()
if not os.environ.get("R_HOME"):
    os.environ['R_HOME'] = R_HOME

initr()



