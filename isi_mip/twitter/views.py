from django.shortcuts import render

from isi_mip.twitter.twitter import Twitte


def twitte(request):
    stati = Twitte().get_timeline('ISIMIPImpacts')
    context = {'stati': stati}
    template = 'twitter/list.html'
    return render(request, template, context)