
import os
from uuid import uuid4
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect, JsonResponse

from .models import DataModel, CATEGORY_CHOICES, SEX_CHOICES


# Create your views here.
WEBSITE_NAME = 'Dress Code AI'
EMAIL = 'senai.nkop@gmail.com'
TEL = '+23409073720587'
COMPANY_NAME = 'SENAI'
MOTTO = 'Your Stop point to all your software solutions'

base_path = settings.BASE_DIR

with open(f'{base_path}/dress_code/LOGIN_SHORT_STORIES.txt', 'r') as file:
    LOGIN_SHORT_STORIES = file.readlines()

with open(f'{base_path}/dress_code/LOGIN_PHRASES.txt', 'r') as file:
    LOGIN_PHRASES = file.readlines()

with open(f'{base_path}/dress_code/REGISTER_SHORT_STORIES.txt', 'r') as file:
    REGISTER_SHORT_STORIES = file.readlines()

with open(f'{base_path}/dress_code/REGISTER_PHRASES.txt', 'r') as file:
    REGISTER_PHRASES = file.readlines()

with open(f'{base_path}/dress_code/DATA_COLLECTION_JOKES.txt', 'r') as file:
    DATA_COLLECTION_JOKES = file.readlines()

with open(f'{base_path}/dress_code/AI_JOKES.txt', 'r') as file:
    AI_JOKES = file.readlines()


class HomepageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('dress-code:login')
    template_name = 'dress_code/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['male_sex'] = DataModel.custom_manager.get_sex_count(self.request.user.username, 'Male')
        context['female_sex'] = DataModel.custom_manager.get_sex_count(self.request.user.username, 'Female')
        context['other_sex'] = DataModel.custom_manager.get_sex_count(self.request.user.username, 'Others')
        context['arg_max_sex'] = max(
            [context['male_sex'], context['female_sex'],
             context['other_sex']]
        )

        # First Row Charts

        # right side
        proper_unique_weekly, proper_count_weekly = DataModel.custom_manager.get_category_daily(self.request.user.username, 'proper')
        improper_unique_weekly, improper_count_weekly = DataModel.custom_manager.get_category_daily(self.request.user.username, 'improper')

        arg_max_category_weekly = max(proper_count_weekly + improper_count_weekly)
        unique_weekly = list(set([0] + list(proper_unique_weekly) + list(improper_unique_weekly)))

        context['arg_max_category_weekly'] = arg_max_category_weekly
        context['unique_weekly_category'] = unique_weekly
        context['proper_count_weekly'] = [0] + proper_count_weekly
        context['improper_count_weekly'] = [0] + improper_count_weekly

        # left side
        male_proper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Male', 'proper')
        female_proper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Female', 'proper')
        other_proper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Others', 'proper')

        male_improper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Male', 'improper')
        female_improper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Female', 'improper')
        other_improper = DataModel.custom_manager.get_sex_and_category_count(self.request.user.username, 'Others', 'improper')

        sex_proper = [male_proper, female_proper, other_proper]
        sex_improper = [male_improper, female_improper, other_improper]

        context['sex_proper'] = sex_proper
        context['sex_improper'] = sex_improper
        context['arg_max_sex_and_category'] = max(sex_proper + sex_improper)

        context['proper_category_count'] = DataModel.custom_manager.get_category_count(self.request.user.username)
        context['improper_category_count'] = DataModel.custom_manager.get_category_count(self.request.user.username, 'improper')

        context['total'] = sum(DataModel.objects.all().values_list('no_of_images', flat=True))

        proper_total = sum(DataModel.objects.filter(username=self.request.user.username, category='Proper Dress code').values_list('no_of_images', flat=True))
        improper_total = sum(DataModel.objects.filter(username=self.request.user.username).exclude(category='Proper Dress code').values_list('no_of_images', flat=True))

        user_unique_weekly, user_count_weekly = DataModel.custom_manager.get_user_total_weekly(self.request.user.username)
        arg_max_user_weekly = max(user_count_weekly)

        context['user_unique_weekly'] = [0] + list(user_unique_weekly)
        context['user_count_weekly'] = [0] + user_count_weekly
        context['arg_max_user_count_weekly'] = max(context['user_count_weekly'])

        context['category_total'] = [proper_total, improper_total]
        context['arg_max_category_total'] = max(context['category_total'])
        return context


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('dress-code:homepage'))


class LoginView(TemplateView):
    template_name = 'dress_code/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['SHORT_STORIES'] = LOGIN_SHORT_STORIES
        context['LOGIN_PHRASE'] = LOGIN_PHRASES
        return context

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['SHORT_STORIES'] = LOGIN_SHORT_STORIES
        context['LOGIN_PHRASE'] = LOGIN_PHRASES

        body = request.POST

        username_or_email = body['email']
        password = body['password']

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            # TODO: Ensure that email is unique
            # Email is used for login

            try:
                user = User.objects.get(email=username_or_email)
            except User.MultipleObjectsReturned as e:
                context['error'] = str(e)
                return self.render_to_response(context)
            except User.DoesNotExist as e:
                context['error'] = str(e)
                return self.render_to_response(context)
                # Water don pass garri be that
                # invalid login details
            else:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('dress-code:homepage'))
        else:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('dress-code:homepage'))


class RegisterView(TemplateView):
    template_name = 'dress_code/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['REGISTER_SHORT_STORIES'] = REGISTER_SHORT_STORIES
        context['REGISTER_PHRASES'] = REGISTER_PHRASES

        return context

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['REGISTER_SHORT_STORIES'] = REGISTER_SHORT_STORIES
        context['REGISTER_PHRASES'] = REGISTER_PHRASES

        body = request.POST

        username = body['username']
        email = body['email']
        password = body['password']
        sex = body['sex']

        # Check to ensure username is unique
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            user = None

        if user is not None:
            context['error'] = f"An account with this name ({username}) is created already"
            return self.render_to_response(context)

        elif User.objects.filter(email=email.lower()):
            context['error'] = f"An account with this email ({email}) is created already"
            return self.render_to_response(context)

        else:
            user = User(username=username, email=email.lower(), first_name=sex)
            user.set_password(password)

            try:
                user.save()
            except Exception as e:
                context['error'] = str(e)
                return self.render_to_response(context)

            login(request, user)
            return HttpResponseRedirect(reverse_lazy('dress-code:homepage'))


class ContactFromLoginView(TemplateView):
    template_name = 'dress_code/auth_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        return context


class DataCollectionView(LoginRequiredMixin, TemplateView):
    template_name = 'dress_code/data.html'
    login_url = reverse_lazy('dress-code:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['DATA_COLLECTION_JOKES'] = DATA_COLLECTION_JOKES
        context['AI_JOKES'] = AI_JOKES

        A = os.getcwd()
        B = settings.BASE_DIR
        C = settings.STATIC_URL

        values = f"{settings.BASE_DIR}/static/assets/dress_code/img/sample_pic"

        context['no_of_sample_pics'] = os.listdir(values)

        return context

    @staticmethod
    def write_image(path, image):

        if not os.path.exists(path):
            os.makedirs(path)

        random_generator = str(uuid4())
        path = f"{path}/{random_generator}_{image.name}"

        with open(path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        return path

    @staticmethod
    def get_image_path(obj, file):
        base_url = f"dress_code/{obj.username}/{obj.sex}/{obj.category}"
        return base_url

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        context['DATA_COLLECTION_JOKES'] = DATA_COLLECTION_JOKES
        context['AI_JOKES'] = AI_JOKES

        body = request.POST
        files = request.FILES

        sex = int(body['sex'])
        category = int(body['category'])
        location = body['location'].strip()
        images = files.getlist('images')

        category_dict = dict(CATEGORY_CHOICES)
        sex_dict = dict(SEX_CHOICES)

        # TODO: Check in case the user somehow sent a form without any image
        if not images:
            context['error'] = 'witty error messages'
            return self.render_to_response(context)

        data = DataModel(username=request.user, sex=sex_dict[sex], category=category_dict[category])

        images_path = []
        for image in images:
            path = self.get_image_path(data, image)
            full_path = f"{settings.MEDIA_ROOT}{path}"

            full_path = self.write_image(full_path, image)
            images_path.append(full_path)

        data.no_of_images = len(images_path)
        images_path = ", ".join(images_path)
        data.images = images_path

        try:
            data.save()
        except Exception as e:
            context['error'] = str(e)
            return self.render_to_response(context)

        context['success'] = "Witty successful remarks"

        return self.render_to_response(context)


class AboutView(TemplateView):
    template_name = "dress_code/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        return context


class AnalysisView(LoginRequiredMixin, TemplateView):
    template_name = 'dress_code/analysis.html'
    login_url = reverse_lazy('dress-code:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['COMPANY_NAME'] = COMPANY_NAME
        context["WEBSITE_NAME"] = WEBSITE_NAME
        context['EMAIL'] = EMAIL
        context['TEL'] = TEL
        context['MOTTO'] = MOTTO

        return context

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)

        file = request.FILES

        return JsonResponse({})










