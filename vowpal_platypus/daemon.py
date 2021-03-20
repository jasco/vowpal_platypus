from internal import netcat
from utils import vw_hash_to_vw_str
from vw import VW

def daemon(model, port=None, num_children=1):
    if isinstance(model, basestring):
        model_handle = model.split('.')[0]
        model_file = model
    else:
        if not port:
            if model.params.get('node'):
                port = model.params['node'] + 4040
            else:
                port = 4040
        model_handle = model.handle
        model_file = model.get_model_file()
    daemon_model = VW({'name': model_handle,
                       'daemon': True,
                       'old_model': model_file,
                       'holdout_off': True,
                       'quiet': True,
                       'port': port,
                       'num_children': num_children})
    daemon_model.start_predicting()
    return daemon_model

def daemon_predict(daemon, content, quiet=False):
    if isinstance(daemon, int):
        port = daemon
    else:
        port = daemon.params['port']
    if isinstance(content, dict):
        content = [content]
    if not isinstance(content[0], dict):
        raise ValueError("Daemon predict can only predict on a VP dictionary.")
    content = '\n'.join(map(vw_hash_to_vw_str, content))
    return netcat(port=port,
                  content=content,
                  quiet=quiet)
