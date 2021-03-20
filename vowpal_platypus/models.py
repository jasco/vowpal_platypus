from vw import VW

def vw_model(model_params, node=False):
    params = model_params.copy()
    if node is not False:
        assert params.get('cores'), '`cores` parameter must specify the total number of cores to make a multi-core model.'
        if params.get('machines') and params.get('machines') > 1:
            assert params.get('machine_number'), '`machine_number` parameter must be set to track which machine each model runs on.'
            assert params.get('master_ip'), '`master_ip` parameter must be set to track which network to connect to.'
            machine_number = params['machine_number']
            multicore_params = {
                'total': params['cores'] * params['machines'],
                'node': params['machine_number'] * params['cores'] + node,
                'holdout_off': True,
                'span_server': params['master_ip']
            }
        else:
            multicore_params = {
                'total': params['cores'],
                'node': node,
                'holdout_off': True,
                'span_server': 'localhost'
            }
        params.update(multicore_params)
        if not params.get('unique_id'):
            params['unique_id'] = 0
    params_to_delete = ['master_ip', 'machines', 'cores', 'machine_number']
    [params.pop(p) for p in params_to_delete if params.get(p) is not None]
    params = {k: v for k, v in params.items() if v is not None}
    return VW(params)

def model(model_params):
    cores = model_params.get('cores')
    if cores is not None and cores > 1:
        return [vw_model(model_params, node=n) for n in range(cores)]
    else:
        return vw_model(model_params)

def linear_regression(**model_params):
    return model(model_params)

def als(**model_params):
    return model(model_params)

def logistic_regression(**model_params):
    model_params.update({'link': 'logistic', 'loss': 'logistic'})
    return model(model_params)

def ftrl(**model_params):
    model_params.update({'ftrl': True})
    return model(model_params)
