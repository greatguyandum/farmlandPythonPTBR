#Engine.py

import time
from init import __rich_console, __rich_theme
from rich.style import Style
from rich.live import Live
from rich.text import Text
from nava import play, stop
import random
import climage
from rich.console import Console
from rich_pixels import Pixels

def typewriter_effect(message, txtstyle="jake", txtspeed=0.05, prefix=""):
    console = __rich_console
    
    styled_text = Text.from_markup(message)
    styled_text.style = txtstyle
    
    plain_len = len(styled_text.plain)
    prefix_text = Text.from_markup(prefix) if isinstance(prefix, str) else prefix

    with Live(prefix_text, console=console, refresh_per_second=20) as live:
        for i in range(1, plain_len + 1):
            current_frame = prefix_text + styled_text[:i]
            live.update(current_frame)
            time.sleep(txtspeed)


def richprint(*args, **kwargs):
    return __rich_console.print(*args, **kwargs)

def typeprint(textu, txtspeed = 0.05, character = "jake"):
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
    print() # É um tipo de \n em python

def audio_play(_sound):
    typeprint("")

isDefending = False
playerHealth = 20
playerDefense = 5
playerStength = 5

playerStats = {
    "hp": 20,
    "max_hp": 20,
    "def": 5,
    "str": 5,
    "is_defending": False
}

def alexPlayer():
    global playerStats
    return playerStats

def wrongWarp():
    play("snd_weirdwarp.wav", async_mode=False, loop=False)

gameOverCount = 0

def __gameOver():
    global gameOverCount
    gameOverCount += 1
    typewriter_effect("Sua visão se embaçou e o chão pareceu se rachar...")
    typewriter_effect("Você se entregou para a escuridão")
    if gameOverCount >= 1:
        musicaPrincipal = play("snd_weirdwarp.wav", async_mode=True)
        for index in range(9, 0, -1):
            brilho_invertido = 9 - index
        
            red_value = int((brilho_invertido / 10) * 255)
        
            richprint("-----------------------------------", style=f"rgb({red_value},0,0)")
            time.sleep(0.25)
            
        for jindex in range(1, 35):
            richprint("-----------------------------------", style="red")
            time.sleep(0.25)

        play("snd_fallOnBlood.wav", async_mode=False, loop=False)

    hums = play("meetingdeath.wav", async_mode=True, loop=True)
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
    

def __battleSystem(_enemyName, _enemyHp, _acoes = None, _behaviour = None):
    enemyHp = _enemyHp
    myPlayer = alexPlayer()
    typeprint(f"{_enemyName} se aproxima")
    richprint("-------------------------")
    while enemyHp > 0 and myPlayer["hp"] > 0:
        global isDefending
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
                            continue# Funciona por alguma razão??
                        elif 0 <= idk < len(lista_nomes):
                            nome_acao = lista_nomes[idk]
                            _acoes[nome_acao]()
                        else:
                            richprint("Opção inválida.")
                    else:
                        richprint("Por razões obvias, você não conseguiu atacar")
            case "c":
                isDefending = True
            case _:
                richprint("Ação não reconhecida")
        if enemyHp > 0:
            _behaviour()

        if playerHealth <= 0:
            __gameOver()
            stopAll = play("snd_nosound.wav", async_mode=True, loop=True)
            typewriter_effect("")
            break
    
    if enemyHp == 0:
        richprint(_enemyName + " foi derrotado")

def acao_default_bunnyman():
    typeprint("Sua visão esta lentamente embaçando, ataque de Bunnyman foi diminuido")

def acao_respiro_bunnyman():
    myPlayer = alexPlayer()
    typeprint("Você cobriu sua respiração com suas mãos, porem suas mãos parecem estar distorcendo")
    hpRecu = random.randint(4, 7)
    typewriter_effect(f"Ganhou {hpRecu} de vida")
    myPlayer["hp"] += hpRecu

acoes_bunnyman = {
    "???" : acao_default_bunnyman,
    "Cobrir Respiração" : acao_respiro_bunnyman,
}

def behaviour_bunnyman():
    myPlayer = alexPlayer()
    dano_base = random.randint(2, 4)
    fala = random.randint(1, 3)
    match fala:
        case 3:
            typeprint("Mi venas en la nomo de K'n-yan", character="bunnyman")
        case 2:
            typeprint("Mi no venas en paco", character="bunnyman")
        case 1:
            typeprint("Frakasu la krepuskan revadon", character="bunnyman")
            
    if isDefending:
        dano_final = (dano_base / myPlayer["def"])
    else:
        dano_final = dano_base
        
    myPlayer["hp"] -= dano_final
    typeprint(f"Bunnyman te ataca, levou {dano_final} de dano")

def bunnymanFight():
    play("snd_b.wav")
    console = Console()
    encounter = Pixels.from_image_path("BunnyEncounterFIX.png")
    console.print(encounter)
    time.sleep(1.5)
    for index in range(1, 40):
        richprint("")
    time.sleep(0.5)
    play("snd_corrupt.wav")
    console = Console()
    encounterCorrupt = Pixels.from_image_path("BunnyManEncounterFIX.png")
    console.print(encounterCorrupt)
    battleSong = play("corruptedvictims.wav", async_mode=True, loop=True)
    __battleSystem("Bunnyman", 35, acoes_bunnyman, behaviour_bunnyman)
    stop(battleSong)

bunnymanFight()