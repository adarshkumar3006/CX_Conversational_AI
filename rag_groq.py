"""
Simple RAG module with user context and personalization.
Demo purpose: upload PDF, store user profiles, generate personalized responses using Groq.
"""

import os
import json
from typing import List, Optional, Dict
import PyPDF2

# Try importing Groq client, but don't fail import if package or credentials are missing
try:
    from groq import Groq, GroqError
except Exception:
    Groq = None
    GroqError = Exception


class UserContextDB:
    """Simple in-memory vector DB for user profiles and preferences with JSON persistence."""

    def __init__(self, users_file: str = "users.json"):
        """Initialize the user context database."""
        self.users: Dict[str, dict] = {}  # user_id -> user_profile dict
        self.users_file = users_file
        
        # Auto-load users from file if it exists
        self.load_from_file()

    def create_or_update_user(
        self,
        user_id: str,
        name: str = None,
        preferences: List[str] = None,
        purchase_history: List[str] = None,
    ) -> dict:
        """
        Create or update a user profile and save to file.

        Args:
            user_id: Unique user identifier
            name: User's full name
            preferences: List of user preferences (e.g., ["vegetarian", "likes_coffee"])
            purchase_history: List of past purchases or interactions

        Returns:
            Updated user profile
        """
        if user_id not in self.users:
            self.users[user_id] = {
                "user_id": user_id,
                "name": name or f"User_{user_id}",
                "preferences": preferences or [],
                "purchase_history": purchase_history or [],
            }
        else:
            if name:
                self.users[user_id]["name"] = name
            if preferences:
                self.users[user_id]["preferences"] = preferences
            if purchase_history:
                self.users[user_id]["purchase_history"] = purchase_history

        # Auto-save to file after any change
        self.save_to_file()
        return self.users[user_id]

    def get_user(self, user_id: str) -> Optional[dict]:
        """
        Retrieve a user profile.

        Args:
            user_id: User identifier

        Returns:
            User profile dict or None if not found
        """
        return self.users.get(user_id)

    def list_users(self) -> List[dict]:
        """Return all stored user profiles."""
        return list(self.users.values())

    def delete_user(self, user_id: str) -> bool:
        """Delete a user profile and save to file."""
        if user_id in self.users:
            del self.users[user_id]
            self.save_to_file()
            return True
        return False

    def save_to_file(self) -> None:
        """Persist users to JSON file."""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save users to {self.users_file}: {e}")

    def load_from_file(self) -> None:
        """Load users from JSON file if it exists."""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
                    print(f"✓ Loaded {len(self.users)} user(s) from {self.users_file}")
            except Exception as e:
                print(f"Warning: Could not load users from {self.users_file}: {e}")

    def clear_all(self) -> None:
        """Clear all users and save to file."""
        self.users = {}
        self.save_to_file()


class SimpleRAG:
    """Simple RAG system: load multiple PDFs, store user context, generate personalized responses via Groq."""

    def __init__(self, model: str = None, users_file: str = "users.json"):
        """Initialize RAG with Groq model and user context DB with persistence.

        The Groq model will be taken from the `model` argument if provided,
        otherwise from the `GROQ_MODEL` environment variable, and finally
        falls back to a sensible default `groq-mixtral-v1`.
        """
        # Prefer explicit argument -> env var -> sensible default
        self.model = model or os.getenv("GROQ_MODEL") or "groq-mixtral-v1"
        self.documents: List[Dict[str, str]] = []  # Store PDFs with metadata: {name, text, pages, char_count}
        self.conversation_history: List[dict] = []  # For multi-turn conversations
        self.client = None
        self.user_db = UserContextDB(users_file=users_file)  # Initialize with persistence

        api_key = os.getenv("GROQ_API_KEY")
        if Groq is None:
            print("Warning: 'groq' package not installed. Install it to enable Groq generation.")
        elif not api_key:
            print("Warning: GROQ_API_KEY environment variable not set. Set it to enable generation.")
        else:
            try:
                self.client = Groq(api_key=api_key)
            except Exception as e:
                print(f"Error initializing Groq client: {e}")
                self.client = None

    def load_pdf(self, pdf_path: str) -> str:
        """
        Load and extract text from a PDF file (can load multiple).

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text from PDF
        """
        try:
            text = ""
            pdf_name = os.path.basename(pdf_path)
            page_count = 0
            
            with open(pdf_path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page_count = len(pdf_reader.pages)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text() or ""
                    text += f"\n--- {pdf_name} Page {page_num} ---\n{page_text}"

            # Add to documents list (supports multiple PDFs)
            doc_entry = {
                "name": pdf_name,
                "text": text,
                "pages": page_count,
                "char_count": len(text)
            }
            self.documents.append(doc_entry)
            print(f"✓ PDF loaded: {pdf_name} ({page_count} pages, {len(text)} characters)")
            return text
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return ""

    def generate_response(self, query: str, user_id: str = None) -> str:
        """
        Generate a personalized response based on query, multiple PDF contents, and user context using Groq.

        Args:
            query: User query
            user_id: Optional user ID for personalization

        Returns:
            Generated response from Groq or a guidance message if client not configured
        """
        if not self.documents:
            return "No PDF loaded. Please upload a PDF first."

        # Prepare combined document context from all loaded PDFs
        context = "\n\n".join([doc["text"] for doc in self.documents])

        # Retrieve user context if user_id is provided
        user_context_str = ""
        if user_id:
            user_profile = self.user_db.get_user(user_id)
            if user_profile:
                user_context_str = self._format_user_context(user_profile)
            else:
                user_context_str = f"User ID: {user_id} (no profile data available)"

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": query})

        # Build system prompt with user context awareness
        system_prompt = (
            "You are a helpful, personalized assistant. "
            "Answer questions based on the provided document context and user context. "
            "Tailor your response to the user's preferences and history when relevant. "
            "If the answer is not in the document, say 'The information is not available in the provided document.'"
        )

        # Build user message with document + user context
        user_message = f"Document context:\n{context}"
        if user_context_str:
            user_message += f"\n\nUser Context:\n{user_context_str}"
        user_message += f"\n\nQuestion: {query}"

        # Build messages for Groq API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        if not self.client:
            return (
                "Groq client not configured.\n"
                "Set the GROQ_API_KEY environment variable (or add it to your .env) and restart the app.\n"
                "Example (PowerShell): $env:GROQ_API_KEY = 'your_key_here'"
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            # The response shape may vary by SDK version; guard access
            try:
                answer = response.choices[0].message.content
            except Exception:
                answer = getattr(response, "text", None) or str(response)

            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _format_user_context(self, user_profile: dict) -> str:
        """
        Format user context for inclusion in the LLM prompt.

        Args:
            user_profile: User profile dictionary

        Returns:
            Formatted user context string
        """
        lines = [f"Name: {user_profile.get('name', 'Unknown')}"]

        if user_profile.get("preferences"):
            lines.append(f"Preferences: {', '.join(user_profile['preferences'])}")

        if user_profile.get("purchase_history"):
            lines.append(f"Recent interactions: {', '.join(user_profile['purchase_history'][-3:])}")

        return "\n".join(lines)

    def create_user(
        self,
        user_id: str,
        name: str = None,
        preferences: List[str] = None,
        purchase_history: List[str] = None,
    ) -> dict:
        """Create or update a user profile in the context DB."""
        return self.user_db.create_or_update_user(user_id, name, preferences, purchase_history)

    def get_user(self, user_id: str) -> Optional[dict]:
        """Retrieve a user profile."""
        return self.user_db.get_user(user_id)

    def list_users(self) -> List[dict]:
        """List all stored user profiles."""
        return self.user_db.list_users()

    def list_documents(self) -> List[Dict]:
        """List all loaded documents with metadata."""
        return self.documents

    def remove_document(self, pdf_name: str) -> bool:
        """Remove a specific document by name."""
        for i, doc in enumerate(self.documents):
            if doc["name"] == pdf_name:
                self.documents.pop(i)
                print(f"✓ Removed: {pdf_name}")
                return True
        print(f"✗ Document not found: {pdf_name}")
        return False

    def clear_documents(self):
        """Clear all loaded documents."""
        self.documents = []
        self.conversation_history = []
        print("All documents cleared.")


if __name__ == "__main__":
    rag = SimpleRAG()
    print("SimpleRAG initialized with user context and multiple PDF support.")
    print("Use rag.load_pdf(path) to load PDFs (can load multiple).")
    print("Use rag.list_documents() to see all loaded PDFs.")
    print("Use rag.remove_document(name) to remove a specific PDF.")
    print("Use rag.create_user(user_id, name, preferences) to create a user profile.")
