from django import forms

from z_tech.models import Tech


class TechCreationForm(forms.ModelForm):
    url = forms.CharField(label='링크', widget=forms.TextInput)

    class Meta:
        model = Tech
        fields = ['name', 'url']

    def clean_url(self):
        url = self.cleaned_data.get('url')  # url 가져오자
        if not (url.startswith('http://') or url.startswith('https://')):  # 만약 http:// 나 https://가 없으면,
            url = 'https://' + url  # https:// 추가하자
        return url

    def save(self, commit=True):
        new_tech = Tech.objects.create(
            name=self.cleaned_data.get('name'),  # 사용자가 입력한 내용을 clean_name()하고 깨끗해진 것 가져오자
            url=self.cleaned_data.get('url'),  # 사용자가 입력한 내용을 clean_url()하고 깨끗해진 것 가져오자
        )
        return new_tech


class TechChangeForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = ['name', 'url']
