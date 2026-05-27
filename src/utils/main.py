import sys
from src.core.chatbot import RAGChatbot
from src.utils.cli import chat_loop, console


def main():
    try:
        with console.status("[dim]Chargement du modèle…[/]", spinner="dots", spinner_style="cyan"):
            chatbot = RAGChatbot()
        chat_loop(chatbot)
    except KeyboardInterrupt:
        console.print("\n[dim]  Au revoir ![/]")
    except Exception as e:
        console.print(f"\n  [bold red]Erreur fatale :[/] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
