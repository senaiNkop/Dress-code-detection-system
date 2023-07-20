
from itertools import zip_longest
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.http.response import JsonResponse

from data_analysis.models import DataAnalysis
from article.models import Article
from backend.models import Backend

# Create your views here.


COMPANY_NAME = "SENAI"
COMPANY_EMAIL = 'senai.nkop@gmail.com'
COMPANY_NUMBER = "+2349073720587"
COMPANY_ADDRESS = "No 15 Itu Road, Uyo, Nigeria"


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        data_analysis = DataAnalysis.objects.all()
        articles = Article.objects.all()
        backends = Backend.objects.all()

        context['company_name'] = COMPANY_NAME
        context['company_email'] = COMPANY_EMAIL
        context['company_number'] = COMPANY_NUMBER
        context['company_address'] = COMPANY_ADDRESS

        portfolios = zip_longest(data_analysis, articles, backends)
        context['portfolio'] = portfolios

        context['data_analysis'] = data_analysis
        context['articles'] = articles
        context['backend'] = backends

        return context


class SendEmails(TemplateView):

    def post(self, request, *args, **kwargs):

        body = request.POST

        name = body['name']
        email = body['email']
        subject = body['subject']
        message = f"{subject}\n\n{body['message']}\n\n {email}"

        try:
            send_mail(subject=name, message=message, from_email=email,
                      recipient_list=['samueleffiong80@gmail.com'])
        except Exception as e:
            return JsonResponse({'confirm': False})
        else:
            return JsonResponse({'confirm': True})

