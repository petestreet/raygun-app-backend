__author__ = 'Alex P'

import os
import logging
import webapp2

import models

import jinja2

template_path = os.path.join(os.path.dirname(__file__))

jinja2_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path),
    autoescape=True
)

#a helper class
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja2_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class HomepageHandler(Handler):
    def get(self):
        sloganRows = models.slogan.gql('ORDER BY globalRank DESC LIMIT 5').fetch()

        template_values = {"sloganRows": sloganRows}
        template = jinja2_env.get_template('site-html/index.html')
        self.response.out.write(template.render(template_values))


def handle_404(request, response, exception):
    logging.exception(exception)
    template = jinja2_env.get_template('site-html/404.html')
    response.write(template.render())
    response.set_status(404)


def handle_500(request, response, exception):
    logging.exception(exception)
    template = jinja2_env.get_template('site-html/500.html')
    response.write(template.render())
    response.set_status(500)


application = webapp2.WSGIApplication([
    ("/", HomepageHandler),
], debug=True)
application.error_handlers[404] = handle_404
#application.error_handlers[500] = handle_500