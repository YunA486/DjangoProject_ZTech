from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.models import Profile
from z_tech.forms import TechCreationForm, TechChangeForm
from z_tech.models import Tech


class TechListView(ListView):
    model = Tech

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:  # 로그인 하면, 로그인한 사용자의 북마크만 보이자
            profile = Profile.objects.get(user=user)  # user -> profile
            tech_list = Tech.objects.filter(profile=profile)  # profile -> bookmark_list
        else:  # 로그인 안하면,
            tech_list = Tech.objects.none()  # 북마크 보이지 말자
        return tech_list


class TechCreateView(LoginRequiredMixin, CreateView):
    model = Tech
    fields = ['profile', 'name', 'url']  # '__all__'
    template_name_suffix = '_create'  # bookmark_form.html -> bookmark_create.html
    success_url = reverse_lazy('z_tech:list')

    def get_initial(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return {'profile': profile}


class TechDetailView(LoginRequiredMixin, DetailView):
    model = Tech


class TechUpdateView(LoginRequiredMixin, UpdateView):
    model = Tech
    fields = ['name', 'url']  # '__all__'
    template_name_suffix = '_update'  # bookmark_update.html

class TechDeleteView(LoginRequiredMixin, DeleteView):
    model = Tech
    success_url = reverse_lazy('z_tech:list')


def list_tech(request):
    # 로그인 사용자 확인하자
    user = request.user
    if user.is_authenticated:  # 로그인 되어있으면
        profile = Profile.objects.get(user=user)
        tech_list = Tech.objects.filter(profile=profile)  # 그 사용자의 북마크 가져오자
    else:  # 로그인 안되어 있으면
        tech_list = Tech.objects.none()  # 북마크 없는것 가져오자

    return render(request, 'z_tech/tech_list.html', {'tech_list': tech_list})


def detail_tech(request, pk):
    tech = Tech.objects.get(pk=pk)
    return render(request, 'z_tech/tech_detail.html', {'tech': tech})


@login_required
def delete_tech(request, pk):
    if request.method == 'POST':  # 삭제 버튼 눌렀을 때
        tech = Tech.objects.get(pk=pk)
        tech.delete()  # DELETE FROM table WHERE 조건
        return redirect('z_tech:list')
    else:  # 처음 bookmark_delete.html 요청
        tech = Tech.objects.get(pk=pk)
        return render(request, 'z_tech/tech_confirm_delete.html', {'tech': tech})


@login_required
def create_tech(request):
    if request.method == 'POST':  # 사용자가 입력하고 버튼 눌렀을 때
        form = TechCreationForm(request.POST)  # form 가져오자
        if form.is_valid():  # is_valid()
            new_tech = form.save(commit=False)  # new_bookmark 생성하자(name, url)
            new_tech.profile = Profile.objects.get(user=request.user)  # new_bookmark에 profile 추가하자
            new_tech.save()
            return redirect('z_tech:list')  # bookmark:list 이동하자
    else:  # 빈 폼
        form = TechCreationForm()
    return render(request, 'z_tech/tech_create.html', {'form': form})


@login_required
def modify_tech(request, pk):
    if request.method == 'POST':
        form = TechChangeForm(request.POST)  # form 가져오자
        if form.is_valid():  # is_valid()
            tech = Tech.objects.get(pk=pk)  # pk에 해당하는 bookmark 가져오자
            tech.name = form.cleaned_data.get('name')  # 사용자가 입력한 name set
            tech.url = form.cleaned_data.get('url')  # 사용자가 입력한 url set
            tech.save()
            return redirect('z_tech:list')  # bookmark:list로 이동하자
    else:
        tech = Tech.objects.get(pk=pk)  # pk에 해당하는 bookmark 정보 가져오자
        form = TechChangeForm(instance=tech)  # bookmark 정보 넣은 form
    return render(request, 'z_tech/tech_update.html', {'form': form})
