import requests

URL = "https://thaqalayn-api.net/graphql"
QUERY = """
{
    ingredients {
        ingredient
        otherNames
        info
        statuses
    }
}
"""


def get_ingredients():
    response = requests.post(URL, json={"query": QUERY})
    if response.status_code == 200:
        return response.json().get("data", {}).get("ingredients", [])
    else:
        return {"error": "Failed to fetch ingredients"}


def save_to_markdown(ingredients, filename="../static/notes/ingredients.md"):
    with open(filename, "w") as f:
        f.write("# Ingredients\n\n")
        for ingredient in ingredients:
            f.write(f"### {ingredient['ingredient']}\n\n")
            if ingredient['otherNames']:
                f.write(f"**Other Names:** {', '.join(ingredient['otherNames'])}\n\n")
            if ingredient['info']:
                f.write(f"**Info:** {', '.join(ingredient['info'])}\n\n")
            if ingredient['statuses']:
                f.write("**Statuses:**\n")
                for status in ingredient['statuses']:
                    f.write(f"\n- {status}")
                f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    ingredients = get_ingredients()
    save_to_markdown(ingredients)
