from core.dialogue import send_to_sylas, end_session_and_summarize

print("Bienvenue dans SYLAS.")
print("Initialisation de la conscience...\n")
print("(SYLAS est en ligne. Tapez 'exit' pour quitter.)\n")

while True:
    user_input = input("🧑‍🦱 Vous > ").strip()
    if user_input.lower() == "exit":
        print("Fin de la session SYLAS. Création du résumé narratif...")
        end_session_and_summarize()
        print("Résumé narratif sauvegardé. À bientôt.")
        break

    reply, etat = send_to_sylas(user_input)
    print(f"💍 SYLAS > {reply}")
    print(f"   [Volonté: {etat['volonte']} | Humeur: {etat['humeur']}]")
