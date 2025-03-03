from datetime import datetime

def format_due_date(due_date_str):
    for fmt in ['%d/%m/%Y', '%d-%m-%Y']:
        try:
            due_date = datetime.strptime(due_date_str, fmt)
            return due_date
        except ValueError:
            continue

    raise ValueError(f"Formato de data inválido: {due_date_str}. Esperado formato 'dd/mm/yyyy' ou 'dd-mm-yyyy'.")