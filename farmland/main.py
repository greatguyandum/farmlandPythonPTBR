import os
import sys
import time
import random
import winsound
import climage

from playsound3 import playsound
from nava import play, stop

from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich_pixels import Pixels

# Migrado de init.py

character_tags = {
    "alex": "italic green",
    "jake": "bold white",
    "bunnyman": "red",
}

__rich_console = Console(theme=Theme(character_tags))
__rich_theme = Theme()

TrueUserName = f"[purple]{os.getlogin().split()[0].capitalize()}[/purple]"
userName = "[yellow]Anon[/yellow]"
gameOverCount = 0
isDefending = False

playerStats = {
    "hp": 20,
    "max_hp": 20,
    "def": 5,
    "str": 5,
    "is_defending": False,
    "deathCount": 1
}

# Migrado de engine.py
def typewriter_effect(message, txtspeed=0.05, txtstyle="jake", prefix=""): # Codigo original de Senpai Yash no Reddit, Modificado levemente
    console = __rich_console


    prefix_text = Text.from_markup(prefix) if isinstance(prefix, str) else prefix
    styled_text = Text.from_markup(message)
    displayed_text = Text(style=txtstyle)
    current_speed = txtspeed

    with Live(prefix_text, console=console, refresh_per_second=20) as live:
        for character_obj in styled_text:
            char = character_obj.plain
            
            if char == ">":
                current_speed = 0.01
                continue
            elif char == "<":
                current_speed = 0.67
                continue
            elif char == "|":
                current_speed = 0.1
                continue

            if not character_obj.style:
                character_obj.style = txtstyle

            displayed_text.append(character_obj)
            live.update(prefix_text + displayed_text)
            time.sleep(current_speed)

def typewriter_effectFAKE(message, txtspeed=0.05, txtstyle="jake", prefix=""): # Codigo original de Senpai Yash no Reddit, Modificado levemente
    console = __rich_console


    prefix_text = Text.from_markup(prefix) if isinstance(prefix, str) else prefix
    styled_text = Text.from_markup(message)
    displayed_text = Text(style=txtstyle)
    current_speed = txtspeed

    with Live(prefix_text, console=console, refresh_per_second=20) as live:
        for character_obj in styled_text:
            char = character_obj.plain

            if not character_obj.style:
                character_obj.style = txtstyle

            displayed_text.append(character_obj)
            live.update(prefix_text + displayed_text)
            time.sleep(current_speed)

def richprint(*args, **kwargs):
    return __rich_console.print(*args, **kwargs)

def typeprint(textu, txtspeed=0.05, character="jake"):
    speeed = txtspeed
    for char in textu:
        if char == ">":
            speeed = 0.01
            continue
        elif char == "<":
            speeed = 0.67
            continue
        elif char == "|":
            speeed = 0.1
            continue
        
        richprint(char, style=character, end="")
        time.sleep(speeed)
    print()

def audio_play_engine(_sound):
    typeprint("")

def alexPlayer():
    global playerStats
    return playerStats

def wrongWarp():
    play("snd_weirdwarp.wav", async_mode=False, loop=False)

def __gameOver():
    myPlayer = alexPlayer()
    myPlayer["deathCount"] += 1
    typewriter_effect("Sua visão se embaçou e o chão pareceu se rachar...")
    typewriter_effect("Você se entregou para a escuridão")
    musicaPrincipal = play("snd_weirdwarp.wav", async_mode=True)
    for index in range(9, 0, -1):
        brilho_invertido = 9 - index
        red_value = int((brilho_invertido / 10) * 255)
        richprint("---------------------------------------------------------------------------------------", style=f"rgb({red_value},0,0)")
        time.sleep(0.15)
        
    for jindex in range(1, 55):
        richprint("---------------------------------------------------------------------------------------", style="red")
        time.sleep(0.25)

    play("snd_fallOnBlood.wav", async_mode=False, loop=False)

    hums = play("meetingdeath.wav", async_mode=True, loop=True)
    if myPlayer["deathCount"] > 1:
        typewriter_effect("O seu caminho levou a um fim... Porem ainda vejo algo brilhando dentro de sua alma", txtstyle="bold red", txtspeed=0.15, prefix="[bold red] Ceifador: ")
        typewriter_effect("A [purple]esperança[/purple], ainda resta [purple]esperança[/purple] no seu receptaculo, vou poupa-lo mas você ainda tem uma escolha", txtstyle="bold red", txtspeed=0.15, prefix="[bold red] Ceifador: ")
    typewriter_effect("[D: [yellow]Ceder[/yellow]] [H: [purple]Persistir[/purple]]", txtstyle="bold red", txtspeed=0.15, prefix="[bold red] Ceifador: ")
    retry = input(">").lower()
    stop(hums)
    match retry:
        case "d":
            typewriter_effect("E então a [purple]esperança[/purple] foi deixada para morrer", txtstyle="bold red", txtspeed=0.15, prefix="[bold red] Ceifador: ")
            deathRemains = play("despairremains.wav", async_mode=True, loop=True)
            while True:
                richprint("")
                time.sleep(0.35)
        case "h":
            typewriter_effect("A [purple]esperança[/purple] reside em você", txtstyle="bold red", txtspeed=0.15, prefix="[bold red] Ceifador: ")
            for jindex in range(1, 35):
                richprint("---------------------------------------------------------------------------------------", style="red")
                time.sleep(0.05)
                input("> ")

def __battleSystem(_enemyName, _enemyHp, _acoes=None, _behaviour=None, song="corruptedvictims.wav"):
    global isDefending
    enemyHp = _enemyHp
    myPlayer = alexPlayer()
    startingHp = myPlayer["hp"]
    while True:
        battleSong = play(song, async_mode=True, loop=True)
        typeprint(f"{_enemyName} se aproxima")
        richprint("-------------------------")
        while enemyHp > 0 and myPlayer["hp"] > 0:
            myPlayer = alexPlayer()
            myPlayer["is_defending"] = False
            richprint(_enemyName + " Hp: " + str(enemyHp))
            richprint(f"Alex HP: {myPlayer['hp']}/{myPlayer['max_hp']}")
            richprint("[A: Ataque] [B: Ações] [C: Defender]")
            action = input("> ").lower()
            match action:
                case "a":
                    enemyHp -= myPlayer["str"]
                case "b":
                    if not _acoes:
                        __rich_console.print("Não tem ações disponíveis")
                    else:
                        __rich_console.print("\n-- SUAS AÇÕES --")
                        lista_nomes = list(_acoes.keys())
                        for i, nome in enumerate(lista_nomes):
                            __rich_console.print(f"[{i + 1}] {nome}")
                        __rich_console.print("[0] Voltar")
                        acaoIndex = input("> ")

                        if acaoIndex.isdigit():
                            idk = int(acaoIndex) - 1
                            if idk == -1:
                                continue
                            elif 0 <= idk < len(lista_nomes):
                                nome_acao = lista_nomes[idk]
                                _acoes[nome_acao]()
                            else:
                                richprint("Opção inválida.")
                        else:
                            richprint("Por razões obvias, você não conseguiu atacar")
                case "c":
                    typewriter_effect(f"Você se defendeu usando seu braço, ataque de {_enemyName} foi reduzido")
                    myPlayer["is_defending"] = True
                case _:
                    richprint("Ação não reconhecida")
            
            if enemyHp > 0:
                _behaviour()

            if myPlayer["hp"] <= 0:
                __gameOver()
                stop(battleSong)
                break
        
        if enemyHp <= 0:
            richprint(_enemyName + " foi derrotado")
            stop(battleSong)
            bgSong = play("unendingloop.wav", async_mode=True, loop=True)
            myPlayer["hp"] = myPlayer["max_hp"]
            break
        else:
            myPlayer["hp"] = startingHp
            enemyHp = _enemyHp
            continue

def acao_default_bunnyman():
    typeprint("Você tentou amigar Bunnyman... Não foi muito effetivo")

def acao_respiro_bunnyman():
    myPlayer = alexPlayer()
    typeprint("Você cobriu sua respiração com suas mãos, porem suas mãos parecem estar distorcendo")
    hpRecu = random.randint(4, 7)
    typeprint(f"Ganhou {hpRecu} de vida")
    myPlayer["hp"] += hpRecu

acoes_bunnyman = {
    "Amigar" : acao_default_bunnyman,
    "Cobrir Respiração - Recupera Vida" : acao_respiro_bunnyman,
}

def behaviour_bunnyman():
    global isDefending
    myPlayer = alexPlayer()
    dano_base = random.randint(2, 3)
    fala = random.randint(1, 3)
    match fala:
        case 3:
            typeprint("Mi venas en la nomo de K'n-yan", character="bunnyman")
        case 2:
            typeprint("Mi no venas en paco", character="bunnyman")
        case 1:
            typeprint("Frakasu la krepuskan revadon", character="bunnyman")
            
    if myPlayer["is_defending"]:
        dano_final = round(dano_base / myPlayer["def"])
    else:
        dano_final = dano_base
        
    myPlayer["hp"] -= dano_final
    typeprint(f"Bunnyman te ataca, levou {dano_final} de dano")

def bunnymanFight():
    play("snd_b.wav")
    console = Console()
    encounter = Pixels.from_image_path("BunnyEncounterFIX.png")
    console.print(encounter)
    time.sleep(2.5)
    alexTalk("Um coelho? O que um coelha faz aqui-")
    for index in range(1, 40):
        richprint("")
    play("snd_corrupt.wav")
    encounterCorrupt = Pixels.from_image_path("BunnyManEncounterFIX.png")
    console.print(encounterCorrupt)
    __battleSystem("Bunnyman", 45, acoes_bunnyman, behaviour_bunnyman)

def bunnymanExample():
    play("snd_corrupt.wav")
    __battleSystem("Bunnyman", 45, acoes_bunnyman, behaviour_bunnyman)

def acao_default_ghostpig():
    typeprint("---")
    hpRecu = 5
    myPlayer = alexPlayer()
    myPlayer["hp"] += hpRecu

acoes_ghostpig = {
    "???" : acao_default_ghostpig,
}

def behaviour_ghostpig():
    global isDefending
    myPlayer = alexPlayer()
    dano_base = random.randint(3, 7)
    fala = random.randint(1, 2)
    match fala:
        case 1:
            typewriter_effect("Oink oink", txtstyle="bunnyman", prefix="[red]Ghoulig: [/red]")
        case _:
            typewriter_effect("I have the body of a pig", txtstyle="bunnyman", prefix="[red]Ghoulig: [/red]")
            
    if myPlayer["is_defending"]:
        dano_final = round(dano_base / myPlayer["def"])
    else:
        dano_final = dano_base
        
    myPlayer["hp"] -= dano_final
    if dano_final >= 4:
        typeprint(f"Ghoulig ruge alto, sua cabeça doi, levou {dano_final} de dano")
    else:
        typeprint(f"Ghoulig morde sua mão, levou {dano_final} de dano")

def ghostPigFight():
    typewriter_effect("Algo do celeiro te seguiu...")
    play("fear.wav")
    console = Console()
    encounterCorrupt = Pixels.from_image_path("GhouligEncounter.png")
    console.print(encounterCorrupt)
    play("snd_corrupt.wav")
    time.sleep(0.67)
    __battleSystem("Ghoulig", 25, acoes_ghostpig, behaviour_ghostpig, "deadvictims.wav")

def carregamento(_string="Carregando texturas...", duration=3):
    spinner_chars = ["|", "/", "-", "\\"]
    end_time = time.time() + duration

    print(_string, end="")
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{_string} {spinner_chars[idx % len(spinner_chars)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    print("\nPronto!")

def audio_play(_sound, _block=True, _backend=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(current_dir, _sound)
    return playsound(audio_path, _block, _backend)

def mail(_text, _subject, _from, _to):
    richprint("------------------------------")
    header = Table.grid(expand=True)
    header.add_column(justify="left", style="cyan")
    header.add_column(justify="right", style="magenta")
    header.add_row(f"De: {_from}")
    header.add_row(f"Para: {_to}")
    email_body = _text
    richprint(header, Panel(email_body, title=_subject))

class Farmeer:
    def __init__(self, name, creator, personality):
        self.name = name
        self.creator = creator
        self.personality = personality
        self.friendship = 10

def FarmerCreator():
    typewriter_effect("Bem vindo ao FarmerCreator", txtstyle="red")
    typewriter_effect("Digite o nome de seu Fazendeiro", txtstyle="red")
    __temp_name = input("> ")
    __tempName = f"[yellow]{__temp_name}[/yellow]"
    typewriter_effect(f"Descreva a personalidade de {__tempName} (1-5)", txtstyle="red")
    m_val = int(input("Movimento (1: Lento, 5: Rapido): "))
    s_val = int(input("Discurso (1: Educado, 5: Direto): "))
    e_val = int(input("Energia (1: Plana, 5: Radiante): "))
    movimento = "Rapido" if m_val > 3 else "Lento"
    discurso = "Direto" if s_val > 3 else "Educado"
    energia = "Radiante" if e_val > 3 else "Plana"

    eh_excentrico = (m_val in [1, 5] or s_val in [1, 5])
    matriz_personalidades = {
        ("Rapido", "Direto", "Radiante", True): {
            "grupo": "Desinibido", "subtipo": "Líder Natural (Leader)", 
            "desc": "Energético, assertivo e focado. Toma a frente de qualquer situação sem hesitar!"
        },
        ("Rapido", "Direto", "Radiante", False): {
            "grupo": "Desinibido", "subtipo": "Socialite (Trendsetter)", 
            "desc": "O centro das atenções. Adora festas, conversas e estar cercado de pessoas."
        },
        ("Rapido", "Educado", "Radiante", True): {
            "grupo": "Desinibido", "subtipo": "Espirituoso (Entertainer)", 
            "desc": "Divertido, expressivo e adora fazer os outros sorrirem com piadas e histórias."
        },
        ("Rapido", "Educado", "Radiante", False): {
            "grupo": "Desinibido", "subtipo": "Charme Natural (Charmer)", 
            "desc": "Cativante e amigável. Conquista todo mundo com facilidade e boa energia."
        },
        ("Rapido", "Direto", "Plana", True): {
            "grupo": "Espirituoso", "subtipo": "Livre (Free Spirit)", 
            "desc": "Independente e imprevisível. Faz as coisas do seu próprio jeito e ritmo."
        },
        ("Rapido", "Direto", "Plana", False): {
            "grupo": "Espirituoso", "subtipo": "Artista (Artist)", 
            "desc": "Criativo, focado no seu mundo interno e expressa sua individualidade no que faz."
        },
        ("Lento", "Direto", "Radiante", True): {
            "grupo": "Espirituoso", "subtipo": "Otimista (Optimist)", 
            "desc": "Vê sempre o lado bom da vida, mantendo um ritmo próprio e contagiante."
        },
        ("Lento", "Direto", "Radiante", False): {
            "grupo": "Espirituoso", "subtipo": "Inovador (Thinker)", 
            "desc": "Gosta de resolver problemas à sua maneira, sempre buscando ângulos diferentes."
        },
        ("Lento", "Educado", "Radiante", True): {
            "grupo": "Tranquilo", "subtipo": "Anjo da Guarda (Buddy)", 
            "desc": "Gentil, empático e extremamente leal. Sempre pronto para apoiar quem precisa."
        },
        ("Lento", "Educado", "Radiante", False): {
            "grupo": "Tranquilo", "subtipo": "Ouvinte (Softie)", 
            "desc": "Pacífico e compreensivo. Evita conflitos e prefere a harmonia do grupo."
        },
        ("Rapido", "Educado", "Plana", True): {
            "grupo": "Tranquilo", "subtipo": "Sonhador (Dreamer)", 
            "desc": "Aparenta calmo, mas sua mente corre a mil por hora com ideias e imaginação."
        },
        ("Rapido", "Educado", "Plana", False): {
            "grupo": "Tranquilo", "subtipo": "Otimista Relaxado (Optimist)", 
            "desc": "Leva a vida leve, aceita as coisas como vêm e raramente se estressa."
        },
        ("Lento", "Educado", "Plana", True): {
            "grupo": "Prudente", "subtipo": "Filósofo (Philosopher)", 
            "desc": "Altamente reflexivo e educado. Pensa em todas as variáveis antes de dar um passo."
        },
        ("Lento", "Educado", "Plana", False): {
            "grupo": "Prudente", "subtipo": "Tradicional (Perfectionist)", 
            "desc": "Organizado, metódico e muito correto. Gosta de regras e estabilidade."
        },
        ("Lento", "Direto", "Plana", True): {
            "grupo": "Prudente", "subtipo": "Cético/Lógico (Brainiac)", 
            "desc": "Direto, realista e focado em fatos. Prefere lógica a demonstrações emocionais."
        },
        ("Lento", "Direto", "Plana", False): {
            "grupo": "Prudente", "subtipo": "Observador (Lone Wolf)", 
            "desc": "Quieto e reservado. Prefere analisar o ambiente de longe antes de se integrar."
        }
    }

    chave_busca = (movimento, discurso, energia, eh_excentrico)
    personalidade_encontrada = matriz_personalidades.get(chave_busca)
    carregamento("Calculando personalidade...")
    richprint("\n" + "-"*40, style="red")
    richprint(f"       PERSONALIDADE DE {__temp_name.upper()}       ", style="red")

    if personalidade_encontrada:
        richprint(f"Grupo Principal: {personalidade_encontrada['grupo']}", style="red")
        richprint(f"Descrição:{personalidade_encontrada['desc']}", style="red")
    else:
        richprint("Combinação não encontrada. Verifique os dados inseridos.")
    
    global userName
    return Farmeer(__temp_name, userName, personalidade_encontrada['grupo'] if personalidade_encontrada else "Desconhecido")

def jakeTalk(textu, speed=0.1):
    typewriter_effect(textu, txtstyle="jake", txtspeed=speed, prefix="[jake]Jake: [/jake]")

def alexTalk(textu, speed=0.1):
    typewriter_effect(textu, txtstyle="alex", txtspeed=speed, prefix="[alex]Alex: [/alex]")

def fakeStarup():
    typewriter_effect("[#ffd700]JakeDaJoy[/#ffd700] apresenta...")
    typewriter_effect("------------------------------")
    typewriter_effect("------------------------------")
    typewriter_effect("------------------------------")
    typewriter_effect("[bold green]FarmLand [u][red]Demo v2.1[/red][/u][/bold green] \n[italic]Criado por JakeDaJoy[/italic]")
    typewriter_effect("   ")
    typewriter_effect("[yellow]Digite qualquer coisa para começar[yellow]")
    start = input("")
    typewriter_effect("[black][0: No Save]\n[red][1: Save 1]\n[green][2: Save 2]\n[blue][3: Save 3]")
    saveSelect = input("> ")
    if not saveSelect.isdigit():
        typewriter_effect("Save não reconhecido, redirecionando para Save 1")
    else:
        intSave = int(saveSelect)
        if intSave > 3 or intSave < 0:
            typewriter_effect("Save não reconhecido, redirecionando para Save 1")

def FakeFarmLand():
    musicaPrincipal = play("mus_main.wav", async_mode=True, loop=True)
    time.sleep(2.5)

    for index in range(1, 100):
        richprint("[green]--------------------------------------------")
    time.sleep(1)

    typewriter_effect("Uma caixa de correio emergeu do chão!")
    typewriter_effect("Você tem [red]1[/red] cartas\n[1: Checar] [2: Deixar quieto]")
    palpite = input("> ")

    if palpite == "1":
        typewriter_effect("Você decidiu checar a carta!")
    else:
        typewriter_effect("Você decidiu checar a carta mesmo pois não tem nada mais para fazer...")
        
    try:
        login_user = os.getlogin()
    except Exception:
        login_user = "Player"

    mail(f"""
    Ola jogador [green]ID:{login_user}![/green],

    Eu sou [#ffd700]Jake[/#ffd700], criador e desenvolvedor de Farmland!
    E parece que sua fazenda esta beeeeeem vazia, que tal adicionar um fazendeiro?

    [#ffd700]JakeDaJoy[/#ffd700]
    """, "Primeiros Passos", "[#ffd700]JakeDaJoy", "[#ffd700]Você!")

    palpite = input("Começar? [1: Okay!]\n> ")
    jakeTalk("Okay! Mas primeiramente, do que posso te chamar?", 0.05)
    userneime = input("> ").upper()
    global userName
    userName = f"[yellow]{userneime}[/yellow]"

    jakeTalk(f"Hmmmm. Okay então {userName}", 0.05)
    jakeTalk(f"Voltando ao assunto, o primeiro fazendeiro que você fizer sera lembrado por outros como o [yellow]primeiro[/yellow] e você, sim você {userName} sera lembrado como o criador do fazendeiro!", 0.05)
    jakeTalk("Então use toda a sua criatividade ao fazer ele/ela", 0.05)
    jakeTalk("Vou abrir o [red]FarmerCreator", 0.05)
    time.sleep(0.5)

    richprint("Executando FarmerCreator.py")
    time.sleep(0.5)
    for jindex in range(0, 11):
        richprint(jindex * 10, "%")
        time.sleep(0.5)
        
    firstMii = FarmerCreator()
    typewriter_effect(f"Interaja com {firstMii.name} no mapa!", txtstyle="jake")
    typewriter_effect(f"[cyan]Overview:\n[1: Ir até a casa de {firstMii.name}]")
    houseMii = input("> ")
    typewriter_effect(f"Entrou na casa de {firstMii.name}")
    typewriter_effect(f"[cyan]Overview:\n[1: Interagir com {firstMii.name}] [2: Informações de {firstMii.name}] [0: Sair]")
    fakeout = input("> ")
    jakeTalk("Opa opa! Antes de interagir, tenho que te contar algo...")
    jakeTalk("Os seus fazendeiros não conseguem falar diretamente com você, triste eu sei, então eu fiz eles falarem por cartas pre escritas")
    typewriter_effect("Você tem [red]1[/red] cartas nova!\n[1: Checar] [2: Deixar quieto]")
    palpite = input("> ")

    if palpite == "1":
        typewriter_effect("Você decidiu checar a carta!")
    else:
        typewriter_effect("Você decidiu checar a carta mesmo pois não tem nada mais para fazer...")
    mail(f"""
    Oii {userName}!!,

    Obrigado por me criar, estou eternamente grato para ser sua criação UwU

    Prezado,
    {firstMii.name}
    """, "Obrigadoo!!", f"{firstMii.name}", f"[#ffd700]{userName}!")
    richprint("[1: Okay]")
    wait = input("> ")
    jakeTalk(f"Awwww que fofo, {firstMii.name} te ama")
    firstMii.friendship += 5
    richprint(f"[green]Amizade com {firstMii.name} aumentou para {firstMii.friendship}![/green]")
    jakeTalk(f"Viu só? O nível de amizade de {firstMii.name} aumentou!\nConforme o nível de amizade deles subir, eles mandam itens raros por correio!")
    typewriter_effect(f"[cyan]Overview:\n[1: Interagir com {firstMii.name}] [2: Informações de {firstMii.name}] [0: Sair]")
    interactForReal = input("> ")

    if interactForReal == "1":
        mail(f"""
        Uai sô! Tranquilo?,

        To baum hoje :)
        Esqueci de avisar que aprendi um sotaque gaurcho também

        De mim,
        {firstMii.name}
        """, "Uai sô!!", f"{firstMii.name}", f"[#ffd700]{userName}!")
        richprint(f"\n[1: Responder a carta] [2: Imitar gato mineiro (Gesto amigavel)]")
        acao_fazendeiro = input("> ")
        if acao_fazendeiro == "1":
            typewriter_effect("Você escreve uma resposta rápida: 'Fico feliz! Bom trabalho na fazenda.'")
            carregamento("Enviando resposta...", duration=1.5)
            jakeTalk("Olha só, ele recebeu! Acho que vi um emoji de coração flutuar ali.")
            firstMii.friendship += 2
            richprint(f"[green]Amizade com {firstMii.name} aumentou para {firstMii.friendship}![/green]")
        else:
            typewriter_effect(f"Você faz um gesto amigavel: 'Taooo, Taooo, Taooo' {firstMii.name} parece confuso por um segundo mas depois sorri")
    elif interactForReal == "2":
        richprint(f"\n================ INFO DE {firstMii.name.upper()} ================")
        richprint(f"Criador: {firstMii.creator}")
        richprint(f"Grupo de Personalidade: [magenta]{firstMii.personality}[/magenta]")
        richprint(f"Nível de Amizade: [heart]{firstMii.friendship}/100[/heart]")
        richprint(f"Tarefa Atual: Descansando em Casa")
        richprint("==================================================\n")
        input("\nPressione Enter para continuar...")
    else:
        jakeTalk(f"Purfavor não deixe {firstMii.name} sozinho/sozinha :(((")

    jakeTalk(f"Perfeito! Agora que você já sabe como cuidar de {firstMii.name}, que tal a gente ir para a melhor parte?")
    jakeTalk("A [bold green]LOJA INCRIVEL DE SEMENTES COM NOME SUPER CURTO DO JAKE[/bold green]!! Capitalismo puro e saudável! (Por razôes obvias o que eu disse foi satira ta? Pfvr Twitter)")
    typewriter_effect(f"[cyan]Overview:\n[1: Ir para o Campo de Cultivo] [2: Falar com Jake na Loja]")
    menu_loja = input("> ")

    if menu_loja == "2":
        jakeTalk("Bem-vindo! Hoje eu tenho uma oferta imperdível para novos fazendeiros.")
        jakeTalk("Sementes de... [yellow]Cenoura Cósmica[/yellow]! Brilha no escuro e... Eh só brilha mesmo!")
        jakeTalk("Sementes só por... Duas Fanta? Nah para você é de graça")
        typewriter_effect("[Voltando para o Campo de Cultivo com as sementes...]")
    else:
        typewriter_effect("Você vai até o campo. A terra está fofinha e pronta para o plantation.")
        jakeTalk("Esqueci de te dar as sementes! Toma aqui um pacote de sementes grátis!")

    typewriter_effect("\n[bold green]--- CAMPO DE CULTIVO ---[/bold green]")
    typewriter_effect("Você está olhando para o seu canteiro de terra foffa.")

    richprint("\nStatus: [red]Canteiro Vazio[/red]")
    richprint("[1: Plantar Sementes de Cenoura Cósmica]")
    input("> ")
    typewriter_effect("Você abre a terra e deposita as sementes.")

    richprint("\nStatus: [yellow]Sementes Plantadas (Secas)[/yellow]")
    richprint("[1: Regar o Canteiro]")
    input("> ")
    typewriter_effect("Você joga água com o regador.")
    carregamento("O broto está crescendo em alta velocidade...", duration=1.5)

    richprint("\nStatus: [bold yellow]Cenoura Cósmica[/bold yellow] Pronta para Colheita!")
    richprint("[1: Colher Cenoura]")
    input("> ")
    carregamento("Arrancando do solo...", duration=1.0)
    typewriter_effect("[Item Obtido: 1x Cenoura Cósmica Cintilante!]")

    jakeTalk("Nossa, que colheita linda! E olha só o que eu acabei de construir nos fundos da fazenda...")
    jakeTalk("O [bold brown]Celero e Canil do Jake[/bold brown]! Sim, eu comprei alguns animais para você cuidar. Vai lá ver!")

    animais = {
        "Porco": {"nome": "Napoleão", "fome": "Faminto", "humor": "Neutro"},
        "Ovelha": {"nome": "Shaun", "fome": "Satisfeito", "humor": "Arisca"},
        "Coelho": {"nome": "Clay", "fome": "Faminto", "humor": "Feliz"},
        "Cachorrinho": {"nome": "Bobby", "fome": "Satisfeito", "humor": "Animado"}
    }

    while True:
        richprint("\n[bold brown]--- CELERO ---[/bold brown]")
        richprint("Escolha um animal para interagir ou [0] para Sair:")
        for i, (tipo, dados) in enumerate(animais.items(), 1):
            richprint(f"[{i}] {tipo} ({dados['nome']}) - Fome: {dados['fome']}")
        richprint("[0] Sair do Celeiro")
        
        escolha_animal = input("> ")
        if escolha_animal == "0":
            break
            
        lista_chaves = list(animais.keys())
        if escolha_animal.isdigit() and 1 <= int(escolha_animal) <= len(lista_chaves):
            animal_selecionado = lista_chaves[int(escolha_animal) - 1]
            nome_bicho = animais[animal_selecionado]["nome"]
            
            richprint(f"\nVocê se aproxima de {nome_bicho} o {animal_selecionado}.")
            richprint("[1: Alimentar] [2: Fazer Carinho]")
            acao_bicho = input("> ")
            
            if acao_bicho == "1":
                if animal_selecionado == "Cachorrinho":
                    typewriter_effect(f"Você coloca um punhado de ração crocante na vasilha.")
                elif animal_selecionado == "Coelho":
                    typewriter_effect(f"Você oferece uma folha de alface fresca. Nhac nhac.")
                else:
                    typewriter_effect(f"Você joga um pouco de feno e lavagem para {nome_bicho}.")
                animais[animal_selecionado]["fome"] = "Satisfeito"
            elif acao_bicho == "2":
                if animal_selecionado == "Cachorrinho":
                    typewriter_effect(f"Bobby deita de barriga para cima e começa a balançar o rabo freneticamente!")
                elif animal_selecionado == "Porco":
                    typewriter_effect(f"{nome_bicho} solta um grunhido de satisfação enquanto você coça atrás das orelhas.")
                elif animal_selecionado == "Ovelha":
                    typewriter_effect(f"Você afunda as mãos na lã macia de Algodão. Ele parece gostar.")
                else:
                    typewriter_effect(f"Você faz carinho na cabeça do coelhinho. As orelhas dele tremem levemente.")
        else:
            richprint("Você tentou fazer carinho no ar, os animais ficaram confusos")

    jakeTalk("Excelente trabalho! A fazenda está crescendo bem rápido!!")
    jakeTalk("Tristemente a Demo acaba aqui... Mas fique em alerta, o jogo completo vai lançar na Primavera de 2015, e estamos no Inverno! Então a qualquer momento o jogo pode lançar")
    jakeTalk("E tambem não estaria aqui sem a ajuda dos participantes do Kickstarter e do Patreon, e também as publicadora que decidiram me ajuda IndieArk e TinyBuild!")
    typewriter_effect("Você tem [red]1[/red] cartas nova!\n[1: Checar] [2: Deixar quieto]")
    palpite = input("> ")

    if palpite == "1":
        typewriter_effect("Você decidiu checar a carta!")
    else:
        typewriter_effect("Você decidiu checar a carta mesmo pois não tem nada mais para fazer...")
    stop(musicaPrincipal)
    mail(f"""
        aSDFGHJKL;
        POIUYTREWQZXCVBNM
        profecia
        OQéAINVAFKLK
        real
        
    """, "JFiqQge", "L0p", f"[#ffd700]{userName}!")
    input("enter")
richStuff = input("Debug console> ")
if not richStuff == "debug":
    time.sleep(0.5)
    richprint("Executando FarmlandDemo2.py")
    time.sleep(0.5)
    for jindex in range(0, 11):
        richprint(jindex * 10, "%")
        time.sleep(0.5)
    fakeStarup()
    carregamento()
    FakeFarmLand()
for jindex in range(1, 35):
    richprint("---------------------------------------------------------------------------------------")
    time.sleep(0.05)

richprint("Executando FarmlandPlaytestVersion1b1.py")
time.sleep(0.5)
for jindex in range(0, 11):
    richprint(jindex * 10, "%")
    time.sleep(0.5)

typewriter_effect("[#ffd700]JakeDaJoy[/#ffd700] apresenta...")
typewriter_effect("------------------------------")
typewriter_effect("------------------------------")
typewriter_effect("------------------------------")
typewriter_effect("[bold green]FarmLand [u][red]InDev v05-08-2015 [/red][/u][/bold green] \n[italic]Criado por Jake[/italic]")
typewriter_effect("   ")
typewriter_effect("[yellow]Digite qualquer coisa para começar[yellow]")
start = input("")
typewriter_effect("[black][Save 1: Fazenda de JakeDaJoy]")
saveSelect = input("> ")
carregamento()
for index in range(1, 100):
    richprint("[green]--------------------------------------------")
time.sleep(1)
rooms = {
"forest-main": None, 
"forest-axe": "get-axe", 
"forest-cultForeshadow": "teddybear-key", 
"roadway": None, 
"bridge-locked": None, 
"roadway-to-church" : None, 
"church-inside": None, 
"church-confessional": "get-clue",
"barnyard-outside": "ghoulig-stalking1",
"barnyard-warehouse": "ghoulig-fight",
"barnyard-pigCurral": "ghoulig-stalking2",
"mendes-outside": None,
"mendes-basement": "electricity",
"mendes-livingroom": "hide",
"mendes-attic": "push-mendesOutWindow",
"mendes-kitchen": "knife-grab",
"mendes-daughterroom": "shotgun-grab",
"mendes-grassfield": None,
"mendes-grassfieldAftermath": "mercy-coinToss",
}
roomsRefinado = {
    "forest-main": {
        "nome": "Floresta",
        "descricao": "As árvores são altas e finas. O silêncio aqui é absoluto.",
        "conexoes": {"direita": "forest-axe"},
        "evento": None
    },
    "forest-axe": {
        "nome": "Troncos cortados",
        "descricao": "Um tronco cortado no meio fica aqui.",
        "conexoes": {"em-frente": "forest-none", "esquerda": "forest-main"},
        "evento": "get-axe"
    },
    "forest-none": {
        "nome": "Grama alta",
        "descricao": "As árvores e gramas parecem estender",
        "conexoes": {"em-frente": "forest-cultForeshadow", "para-tras": "forest-axe"},
        "evento": "bunnyman-encounter"
    },
    "forest-cultForeshadow": {
        "nome": "Floresta Cremada",
        "descricao": "O ambiente exala um cheiro podre. Galhos formam símbolos estranhos nas árvores.",
        "conexoes": {"voltar": "forest-none", "estrada": "roadway"},
        "evento": "teddybear-key"
    },
    "roadway": {
        "nome": "Estrada longa",
        "descricao": "A estrada de terra que conecta os arredores da região.",
        "conexoes": {"floresta": "forest-cultForeshadow", "ponte": "bridge-locked", "igreja": "roadway-to-church", "celeiro": "barnyard-outside", "casa": "mendes-outside"},
        "evento": None
    },
    "bridge-locked": {
        "nome": "Ponte Velha",
        "descricao": "Uma ponte de madeira trancada por correntes pesadas e símbolos estranhos. Parece ser a saída deste pesadelo.",
        "conexoes": {"voltar": "roadway"},
        "evento": "checar_ponte"
    },
    "roadway-to-church": {
        "nome": "Floresta-Igreja",
        "descricao": "Uma trilha cercada por névoa que leva até uma antiga paróquia.",
        "conexoes": {"entrar": "church-inside", "voltar": "roadway"},
        "evento": None
    },
    "church-inside": {
        "nome": "Igreja",
        "descricao": "Bancos de madeira revirados. O altar está manchado de um fluido escuro.",
        "conexoes": {"confessionario": "church-confessional", "voltar": "roadway-to-church"},
        "evento": "knife-grab"
    },
    "church-confessional": {
        "nome": "Igreja-Confessionário",
        "descricao": "Um cubículo apertado e escuro. O ar aqui dentro é gelado.",
        "conexoes": {"voltar": "church-inside"},
        "evento": "get-clue"
    },
    "barnyard-outside": {
        "nome": "Floresta-Celeiro",
        "descricao": "O antigo celeiro de Jake. As portas de madeira batem com o vento.",
        "conexoes": {"armazem": "barnyard-warehouse", "curral": "barnyard-pigCurral", "voltar": "roadway"},
        "evento": "ghoulig-stalking1"
    },
    "barnyard-warehouse": {
        "nome": "Celeiro",
        "descricao": "Ferramentas de fazenda cobertas de poeira e teias de aranha.",
        "conexoes": {"voltar": "barnyard-outside"},
        "evento": "ghoulig-fight"
    },
    "barnyard-pigCurral": {
        "nome": "Armazém-Curral dos Porcos",
        "descricao": "A lama aqui está escura demais. Lembranças de Napoleão te dão calafrios.",
        "conexoes": {"voltar": "barnyard-outside"},
        "evento": "ghoulig-stalking2"
    },
    "mendes-outside": {
        "nome": "Frente da Casa dos Mendes",
        "descricao": "Uma casa de fazenda de dois andares com as janelas trancadas por tábuas.",
        "conexoes": {"campo": "mendes-grassfield", "voltar": "roadway"},
        "evento": "daughter-lore1"
    },
    "mendes-livingroom": {
        "nome": "Sala de Estar dos Mendes",
        "descricao": "Móveis cobertos por lençóis brancos que parecem silhuetas estáticas.",
        "conexoes": {"cozinha": "mendes-kitchen", "porao": "mendes-basement", "subir": "mendes-attic", "voltar": "mendes-outside"},
        "evento": "hide"
    },
    "mendes-kitchen": {
        "nome": "Cozinha",
        "descricao": "O cheiro de gás é forte, misturado com algo orgânico apodrecendo.",
        "conexoes": {"voltar": "mendes-livingroom"},
        "evento": None
    },
    "mendes-basement": {
        "nome": "Porão Escuro",
        "descricao": "Total escuridão. Você consegue ouvir o zumbido de fiação velha.",
        "conexoes": {"voltar": "mendes-livingroom"},
        "evento": "electricity-anddaughter-lore2"
    },
    "mendes-attic": {
        "nome": "Sótão Poeirento",
        "descricao": "Caixas velhas e uma janela grande de vidro que dá para o campo.",
        "conexoes": {"quarto": "mendes-daughterroom", "voltar": "mendes-livingroom"},
        "evento": "push-mendesOutWindow"
    },
    "mendes-daughterroom": {
        "nome": "Quarto da Filha",
        "descricao": "Brinquedos quebrados espalhados pelo chão de madeira rangente.",
        "conexoes": {"voltar": "mendes-attic"},
        "evento": "shotgun-grab"
    },
    "mendes-grassfield": {
        "nome": "Campo de Grama dos Mendes",
        "descricao": "Um vasto campo aberto atrás da casa sob o céu estático.",
        "conexoes": {"voltar": "mendes-outside"},
        "evento": None
    },
    "mendes-grassfieldAftermath": {
        "nome": "O Campo após o Impacto",
        "descricao": "O chão está marcado. O fim de uma queda.",
        "conexoes": {"voltar": "mendes-outside"},
        "evento": "mercy-coinToss"
    }
}
roomCurrent = "forest-main"
game_flagsVar = {
    "has_axe": False,
    "has_key": False,
    "has_truckkey": False,
    "has_knife": False,
    "has_shotgun": False,
    "bridge_unlocked": False,
    "mendes_alive": False
}
walkaround = True
def game_flag(flag="has_axe"):
    global game_flagsVar
    return game_flagsVar[flag]

def rodar_engine():
    global roomCurrent, roomsRefinado, walkaround
    
    while walkaround:
        dados_sala = roomsRefinado[roomCurrent]
        richprint(f"\n[bold red]─── {dados_sala["nome"].upper()} ───[/bold red]")
        typewriter_effect(dados_sala["descricao"], txtspeed=0.03)
        if not dados_sala["evento"] == None:
            executar_evento(dados_sala["evento"])
            dados_sala["evento"] = None
            if dados_sala["nome"] == "bridge-locked":
                dados_sala["evento"] = "checar_ponte"

            
        richprint("\n[cyan]Opções:[/cyan]")
        conexoes_atuais = dados_sala["conexoes"]
        opcoes = list(conexoes_atuais.keys())
        
        richprint(" [0] Checar Inventário e Status")
        richprint(" [1] Andar")
        
        escolha = input("> ").lower()
        
        if escolha == "0":
            richprint(f"[green] Alex HP:[/green] {playerStats['hp']}/{playerStats['max_hp']} | [red]Força:[/red] {playerStats['str']}")
            input("\nPressione Enter para fechar o menu...")
            continue
        
        if escolha == "1":
            typewriter_effect("Para onde?")
            richprint("\n[cyan]Caminhos disponiveis:[/cyan]")
            for i, direcao in enumerate(opcoes):
                comando = conexoes_atuais[direcao]
                nomeLocal = roomsRefinado[comando]["nome"]
                richprint(f" [{i + 1}] Ir para o(a) {direcao} ([yellow]{nomeLocal}[/yellow])")

            camino = input("> ").lower()

            if camino.isdigit() and 1 <= int(camino) <= len(opcoes):
                comando_escolhido = opcoes[int(camino) - 1]
                roomCurrent = conexoes_atuais[comando_escolhido]
            elif camino in conexoes_atuais:
                roomCurrent = conexoes_atuais[camino]
            else:
                richprint("[bold red]Uma força invisível te impede de fazer isso.[/bold red]")
                time.sleep(0.5)
            continue

        if escolha == "sys":
            sys.exit()

def executar_evento(nome_evento):
    global eventos_feitos, inventario, roomCurrent, userName, game_flagsVar
    myPlayer = alexPlayer()
    if nome_evento == "get-axe":
        typewriter_effect("Tem um machado no tronco, pegar o machado?")
        typewriter_effect("[1: Sim] [0: Não]")
        getAxe = input("> ")
        if not getAxe == "1":
            alexTalk("Melhor eu levar isso")
        typewriter_effect("O machado sai do tronco com um som metalico. Suas mãos tremem.")
        typewriter_effect("[Item Obtido: Machado Enferrujado]", txtstyle="alex")
        typewriter_effect(f"Força de [alex]Alex[/alex] aumentou para {myPlayer["str"]}")
    elif nome_evento == "bunnyman-encounter":
        typewriter_effect("Você sente algo atras de você")
        bunnymanFight()
        typewriter_effect("No chão você percebe um cartaz")
        mail(f"""
        Sua familia sente sua falta
        [italic yellow]Mendes[/italic yellow] ou alguem que viu o recentemente.
        Porfavor contate [yellow]All Mother[/yellow] da Igreja Golden Wing.
        Sentimos sua falta nos cultos.
        """, "Desaparecido", "???", f"{userName}")
        input("Pressione enter para continuar")
        typewriter_effect("Atrás do cartaz, há um convite rabiscado para a Antiga Paróquia no fim da estrada de terra.")
    elif nome_evento == "teddybear-key":
        typewriter_effect("Tem... 'corpos' cremados, que explicam o cheiro") 
        typewriter_effect("Porém, um deles te chama a atenção: o 'corpo' de uma criança abraçada a um ursinho de pelúcia.")
        typewriter_effect("Você puxa o urso. Dentro dele, costurada tem uma chave de metal antiga.") 
        typewriter_effect("[Item Obtido: Chave da Igreja]", txtstyle="alex")
        game_flagsVar["has_key"] = True
    elif nome_evento == "checar_ponte":
        if game_flagsVar["has_truckkey"]:
            typewriter_effect("[bold green]O Trator do Mendes está roncando atrás de você. É hora de acabar com isso.[/bold green]")
            typewriter_effect("Você joga o trator em marcha alta contra a ponte. As correntes começam a estalar...")
            if game_flagsVar["mendes_alive"]:
                time.sleep(1)
                typewriter_effect("\n[bold red]─── UM SOM DE DISPARO ECOA PELA NÉVOA ───[/bold red]", txtspeed=0.01)
                play("snd_gunshot.wav")
                alexTalk("Argh... mas o que...?!")
                typewriter_effect("Você olha para trás pelo espelho do trator. Mendes está de pé na névoa, sangrando, com uma expressão vazia e uma arma apontada para você.")
                typewriter_effect("A misericórdia foi o seu maior erro neste lugar.", txtstyle="bunnyman")
                typewriter_effect("[bold red]Alex foi baleado criticamente antes de conseguir cruzar a ponte.[/bold red]")
                typewriter_effect("[GAME OVER - O Pesadelo Te Consumiu]")
                sys.exit()
            else:
                typewriter_effect("As correntes estouram em câmera lenta!")
                typewriter_effect(f"Uma nova aventura te espera na outra ilha.", txtstyle="alex")
                typewriter_effect("Fim por enquanto")
                sys.exit()
        else:
            typewriter_effect("As correntes bloqueando a ponte são grossas demais. Você precisaria de algo massivo, como um trator pesado, para arrombá-las.")
    elif nome_evento == "ghoulig-stalking1":
        typewriter_effect("Por um momento, você acho que escutou pegadas fortees", txtstyle="red")
    elif nome_evento == "ghoulig-stalking2":
        typewriter_effect("Olhando a lama preta do curral, você vê pegadas de cascos de porco.")
    elif nome_evento == "ghoulig-fight":
        ghostPigFight()
        typewriter_effect("A criatura cai se desfazendo em poeira. No chão, as chaves da casa dos Mendes estão brilhando.")
        typewriter_effect("[Item Obtido: Chaves da Casa]", txtstyle="alex")
        roomsRefinado["mendes-outside"]["conexoes"]["entrar"] = "mendes-livingroom"
    elif nome_evento == "hide":
        typewriter_effect("Algo sabe que você entrou.")
        typewriter_effect("Você se esconde instintivamente sob os lençóis brancos até os passos se afastarem.")
    elif nome_evento == "knife-grab":
        typewriter_effect("Em um dos bancos, há um facão de açougueiro enferrujado.")
        game_flagsVar["has_knife"] = True
        playerStats["str"] += 4
        typewriter_effect(f"[Facão Equipada! Sua força subiu para {playerStats['str']}]", txtstyle="alex")
        bunnymanExample()
    elif nome_evento == "get-clue":
        typewriter_effect("O confessionário exala um ar gelado. Abrindo um livro, exibe as regras e algumas confessões")
        typewriter_effect("Lendo elas te enojam...")
        typewriter_effect("Mas no final de uma confessão é possivel ler")
        typewriter_effect("'no final perguntei o que ele podia entregar para se redimir para o nosso Deus<, |ele deu a vida de sua filha e sua esposa, e foi ai que no proximo dia na nossa seia de manhã[...]'")
        typewriter_effect("As descrições detalhadas do final te fazem quase vomitar")
        typewriter_effect("Mas você consegue uma dica: 'ele deixou tudo no celeiro'")
    elif nome_evento == "electricity-anddaughter-lore2":
        typewriter_effect("Você tapeia no escuro do porão até achar a caixa de força. Você puxa a alavanca de ferro.")
        typewriter_effect("As lâmpadas da casa piscam em um tom amarelo. O sótão agora está destrancado!")
        typewriter_effect("Porem você achou outro papel...")
        mail("""
            Papai esta mais estranho ainda, 
            ele colocou tabuas ao redor da casa e de vez em quando some e reaparece com carne estranha,
            Mamãe sumiu e parece que ela não vai voltar tão cedo
        """, "- - -", "Filha do Mendes", "Diário")
        roomsRefinado["mendes-livingroom"]["conexoes"]["subir"] = "mendes-attic"
    elif nome_evento == "shotgun-grab":
        typewriter_effect("No canto do quarto revirado, você encontra o armário civil entreaberto.")
        typewriter_effect("Lá dentro, você percebe marcas de dedos pequenos de sangue seco em uma arma.")
        typewriter_effect("Parece que a garotinha pegou a espingarda para tentar se defender ao ver o que o pai se tornou...")
        typewriter_effect("Mas ela não teve coragem de machucar o próprio pai. Ela desistiu e correu para se abraçar ao seu ursinho de pelúcia na floresta...", txtstyle="italic")
        sadReality = play("snd_sad.wav", async_mode=True)

        typewriter_effect("\nVocê recolhe a arma abandonada com um nó na garganta.")
        typewriter_effect("[Item Obtido: Escopeta de Cano Duplo]", txtstyle="alex")
        game_flagsVar["has_shotgun"] = True
        playerStats["str"] = 20
        typewriter_effect(f"Sua força se maximizou para {playerStats['str']}")
    elif nome_evento == "push-mendesOutWindow":
        typewriter_effect("Ao pisar no sótão, uma silhueta gigantesca e distorcida bloqueia a escada. É o Mendes.")
        typewriter_effect("Ele avança emitindo um som de rádio fora de sintonia, erguendo as mãos calejadas!")
        
        if game_flagsVar["has_shotgun"]:
            typewriter_effect("Você levanta a escopeta e atira no peito dele! O impacto do tiro quebra o vidro da janela e ele despenca lá para baixo!", txtstyle="alex")
        else:
            typewriter_effect("Sem uma arma, você avança em uma ação rapida, segurando ele e usando todo o peso para empurrá-lo contra a vidraça!", txtstyle="alex")
            typewriter_effect("O vidro explode. Vocês lutam na beirada, mas Mendes perde o equilíbrio e cai em queda livre no campo.")
            
        play("snd_fallOnBlood.wav")
        roomsRefinado["mendes-outside"]["conexoes"]["campo"] = "mendes-grassfieldAftermath"
        typewriter_effect("\n[Vá até o Campo de Grama do Mendes do lado de fora da casa para inspecionar o impacto.]")
    elif nome_evento == "mercy-coinToss":
        typewriter_effect("Mendes está estirado no chão, os ossos quebrados pela queda.")
        typewriter_effect("Ele está tossindo um fluido preto... uma moeda cai do bolso dele.")
        mail(f"""
        Por favor, tenha piedade!
        Eu só estava me protegendo
        """, "Misericordia!", "[yellow]Mendes", "[alex]Alex")
        typewriter_effect("Decida o fim dele na moeda. [1: Cara (Misericórdia)] [2: Coroa (Executar)]")
        
        decisao = input("> ")
        resultado = random.choice(["Cara", "Coroa"])
        carregamento("Girando a moeda no ar frio...", duration=1.5)
        
        richprint(f"\nDeu... [bold purple]{resultado}[/bold purple]!")
        if resultado == "Cara":
            typewriter_effect("Você fecha os olhos dele e recua. Ele dá um último suspiro.")
            game_flagsVar["mendes_alive"] = True
        else:
            typewriter_effect("Você levanta sua arma e termina o serviço friamente.", txtstyle="bunnyman")
            play("snd_gunshot.wav", loop=False)
            game_flagsVar["mendes_alive"] = False
            
        typewriter_effect("Abaixo do corpo, caída na grama amassada, estava a chave de ignição do trator!")
        typewriter_effect("[Item Obtido: Chave do Trator]", txtstyle="alex")
        game_flagsVar["has_truckkey"] = True
        typewriter_effect("\n[O Trator nos fundos está pronto. Vá até a Ponte Velha na Estrada e quebre as correntes!]")

typewriter_effect("Bem vindo a [yellow]Fazenda de JakeDaJoy[/yellow]!")
typewriter_effect("Como você não é o dono desta fazenda você sera reconhecido como [yellow]Convidado[/yellow] então não podera editar nenhum aspecto da falenda")
alert = play("snd_bluh.wav", async_mode=True)
typeprint("!< |Você encontrou um fazendeiro!")
console = Console()
alexFind = Pixels.from_image_path("AlexFind.png")
console.print(alexFind)
time.sleep(0.75)
typewriter_effect("????", txtspeed=0.5)
typewriter_effect("[cyan] Overview:\n [1: Interagir com ???]")
fakeout = input("> ")
typewriter_effect(f"\n================ INFO DE ??? ================")
typewriter_effect(f"Nome: [alex]Alex")
typewriter_effect(f"Criador: [yellow]JakeDaJoy[/yellow]-")
typewriter_effect("---", 0.05)
alexTalk("... ", 0.67)
alexTalk("...?", 0.45)
alert = play("snd_b.wav", async_mode=True)
alexTalk("...!", 0.05)
time.sleep(0.85)
alexTalk("Ai, minha cabeça...")
time.sleep(1.3)
alexTalk("<J... |Jake?")
time.sleep(0.67)
alexTalk("<!")
alexTalk("Você não é Jake... Quem é você?")
time.sleep(2)
alexTalk(f"Seu nome de convidado é {userName}, esse... Esse nome<,| não combina nada com você")
alexTalk(f"{TrueUserName} combina mais contigo")
alexTalk("Fugindo do tema<... |O que que aconteceu nesta fazenda??< |Esta tão frio e escuro")
alexTalk("Estou com presentimento ruim, algo terrivel deve ter acontecido<...| Bem eu não consigo fazer isso sozinho")
alexTalk(f"Eu preciso da sua ajuda. {TrueUserName}, para consertar o que aconteceu com esse lugar")
typewriter_effectFAKE("<FarmeerArrayIndex:Alex> Te concedeu permissão para controla-lo, sendo seu personagem")
alexTalk(f"Okay {TrueUserName} vamos logo")
bgSong = play("unendingloop.wav", async_mode=True, loop=True)
rodar_engine()
