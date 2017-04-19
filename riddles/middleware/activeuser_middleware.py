import datetime
from django.core.cache import cache
from django.conf import settings

class ActiveUserMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		self.process_request(request)
		response = self.get_response(request)
		return response

	def process_request(self, request):
		current_user = request.user
		if request.user.is_authenticated:
			now = datetime.datetime.now()
			cache.set('status_%s' % (current_user.username), now, settings.USER_ONLINE_TIMEOUT)