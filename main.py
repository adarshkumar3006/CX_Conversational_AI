"""
CLI demo for Groq + PDF RAG with User Context
Features: Load PDF, create users, select user, ask personalized questions
"""

import os
from dotenv import load_dotenv
from rag_groq import SimpleRAG

load_dotenv()


def print_help():
    """Print help message."""
    print("\n" + "=" * 60)
    print("📄 Groq + PDF RAG with User Context - CLI Demo")
    print("=" * 60)
    print("\nAvailable commands:")
    print("  load <path>           - Load a PDF file")
    print("  create_user           - Create a new user interactively")
    print("  list_users            - List all users")
    print("  select_user <user_id> - Select a user for chat")
    print("  list_docs             - List loaded PDFs")
    print("  remove_doc <name>     - Remove a specific PDF")
    print("  clear                 - Clear all loaded documents")
    print("  help                  - Show this help message")
    print("  exit                  - Exit the program")
    print("\nOr just type a question to ask about the loaded PDFs.\n")


def main():
    """Main CLI demo."""
    # Do not hard-code a decommissioned model name; allow env/config to choose the Groq model.
    rag = SimpleRAG(model=None, users_file="users.json")
    current_user_id = None

    print_help()

    while True:
        # Build prompt with current user info
        if current_user_id:
            prompt_str = f"\n[user ({current_user_id})]> "
        else:
            prompt_str = "\n> "

        user_input = input(prompt_str).strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "help":
            print_help()
            continue

        if user_input.lower().startswith("load "):
            pdf_path = user_input[5:].strip()
            if os.path.exists(pdf_path):
                print("⏳ Loading PDF...")
                text_length = len(rag.load_pdf(pdf_path))
                print(f"✓ PDF loaded ({text_length} characters)")
            else:
                print(f"❌ File not found: {pdf_path}")
            continue

        if user_input.lower() == "list_docs":
            docs = rag.list_documents()
            if docs:
                print("\n📚 Loaded Documents:")
                for i, doc in enumerate(docs, 1):
                    print(f"  {i}. {doc['name']} ({doc['pages']} pages, {doc['char_count']} chars)")
            else:
                print("ℹ️ No documents loaded. Use 'load <path>' to add PDFs.")
            continue

        if user_input.lower().startswith("remove_doc "):
            doc_name = user_input[11:].strip()
            if rag.remove_document(doc_name):
                print(f"✓ Removed: {doc_name}")
            continue

        if user_input.lower() == "clear":
            rag.clear_documents()
            print("✓ All documents cleared")
            continue

        if user_input.lower() == "list_users":
            users = rag.list_users()
            if users:
                print("\n👤 Available Users:")
                for user in users:
                    print(f"  • {user['name']} ({user['user_id']})")
                    if user["preferences"]:
                        print(f"    Preferences: {', '.join(user['preferences'])}")
            else:
                print("ℹ️ No users found. Run 'create_user' to add users.")
            continue

        if user_input.lower() == "create_user":
            user_id = input("  User ID: ").strip()
            if not user_id:
                print("❌ User ID is required")
                continue

            user_name = input("  User Name: ").strip()
            if not user_name:
                print("❌ User Name is required")
                continue

            prefs_input = input("  Preferences (comma-separated): ").strip()
            prefs = [p.strip() for p in prefs_input.split(",") if p.strip()]

            history_input = input("  Purchase/Interaction History (comma-separated): ").strip()
            history = [h.strip() for h in history_input.split(",") if h.strip()]

            rag.create_user(user_id, user_name, prefs, history)
            print(f"✓ User '{user_id}' created and saved to users.json")
            current_user_id = user_id
            print(f"✓ Switched to user '{user_id}'")
            continue

        if user_input.lower().startswith("select_user "):
            user_id = user_input[12:].strip()
            user = rag.get_user(user_id)
            if user:
                current_user_id = user_id
                print(f"✓ Switched to user: {user['name']} ({user['user_id']})")
            else:
                print(f"❌ User not found: {user_id}")
            continue

        # Otherwise treat as a question
        if not current_user_id:
            print("⚠️ No user selected. Use 'select_user <user_id>' or 'create_user' first.")
            continue

        print("\n⏳ Generating personalized response...\n")
        response = rag.generate_response(user_input, user_id=current_user_id)
        print(f"Response:\n{response}\n")


if __name__ == "__main__":
    main()
