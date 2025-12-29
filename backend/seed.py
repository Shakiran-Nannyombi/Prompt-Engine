import json
from database import get_connection

def seed_frameworks():
    frameworks = [
        {
            "name": "C.O.R.E.",
            "description": "Context, Objective, Role, Example",
            "structure": {
                "C": "Context (Background)",
                "O": "Objective (Goal)",
                "R": "Role (Persona)",
                "E": "Example (Ideal output)"
            }
        },
        {
            "name": "R.A.C.E.",
            "description": "Role, Action, Context, Expectation",
            "structure": {
                "R": "Role",
                "A": "Action",
                "C": "Context",
                "E": "Expectation"
            }
        },
        {
            "name": "RISEN",
            "description": "Role, Instructions, Steps, End goal, Narrowing",
            "structure": {
                "R": "Role",
                "I": "Instructions",
                "S": "Steps",
                "E": "End goal",
                "N": "Narrowing (Constraints)"
            }
        }
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for f in frameworks:
                cur.execute(
                    """
                    INSERT INTO framework_templates (name, description, structure)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO NOTHING;
                    """,
                    (f["name"], f["description"], json.dumps(f["structure"]))
                )
        conn.commit()
        print("Frameworks seeded successfully.")
    except Exception as e:
        print(f"Error seeding frameworks: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_frameworks()
