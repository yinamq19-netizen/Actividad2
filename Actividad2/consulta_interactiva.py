import sqlite3

DB_FILE = 'facturas.db'

print('Consulta interactiva de la base de datos facturas.db')
print('Escribe una consulta SQL (ejemplo: SELECT * FROM facturas;) o escribe "salir" para terminar.')

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

while True:
    query = input('SQL> ')
    if query.strip().lower() == 'salir':
        break
    try:
        c.execute(query)
        if query.strip().lower().startswith('select'):
            rows = c.fetchall()
            for row in rows:
                print(row)
        else:
            conn.commit()
            print('Comando ejecutado correctamente.')
    except Exception as e:
        print(f'Error: {e}')

conn.close()
print('Sesión finalizada.')
