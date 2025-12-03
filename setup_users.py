"""
Setup script: Create 2 default users and save to users.json
Run this once to initialize the user database with sample data.
"""

from rag_groq import SimpleRAG


def setup_default_users():
    """Create 2 default users with realistic preferences and history."""
    rag = SimpleRAG()

    # Clear existing users (optional; comment out to keep existing data)
    # rag.user_db.clear_all()

    # User 1: Alice - Health-conscious, vegan
    alice = rag.create_user(
        user_id="alice_001",
        name="Alice Johnson",
        preferences=["vegan", "organic", "low-calorie", "fitness", "health-conscious"],
        purchase_history=[
            "bought_acai_bowl",
            "attended_yoga_class",
            "read_nutrition_blog",
            "purchased_smoothie",
            "joined_gym",
        ],
    )
    print("✓ Created user: Alice Johnson")
    print(f"  Preferences: {', '.join(alice['preferences'])}")
    print(f"  History: {', '.join(alice['purchase_history'][-3:])}\n")

    # User 2: Bob - Premium, meat-lover
    bob = rag.create_user(
        user_id="bob_001",
        name="Bob Smith",
        preferences=["premium_cuts", "fine_dining", "wine_pairing", "luxury", "beef_lover"],
        purchase_history=[
            "bought_ribeye_steak",
            "attended_wine_tasting",
            "purchased_champagne",
            "booked_fine_dining",
            "bought_truffle_oil",
        ],
    )
    print("✓ Created user: Bob Smith")
    print(f"  Preferences: {', '.join(bob['preferences'])}")
    print(f"  History: {', '.join(bob['purchase_history'][-3:])}\n")

    # List all users
    print("=" * 60)
    print("All Users:")
    print("=" * 60)
    for user in rag.list_users():
        print(f"\n👤 {user['name']} ({user['user_id']})")
        print(f"   Preferences: {', '.join(user['preferences'])}")
        print(f"   History: {', '.join(user['purchase_history'][:3])}")

    print("\n✓ Users saved to users.json")
    print("You can now run the Streamlit app or CLI demo and these users will be available!")


if __name__ == "__main__":
    setup_default_users()
