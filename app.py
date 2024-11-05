from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Cambiar el backend de matplotlib a Agg
plt.switch_backend('Agg')

app = Flask(__name__)

@app.route('/')
def home():
    # Crear un dataframe de ejemplo
    data = {
        'Nombre': ['Ana', 'Luis', 'Carlos', 'María', 'Jorge', 'Lucía', 'Pedro', 'Marta', 'Sofía', 'Juan'],
        'Edad': [23, 34, 45, 29, 38, 22, 41, 30, 27, 35],
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Bilbao', 'Granada', 'Málaga', 'Murcia', 'Alicante'],
        'Profesión': ['Ingeniera', 'Doctor', 'Abogado', 'Arquitecta', 'Profesor', 'Enfermera', 'Periodista', 'Diseñadora', 'Científica', 'Músico'],
        'Salario': [30000, 45000, 50000, 32000, 40000, 28000, 35000, 37000, 42000, 39000]
    }
    df = pd.DataFrame(data)

    # Convertir el dataframe a HTML
    df_html = df.to_html()

    # Crear un gráfico de barras de salario por ciudad
    plt.figure(figsize=(10, 6))
    df.groupby('Ciudad')['Salario'].mean().plot(kind='bar')
    plt.title('Salario por Ciudad')
    plt.xlabel('Ciudad')
    plt.ylabel('Salario Promedio')

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url_city = base64.b64encode(img.getvalue()).decode()

    # Crear una nueva columna para las franjas de edad
    bins = [20, 25, 30, 35, 40]
    labels = ['20-25', '25-30', '30-35', '35-40']
    df['Franja_Edad'] = pd.cut(df['Edad'], bins=bins, labels=labels, right=False)

    # Crear un gráfico de barras de salario por franja de edad
    plt.figure(figsize=(10, 6))
    df.groupby('Franja_Edad')['Salario'].mean().plot(kind='bar')
    plt.title('Salario por Franja de Edad')
    plt.xlabel('Franja de Edad')
    plt.ylabel('Salario Promedio')

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url_age = base64.b64encode(img.getvalue()).decode()

    # Crear un gráfico de dispersión de edad vs salario
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Edad'], df['Salario'])
    plt.title('Relación entre Edad y Salario')
    plt.xlabel('Edad')
    plt.ylabel('Salario')

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url_scatter = base64.b64encode(img.getvalue()).decode()

    # Plantilla HTML para renderizar el dataframe y los gráficos
    html = f'''
    <html>
    <head>
        <title>DataFrame y Gráficos</title>
    </head>
    <body>
        <h1>DataFrame</h1>
        {df_html}
        <h1>Gráfico de Salario por Ciudad</h1>
        <img src="data:image/png;base64,{plot_url_city}" />
        <h1>Gráfico de Salario por Franja de Edad</h1>
        <img src="data:image/png;base64,{plot_url_age}" />
        <h1>Gráfico de Dispersión de Edad vs Salario</h1>
        <img src="data:image/png;base64,{plot_url_scatter}" />
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)