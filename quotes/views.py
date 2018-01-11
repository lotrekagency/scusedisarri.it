import ukumuku
from ukumuku.views import View
from ukumuku.responses import HttpResponse
from ukumuku.cache import get_from_cache, set_value_in_cache
from ukumuku.templates import load_template
from ukumuku.utils import absolute_url

from sarri.utils import pick_og_image
import settings

from .utils import pick_quote


class QuoteView(View):
    def get(self, req, quote=None):
        picked_quote = pick_quote(quote)
        if picked_quote == None:
            return HttpResponse('', ukumuku.HTTP_301, headers={'Location' : '/dice'})
        else:
            context = picked_quote
            context.update({
                'live_url' : settings.LIVE_URL,
                'og_image_url' :  pick_og_image()
            })
            return HttpResponse(
                load_template('quotes/quote.html', context),
            )

class QuoteResource(View):
    def on_get(self, req, resp, quote=None):
        resp.status = ukumuku.HTTP_200
        resp.content_type = 'text/html'
        picked_quote = pick_quote(quote)
        if picked_quote == None:
            resp.status = ukumuku.HTTP_301
            resp.set_header('Location', '/dice')
        else:
            context = picked_quote
            context.update({
                'live_url' : settings.LIVE_URL,
                'og_image_url' :  pick_og_image()
            })
            
            resp.body = load_template('quotes/quote.html', context)