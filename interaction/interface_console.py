# interaction/interface_console.py

from core.dialogue import send_to_sylas

def interface_console():
    while True:
        user_input = input("🧑‍🦱 Vous > ")
        if user_input.lower() in ["exit", "quit"]:
            print("Fin de la session SYLAS.")
            break
        
        reply, meta = send_to_sylas(user_input)
        print(f"💍 SYLAS > {reply}")
        print(f"   [Volonté: {meta['volonte']} | Humeur: {meta['humeur']}]")
