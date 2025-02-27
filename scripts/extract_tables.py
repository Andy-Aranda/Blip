import os
import re
import sys

TABLE_PATTERN = re.compile(r"FROM\s+([\w\.]+)|JOIN\s+([\w\.]+)", re.IGNORECASE)

def extract_tables_from_sql(file_path):
    """Extrae nombres de tablas del file sql"""
    tables = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            matches = TABLE_PATTERN.findall(line) 
            for match in matches:
                table_name = match[0] or match[1] 
                if table_name:
                    tables.add(table_name)
    return tables

def main():

    modified_files = sys.argv[1:]  

    all_tables = set()

    for file_path in modified_files:
        if file_path.endswith(".sql") and os.path.exists(file_path):
            tables = extract_tables_from_sql(file_path)
            all_tables.update(tables)

    output_file = "scripts/detected_tables.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        if all_tables:
            f.write("\n".join(sorted(all_tables)))
            print(f"Tablas guardadas en {output_file}")
        else:
            #f.write("No se encontraron tablas en los archivos SQL.\n")
            print("No se encontraron tablas en los archivos.")

if __name__ == "__main__":
    main()
