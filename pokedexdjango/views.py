from django.shortcuts import render
from django.db.models import Q
from .models import Pokemon
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegisterForm
from django.core.files.storage import default_storage
from django.conf import settings
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def __validate_search_form(request) -> bool:
    poke_id_param = request.GET.get('poke_id', '')
    name_param = request.GET.get('name', '')
    type_param = request.GET.get('type', '')
    total_param = request.GET.get('total', '')
    hp_param = request.GET.get('hp', '')
    attack_param = request.GET.get('attack', '')
    defence_param = request.GET.get('defence', '')
    sp_attack_param = request.GET.get('sp_attack', '')
    sp_defence_param = request.GET.get('sp_defence', '')
    speed_param = request.GET.get('speed', '')
    generation_param = request.GET.get('generation', '')

    is_valid = True

    if type_param != '' and not type_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Type must be a number.')
        is_valid = False

    if name_param != '' and not all(x.isalpha() or x.isspace() for x in name_param):
        messages.add_message(request, messages.ERROR, 'Name must consist of letters.')
        is_valid = False

    if poke_id_param != '' and not poke_id_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Poke id must be a number.')
        is_valid = False

    if total_param != '' and not total_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Total must be a number.')
        is_valid = False

    if hp_param != '' and not hp_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Hp must be a number.')
        is_valid = False

    if attack_param != '' and not attack_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Attack must be a number.')
        is_valid = False

    if defence_param != '' and not defence_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Defence must be a number.')
        is_valid = False

    if sp_attack_param != '' and not sp_attack_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Sp attack must be a number.')
        is_valid = False

    if sp_defence_param != '' and not sp_defence_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Sp defence must be a number.')
        is_valid = False

    if speed_param != '' and not speed_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Speed must be a number.')
        is_valid = False

    if generation_param != '' and not generation_param.isdigit():
        messages.add_message(request, messages.ERROR, 'Generation must be a number.')
        is_valid = False

    return is_valid


def pokemon_details(request, id):
    title = 'Pokemon Details'

    poke_id_param = id
    # poke_id_param = request.GET.get('poke_id', '')
    pokemon_details = Pokemon.objects.get(id=poke_id_param)

    return render(request,
                  'pokedexdjango/pokemon_details.html',
                  {
                      'title': title,
                      'pokemon': pokemon_details
                  })


def pokemon_list(request):
    title = 'Pokemon list'

    poke_id_param = request.GET.get('poke_id', '')
    name_param = request.GET.get('name', '')
    type_param = request.GET.get('type', '')
    total_param = request.GET.get('total', '')
    hp_param = request.GET.get('hp', '')
    attack_param = request.GET.get('attack', '')
    defence_param = request.GET.get('defence', '')
    sp_attack_param = request.GET.get('sp_attack', '')
    sp_defence_param = request.GET.get('sp_defence', '')
    speed_param = request.GET.get('speed', '')
    generation_param = request.GET.get('generation', '')
    sort_by_param = request.GET.get('sort_by', '')
    sort_direction_param = request.GET.get('sort_direction', '')

    pokemon_list = Pokemon.objects.all()

    is_valid = __validate_search_form(request)

    if not is_valid:
        return redirect('pokedexdjango:pokemon_list')

    if type_param != '':
        pokemon_list = pokemon_list.filter(Q(type_1__contains=type_param) | Q(type_2__contains=type_param))

    if name_param != '':
        pokemon_list = pokemon_list.filter(name__contains=name_param)

    if poke_id_param != '':
        pokemon_list = pokemon_list.filter(poke_id=poke_id_param)

    if total_param != '':
        pokemon_list = pokemon_list.filter(total=total_param)

    if hp_param != '':
        pokemon_list = pokemon_list.filter(hp=hp_param)

    if attack_param != '':
        pokemon_list = pokemon_list.filter(attack=attack_param)

    if defence_param != '':
        pokemon_list = pokemon_list.filter(defence=defence_param)

    if sp_attack_param != '':
        pokemon_list = pokemon_list.filter(sp_attack=sp_attack_param)

    if sp_defence_param != '':
        pokemon_list = pokemon_list.filter(sp_defence=sp_defence_param)

    if speed_param != '':
        pokemon_list = pokemon_list.filter(speed=speed_param)

    if generation_param != '':
        pokemon_list = pokemon_list.filter(generation=generation_param)

    if sort_by_param != '':
        sort_by_desc = sort_by_param
        if sort_direction_param == 'desc':
            sort_by_desc = '-' + sort_by_param
        pokemon_list = pokemon_list.order_by(sort_by_desc, 'poke_id')
    else:
        pokemon_list = pokemon_list.order_by('poke_id')

    pokemon_images = __get_pokemon_images(pokemon_list)


    return render(request,
                  'pokedexdjango/pokemon_list.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                      'form_action': request.path,
                      'poke_id_param': poke_id_param,
                      'name_param': name_param,
                      'type_param': type_param,
                      'total_param': total_param,
                      'hp_param': hp_param,
                      'attack_param': attack_param,
                      'defence_param': defence_param,
                      'sp_attack_param': sp_attack_param,
                      'sp_defence_param': sp_defence_param,
                      'speed_param': speed_param,
                      'generation_param': generation_param,
                      'sort_by_param': sort_by_param,
                      'sort_direction_param': sort_direction_param
                  })


def __get_pokemon_images(pokemon_list) -> dict:
    pokemon_images = dict()

    for x in pokemon_list:
        pokemon_image_path = str(settings.BASE_DIR) + '/static/images/' + str(x.poke_id) + '.jpg'
        exist = default_storage.exists(pokemon_image_path)
        pokemon_images[x.poke_id] = exist

    return pokemon_images


def top_10(request):
    title = 'TOP 10'
    print("http://localhost:8000/top_10/")
    return render(request,
                  'pokedexdjango/top_10.html',
                  {
                      'title': title
                  })


def top_10_pokemons(request):
    title = 'TOP 10 Pokemons'

    pokemon_list = Pokemon.objects.all().order_by('-total')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)

    return render(request,
                  'pokedexdjango/top_10_pokemons.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def top_10_attack(request):
    title = 'TOP 10 Pokemons with the best attack'

    pokemon_list = Pokemon.objects.all().order_by('-attack')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)

    return render(request,
                  'pokedexdjango/top_10_attack.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def top_10_defence(request):
    title = 'TOP 10 Pokemons with the best defence'


    pokemon_list = Pokemon.objects.all().order_by('-defence')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)

    return render(request,
                  'pokedexdjango/top_10_defence.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def top_10_not_legendary(request):
    title = 'TOP 10 Pokemons that are not legendary'


    pokemon_list = Pokemon.objects.all().filter(legendary='False').order_by('-total')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)


    return render(request,
                  'pokedexdjango/top_10_not_legendary.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def top_10_water(request):
    title = 'TOP 10 water Pokemons'


    pokemon_list = Pokemon.objects.all().filter(type_1='Water').order_by('-total')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)


    return render(request,
                  'pokedexdjango/top_10_water.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def top_10_hp(request):
    title = 'TOP 10 Pokemons with the biggest health'


    pokemon_list = Pokemon.objects.all().order_by('-hp')[:10]

    pokemon_images = __get_pokemon_images(pokemon_list)


    return render(request,
                  'pokedexdjango/top_10_hp.html',
                  {
                      'title': title,
                      'pokemon_list': pokemon_list,
                      'pokemon_images': pokemon_images,
                  })


def user_info(request):
    if request.method == 'GET':
        context = {'title': 'User Info Page'}
        template = 'pokedexdjango/user_info.html'
        return render(request,
                      template,
                      context)


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("pokedexdjango:home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})

