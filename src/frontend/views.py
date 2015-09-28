import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from frontend.forms import ContactFormSet, ContactForm, FilesForm, OrderFormSet, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

import requests
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse_lazy, reverse

from main.settings import PORT


class HomePageView(TemplateView):
    template_name = 'frontend/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context


#@login_required
def loginview(request):
    context = {
        'form': LoginForm,
        'login': "None"
    }

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect('formset_default')
            #context['login'] = 'Success'
            #return render(request, template_name='frontend/login.html', context=context)
        else:
            context['login'] = 'Failed'
            return render(request, template_name='frontend/login.html', context=context)
    else:
        return render(request, template_name='frontend/login.html', context=context)
        return HttpResponseBadRequest(content="Test")


class MainView(FormView):

    def get_context_data(self, **kwargs):
        context_data = super(MainView, self).get_context_data(**kwargs)
        context_data['api_response'] = APIClient().get_products()
        return context_data

    def get(self, request, *args, **kwargs):
        # user = authenticate(username='xx', password='xx')
        # login(request, user)
        if request.user.is_authenticated():
            return super(MainView, self).get(request, *args, **kwargs)
        else:
            context = dict(form=LoginForm)
            context['login'] = 'MainView Redirect'
            return render(request, template_name='frontend/login.html', context=context)
            raise APIException(detail='get')

    def post(self, request, *args, **kwargs):
        # user = authenticate(username='xx', password='xx')
        # login(request, user)
        if request.user.is_authenticated():
            return super(MainView, self).post(request, *args, **kwargs)
        else:
            raise APIException(detail='post')


class APIClient(object):
    protocol = 'http://'
    base_url = '0.0.0.0'
    port = PORT if PORT else '8080'
    content_type = {
        'Content-Type': 'application/json'
    }
    authentication_token = {
        'Authentication': 'Token aaaaaa'
    }

    def get_url(self, url=None):
        return "{}{}:{}/{}".format(self.protocol, self.base_url, self.port, url)

    def get_headers(self):
        headers = {}
        headers.update(self.content_type)

        return headers

    def get(self, url):
        url = self.get_url(url=url)
        headers = self.get_headers()

        response = requests.get(url, headers=headers)
        return response.json()

    def post(self, url, data=None):
        url = self.get_url(url=url)
        headers = self.get_headers()

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False

    def get_products(self):
        return self.get('products')

    def add_products(self, form):
        form = form.cleaned_data.pop()
        data = {
            'batch_size': form['amount_select'],
            'type': form['type_order'],
            'date': form['date'].strftime('%Y-%m-%d'),
        }
        added_orders = []
        for product_id in form['products']:
            data.update(order_id=product_id)
            response = self.add_product(data)
            added_orders.append(response)
        return added_orders

    def add_product(self, data):
        return self.post('order', data)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class DefaultFormsetView(LoginRequiredMixin, MainView):
    template_name = 'frontend/formset.html'
    form_class = OrderFormSet
    success_url = reverse_lazy('formset_default_success', kwargs={'success': 1})

    def get_form(self, form_class=None):
        form = super(DefaultFormsetView, self).get_form(form_class)
        products = APIClient().get_products()
        choices = [
            #('XS4ALL', (('abc', 'ABC'), ('1234', '5678'))),
            #('Telfort', (('abc', 'ABC'), ('1234', '5678'))),
        ]
        for product in products:
            choices.append((product['id'], product['name']),)
        form.form.declared_fields['products'].choices = choices
        return form

    def get(self, request, *args, **kwargs):
        success = kwargs.get('success', None)
        self.custom_success = success
        return super(MainView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            if APIClient().add_products(form):
                self.success_url = reverse_lazy('formset_default_success', kwargs={'success': 1})
            else:
                self.success_url = reverse_lazy('formset_default_success', kwargs={'success': 2})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super(DefaultFormsetView, self).post(request, *args, **kwargs)


class DefaultFormView(FormView):
    template_name = 'frontend/form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'frontend/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'frontend/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'frontend/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'frontend/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    # def get_initial(self):
    #     return {
    #         'file4': FieldFile(),
    #     }


class PaginationView(TemplateView):
    template_name = 'frontend/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'frontend/misc.html'