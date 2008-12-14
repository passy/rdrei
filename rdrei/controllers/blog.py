from werkzeug import BaseResponse
from rdrei.utils import render_template
from rdrei.controllers import BaseController
from rdrei.decorators import beaker_cache

class BlogController(BaseController):
    def index(self, request):
        return render_template("index.html")

    def get_session(self, request):
        c = {'msg': "Session value is: "+request.session.get("test_data",
                                                             "empty")}
        return render_template("index.html", c)

    def set_session(self, request, value):
        request.session['test_data'] = value
        request.session.save()
        return BaseResponse("Okay, new Value: %s" %
                            request.session.get('test_data'))

    @beaker_cache(query_args=False)
    def cached_page(self, request):
        """With query_args=False, the arguments to this method are ignored. That
        means that the first call with ?wurst=x will set the cache value and any
        change will be ignore. Set query_args=True, to turn this behaviour
        off."""
        parameter = 'wurst' in request.values and request.values['wurst'] or None
        if parameter:
            return BaseResponse("This should be cached. Wurst is currently %s." %
                                parameter)
        return BaseResponse("This should be cached. (Watch log to verify.)")


controller = BlogController