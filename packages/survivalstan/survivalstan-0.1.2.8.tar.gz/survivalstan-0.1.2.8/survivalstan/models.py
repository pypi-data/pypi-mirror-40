from os.path import join as joinpth
import pkg_resources

resource_package = __name__  # Could be any module/package name.

_pem_survival_unstructured_path = joinpth(
    'stan', 'pem_survival_model_unstructured.stan')
_pem_survival_randomwalk_path = joinpth(
    'stan', 'pem_survival_model_randomwalk.stan')
_pem_survival_gamma_path = joinpth('stan',
                                   'pem_survival_model_gamma.stan')
_pem_survival_timevarying_path = joinpth('stan',
                                         'pem_survival_model_tvc.stan')
_weibull_survival_path = joinpth('stan', 'weibull_survival_model.stan')
_exp_survival_path = joinpth('stan', 'exp_survival_model.stan')

# varying-coefs models
_weibull_survival_varcoef_path = joinpth(
    'stan', 'weibull_survival_model_varying_coefs.stan')
_pem_survival_varcoef_path = joinpth(
    'stan', 'pem_survival_model_unstructured_varcoef.stan')

pem_survival_model = pkg_resources.resource_string(
    resource_package, _pem_survival_unstructured_path
    ).decode("utf-8")
pem_survival_model_unstructured = pkg_resources.resource_string(
    resource_package, _pem_survival_unstructured_path).decode("utf-8")
pem_survival_model_randomwalk = pkg_resources.resource_string(
    resource_package, _pem_survival_randomwalk_path).decode("utf-8")
pem_survival_model_gamma = pkg_resources.resource_string(
    resource_package, _pem_survival_gamma_path).decode("utf-8")
pem_survival_model_timevarying = pkg_resources.resource_string(
    resource_package, _pem_survival_timevarying_path).decode("utf-8")
weibull_survival_model = pkg_resources.resource_string(
    resource_package, _weibull_survival_path).decode("utf-8")
exp_survival_model = pkg_resources.resource_string(
    resource_package, _exp_survival_path).decode("utf-8")

# varying-coefs models
pem_survival_model_varying_coefs = pkg_resources.resource_string(
        resource_package, _pem_survival_varcoef_path).decode("utf-8")
weibull_survival_model_varying_coefs = pkg_resources.resource_string(
        resource_package, _weibull_survival_varcoef_path).decode("utf-8")
