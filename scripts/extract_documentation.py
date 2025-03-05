import os
import re
import sys
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener credenciales desde variables de entorno
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")

if not all([API_URL, API_TOKEN, ENVIRONMENT_ID]):
    print("❌ ERROR: Falta una o más variables de entorno (API_URL, API_TOKEN, ENVIRONMENT_ID).")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

TABLE_PATTERN = re.compile(r"ref\(\s*'([\w\.]+)'\s*\)", re.IGNORECASE)

QUERY = """
query ($environmentId: BigInt!, $modelUniqueId: String!) {
  environment(id: $environmentId) {
    applied {
      models(first: 1, filter: { uniqueIds: [$modelUniqueId] }) {
        edges {
          node {
            name
            description
            catalog {
              columns {
                name
                description
              }
            }
          }
        }
      }
    }
  }
}
"""

def extract_tables_from_sql(file_path):
    """Extract names from SQL file, including dbt ref ()"""
    tables = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            matches = TABLE_PATTERN.findall(line)
            tables.update(matches)
    return tables

def fetch_latest_model_documentation(model_name):
    """
    Retrieve the latest deployed model documentation from dbt Cloud's Discovery API.
    
    :param model_name: Name of the model without prefix (e.g., 'dim_members')
    :return: Formatted documentation string
    """    
    model_unique_id = f"model.dbt_atlas_project.{model_name}"

    variables = {
        "environmentId": int(ENVIRONMENT_ID),
        "modelUniqueId": model_unique_id
    }

    try:
        response = requests.post(API_URL, json={"query": QUERY, "variables": variables}, headers=HEADERS)
        
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        data = response.json()
        # Extract model data

        model_data = data.get("data", {}).get("environment", {}).get("applied", {}).get("models", {}).get("edges", [])

        if not model_data:
            return f"⚠️ No se encontró documentación para el modelo: {model_unique_id}"

        model = model_data[0]["node"]
        model_name = model.get("name", "Unknown Model")
        model_description = model.get("description", "No description available.")

        columns = model.get("catalog", {}).get("columns", [])
        formatted_columns = "\n".join([f"- {col['name']}: {col.get('description', 'No description available.')}" for col in columns])

        formatted_doc = f"**Model:** {model_name}\n\n**Description:** {model_description}\n\n**Columns:**\n{formatted_columns}"
        return formatted_doc
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"

def main():
    modified_files = sys.argv[1:]
    all_tables = set()

    for file_path in modified_files:
        if file_path.endswith(".sql") and os.path.exists(file_path):
            tables = extract_tables_from_sql(file_path)
            all_tables.update(tables)

    output_file = "scripts/detected_tables.txt"
    os.makedirs("scripts", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for table in sorted(all_tables):
            documentation = fetch_latest_model_documentation(table)
            f.write(f"{table}\n{documentation}\n\n")
    
    print(f"Saving tables in: {output_file}")  

if __name__ == "__main__":
    main()
