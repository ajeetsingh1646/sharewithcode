from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, Http404
from .form import JoinForm,EmailForm
from .models import Join

import uuid
# Create your views here.
def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip			

def get_ref_id():
	ref_id = str(uuid.uuid4())[:11].replace('-','').lower()
	try:
		id_exists = Join.objects.get(ref_id=ref_id)
		return get_ref_id()
	except:
		return ref_id

def share(request, ref_id):
	try:
		join_obj = Join.objects.get(ref_id= ref_id)
		friends_referred = Join.objects.filter(friend = join_obj)
		count = join_obj.referer.all().count()
		ref_url = settings.SHARE_URL + str(join_obj.ref_id)
		context = {"ref_id": join_obj.ref_id, "count": count, "ref_url": ref_url}
		template = "share.html"
		return render(request, template, context)
	except:
		raise Http404

def home(request):
	try:
		join_id = request.session['join_id_ref']
		obj = Join.objects.get(id = join_id)
	except:
		obj = None
	form = JoinForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data['email']
		new_join, created = Join.objects.get_or_create(email = email)
		if created:
			new_join.ref_id = get_ref_id()
			#add our friend who joined us to our join or related model
			if not obj == None:
				new_join.friend = obj
			new_join.ip_address = get_ip(request)
			new_join.save()
		# print all "friends" that joined as a result of main sharer email
		#print(Join.objects.filter(friend=obj))
		#print(obj.referer.all().count())

		return HttpResponseRedirect("%s" %(new_join.ref_id))
	context = {"form": form}
	template = "home.html"
	return render(request, template, context)
