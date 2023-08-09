from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

from FRVR.models import Question, Answer


class Home(ListView):
    template_name = 'home.html'
    context_object_name = 'questions'
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'GET':
            search_value = self.request.GET.get('query') or ''

            if search_value:
                context['questions'] = context['questions'].filter(title__icontains=search_value)
                context['search_value'] = search_value

        if self.request.user.is_authenticated:
            user_questions = Question.objects.all()
            context['question_count'] = user_questions.filter(user=self.request.user).count()

            context['answer_count'] = 0
            for question in user_questions:
                context['answer_count'] += question.answers.filter(user=self.request.user).count()

        context['popular_questions'] = Question.objects.annotate(
            num_answers=Count('answers')
        ).order_by('-num_answers')[:4]

        return context

    def post(self, request):
        try:
            text = request.POST['comment']
            question_id = request.POST['question_id']
            user = request.user
            counter = request.POST['counter']

            answer = Answer.objects.create(text=text,
                                           user=user,
                                           question_id=question_id)
            answer.save()

            return JsonResponse({
                'id': question_id,
                'username': user.username,
                'text': text,
                'time': answer.publication_date,
                'counter': counter
            })

        except Exception as e:
            return JsonResponse({'error': str(e)})


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        message = "*Wrong username or password*"
        return render(self.request, 'login.html', {'form': form, 'message': message})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        form.fields['password'].widget.attrs.update({
            'placeholder': 'Password'
        })
        return form


class CreateQuestion(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'create-question.html'
    fields = ['title', 'text']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Title field can't be blank"
        return render(self.request, 'create-question.html', {'form': form, 'message': message})


class EditQuestion(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'create-question.html'
    fields = ['title', 'text']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def form_invalid(self, form):
        message = "*Something went wrong*"
        return render(self.request, 'register.html', {'form': form, 'message': message})

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(Register, self).get(*args, **kwargs)
