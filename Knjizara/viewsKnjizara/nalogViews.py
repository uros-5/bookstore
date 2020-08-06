from Knjizara.views import *
from Knjizara.utils import Korisnik as korisnik


# login korisnika

def login_korisnika(request):
	setupSessionForKorisnik(request)
	if request.POST:

		form = Form_login(request.POST)

		user, provera = korisnik.check_login(form, authenticate, login, request)

		if (provera == True):

			setupSessionForKorisnik(request)
			if request.GET.get('next') is not None:
				return redirect(request.GET['next'])

			return HttpResponseRedirect(reverse('index'))

		elif (provera == False):

			return render(request, 'public/korisnik/nalog.html', {'form': form})
	else:
		form = Form_login()
		return render(request, 'public/korisnik/nalog.html', {'form': form})

class Form_login(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Lozinka", widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(Form_login, self).clean()
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("Wrong login or password!")
		return self.cleaned_data

class Registraciona_forma(forms.Form):
	first_name = forms.CharField(label="first_name", max_length=30)
	last_name = forms.CharField(label="last_name", max_length=150)
	username = forms.CharField(label="username", max_length=150)
	email = forms.EmailField(label="email")
	password = forms.CharField(label="password", widget=forms.PasswordInput)
	password_bis = forms.CharField(label="password", widget=forms.PasswordInput)
	CHOICES = (('korisnik', 'korisnik'),
			   ('autor', 'autor'))
	userType = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

	def clean(self):
		cleaned_data = super(Registraciona_forma, self).clean()
		password = self.cleaned_data.get("password")
		password_bis = self.cleaned_data.get("password_bis")
		if password and password_bis and password != password_bis:
			raise forms.ValidationError("Sifre nisu iste!")
		return self.cleaned_data


def regpage(request):
	if request.POST:
		form = Registraciona_forma(request.POST)

		if form.is_valid():

			korisnik.registracija(form)

			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, 'public/korisnik/registracija.html', {'form': form})
	else:

		form = Registraciona_forma()
		return render(request, 'public/korisnik/registracija.html', {'form': form})


class Korisnici_podaci(DetailView):
	model = Korisnici
	template_name = 'public/korisnik/korisnik_podaci.html'

	def get_context_data(self, **kwargs):
		context = super(Korisnici_podaci, self).get_context_data(**kwargs)
		contextEdited = korisnik.setUpKorisnikPodaci(context, self.object)
		return contextEdited

class Korisnici_narudzbine(ListView):
	model = Korisnici
	template_name = 'public/korisnik/narudzbine.html'
	paginate_by = 5

	def get_queryset(self):
		narudzbine = korisnik.listViewNarudzbina(self.request)

		return narudzbine


class Korisnici_ocenjene_knjige(ListView):
	model = Korisnici
	template_name = 'public/korisnik/ocenjene_knjige.html'
	paginate_by = 5

	def get_queryset(self):
		ocenjeneKnjige = korisnik.getOcenjeneKnjige(self.request)

		reviews = korisnik.setReviews(self.request, ocene=ocenjeneKnjige)

		return reviews

def logout_korisnika(request):
	logout(request)
	return render(request, 'public/korisnik/logout.html')
