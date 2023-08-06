import base64
from IPython.display import Javascript
import uuid
import abc

from IPython.display import clear_output
from .vdomr import exec_javascript

class Component(object):
  def __init__(self):
    self._div_id=str(uuid.uuid4())
  @abc.abstractmethod
  def render(self):
    return None
  def refresh(self):
    html=self.render().to_html()
    html_encoded=base64.b64encode(html.encode('utf-8')).decode('utf-8')
    js="{{var elmt=document.getElementById('{}'); if (elmt) elmt.innerHTML=atob('{}');}}".format(self._div_id,html_encoded)
    exec_javascript(js)
  def to_html(self):
    return self._repr_html_()
  def _repr_html_(self):
    html=self.render().to_html()
    return '<div id={}>'.format(self._div_id)+html+'</div>'

