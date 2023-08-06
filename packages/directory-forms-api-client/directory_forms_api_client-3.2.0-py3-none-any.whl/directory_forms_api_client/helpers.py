class FormSession:

    KEY_INGRESS_URL = 'DIRECTORY_API_FORMS_INGRESS_URL'
    KEY_FUNNEL_STEPS = 'DIRECTORY_API_FORMS_FUNNEL_STEPS'

    def __init__(self, request):
        self.session = request.session

    @property
    def ingress_url(self):
        return self.session.get(self.KEY_INGRESS_URL, '')

    @ingress_url.setter
    def ingress_url(self, ingress_url):
        self.session[self.KEY_INGRESS_URL] = ingress_url

    @ingress_url.deleter
    def ingress_url(self):
        self.session.pop(self.KEY_INGRESS_URL, None)

    @property
    def funnel_steps(self):
        self.funnel_steps = self.session.get(self.KEY_FUNNEL_STEPS, [])
        return self.session[self.KEY_FUNNEL_STEPS]

    @funnel_steps.setter
    def funnel_steps(self, steps):
        self.session[self.KEY_FUNNEL_STEPS] = steps

    @funnel_steps.deleter
    def funnel_steps(self):
        self.session.pop(self.KEY_FUNNEL_STEPS, None)

    def __del__(self):
        del self.funnel_steps
        del self.ingress_url
        return super().__del__()


class FormSessionMixin:
    form_session_class = FormSession

    def dispatch(self, request, *args, **kwargs):
        self.form_session = self.form_session_class(request=request)
        return super().dispatch(request=request, *args, **kwargs)
