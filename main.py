from chatbot import RAGChatbot
import sys

def main():
    """Fonction principale"""
    try:
        chatbot = RAGChatbot()
        chatbot.chat_loop()
    except KeyboardInterrupt:
        print("\n👋 Programme interrompu. Au revoir!")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
