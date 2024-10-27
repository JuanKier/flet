import flet as ft
import database  # Importar las funciones del archivo de base de datos
from datetime import datetime
import locale

# Establecer la localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 

# Crear las tablas al iniciar la aplicación
database.create_tables()

editing_appointment_id = None  # Variable global

dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def load_appointments_view(main_content, page, load_main_view):
    global editing_appointment_id
    editing_appointment_id = None  # Reiniciar ID de edición

    def get_services_options():
        services = [ft.dropdown.Option(service[1]) for service in database.get_all_services()]
        return services

    # Campos de entrada para citas
    name_input = ft.TextField(
        label="Nombre del Cliente",
        width=300,
        on_change=lambda e: update_customer_info(e.control.value)
    )

    # Autocompletar teléfono basado en el nombre ingresado
    def update_customer_info(name):
        customer = database.find_customer_by_name(name)
        if customer:
            phone_input.value = customer[2]  # Establecer el teléfono del cliente encontrado
            phone_input.read_only = True  # Hacer el campo de teléfono de solo lectura
        else:
            phone_input.value = ""  # Limpiar el teléfono si no se encuentra
            phone_input.read_only = False  # Hacer el campo editable si no se encuentra
        page.update()

    phone_input = ft.TextField(label="Teléfono", width=300, read_only=True)
    date_input = ft.TextField(label="Fecha (DD/MM/AAAA)", width=300, value=datetime.now().strftime('%d/%m/%Y'), on_change=lambda e: update_day_of_week(e.control.value))
    day_of_week_text = ft.Text("")  # Para mostrar el día de la semana

    def update_day_of_week(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            dia_de_la_semana = dias_de_la_semana[date_obj.weekday()]  # Obtener el día de la semana en español
            day_of_week_text.value = f"Día: {dia_de_la_semana.capitalize()}"  # Usar capitalize() para asegurar que tenga la primera letra en mayúscula
        except ValueError:
            day_of_week_text.value = "Fecha inválida"  # Manejar error de formato
        page.update()  # Asegurarse de actualizar la página

    time_input = ft.Dropdown(
        label="Hora",
        width=300,
        options=[
            ft.dropdown.Option("07:00"),
            ft.dropdown.Option("08:00"),
            ft.dropdown.Option("09:00"),
            ft.dropdown.Option("10:00"),
            ft.dropdown.Option("11:00"),
            ft.dropdown.Option("12:00"),
            ft.dropdown.Option("13:00"),
            ft.dropdown.Option("14:00"),
            ft.dropdown.Option("15:00"),
            ft.dropdown.Option("16:00"),
            ft.dropdown.Option("17:00"),
            ft.dropdown.Option("18:00"),
            ft.dropdown.Option("19:00"),
        ],
    )

    def format_time_input(control):
        value = control.value.replace(":", "")
        if value.isdigit():
            if len(value) > 4:
                value = value[:4]
            if len(value) >= 2:
                formatted_value = f"{value[:2]}:{value[2:]}"
            else:
                formatted_value = value

            control.value = formatted_value
            page.update()

    service_input = ft.Dropdown(
        label="Servicio",
        options=get_services_options(),
        width=300
    )

    status_input = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("Finalizado")
        ],
        width=300
    )

    appointment_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre", size=12)),  # Tamaño de texto reducido
            #ft.DataColumn(ft.Text("Teléfono", size=12)),
            ft.DataColumn(ft.Text("Fecha", size=12)),
            ft.DataColumn(ft.Text("Día", size=12)),
            ft.DataColumn(ft.Text("Hora", size=12)),
            #ft.DataColumn(ft.Text("Servicio", size=12)),
            #ft.DataColumn(ft.Text("Monto", size=12)),
            #ft.DataColumn(ft.Text("Estado", size=12)),
            #ft.DataColumn(ft.Text("Acciones", size=12))
        ],
        rows=[],
        data_text_style=ft.TextStyle(size=12),
    )

    def load_appointments():
        appointment_table.rows.clear()
        appointments = database.get_all_appointments()
        appointments_sorted = sorted(
            appointments,
            key=lambda row: (datetime.strptime(row[3], '%d/%m/%Y'), row[4])
        )
        for row in appointments_sorted:
            service_price = database.get_service_price(row[5])
            service_price_str = f"{service_price:,.0f} PYG" if service_price else "N/A"
            date_obj = datetime.strptime(row[3], '%d/%m/%Y')  # Convertir la fecha a objeto datetime
            dia_de_la_semana = dias_de_la_semana[date_obj.weekday()]  # Obtener el nombre del día de la semana en español
            appointment_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(ft.Text(row[1], size=12), width=40)),
                    #ft.DataCell(ft.Text(row[2])),
                    ft.DataCell(ft.Container(ft.Text(row[3], size=8), width=40)),
                    ft.DataCell(ft.Container(ft.Text(dia_de_la_semana, size=8), width=40)),  # Añadir el día de la semana
                    ft.DataCell(ft.Container(ft.Text(row[4], size=12), width=40)),
                    #ft.DataCell(ft.Text(row[5])),
                    #ft.DataCell(ft.Text(service_price_str)),
                    #ft.DataCell(ft.Text(row[6])),
                    #ft.DataCell(
                        #ft.Row([
                           # ft.IconButton(ft.icons.EDIT, on_click=lambda e, row=row: edit_appointment(row)),
                            #ft.IconButton(ft.icons.DELETE, on_click=lambda e, row=row: delete_appointment(row[0]))
                       # ])
                    #)
                ])
            )
        page.update()

    def edit_appointment(row):
        global editing_appointment_id
        name_input.value = row[1]
        phone_input.value = row[2]
        phone_input.read_only = True
        date_input.value = row[3]
        update_day_of_week(row[3])  # Actualizar el día de la semana
        time_input.value = row[4]
        service_input.value = row[5]
        status_input.value = row[6]
        editing_appointment_id = row[0]
        page.update()

    def add_or_update_appointment(e):
        global editing_appointment_id
        name = name_input.value.strip()
        phone = phone_input.value.strip()
        date = date_input.value.strip()
        time = time_input.value
        service = service_input.value
        status = status_input.value

        # Comprobar si hay campos vacíos
        if not name or not phone or not date or not time or not service or not status:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Por favor, llena todos los campos antes de agendar."),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: close_dialog(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        # Verificar si el cliente ya existe
        customer = database.find_customer_by_name(name)
        if customer is None:
            # Si el cliente no existe, agregarlo a la base de datos
            customer_id = database.insert_or_update_customer(name, phone)
        else:
            customer_id = customer[0]

        service_id = next((s[0] for s in database.get_all_services() if s[1] == service), None)

        try:
            if editing_appointment_id:
                database.update_appointment(editing_appointment_id, customer_id, date, time, service_id, status)
                editing_appointment_id = None
            else:
                database.insert_appointment(customer_id, date, time, service_id, status)

            # Insertar en el historial de servicios
            database.insert_service_history(customer_id, service_id, date, time)

            load_appointments()

            # Reiniciar campos después de agregar/actualizar
            name_input.value = ""
            phone_input.value = ""
            date_input.value = datetime.now().strftime('%d/%m/%Y')
            day_of_week_text.value = ""  # Limpiar el texto del día
            time_input.value = ""
            service_input.value = None
            status_input.value = "Pendiente"
            page.update()

        except Exception as ex:
            print(f"Error al insertar/actualizar la cita: {ex}")

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def delete_appointment(appointment_id):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta cita?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog(confirm_dialog)),
                ft.TextButton("Eliminar", on_click=lambda e: confirm_delete(appointment_id))
            ]
        )
        page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        page.update()

    def confirm_delete(appointment_id):
        database.delete_appointment(appointment_id)
        load_appointments()
        close_dialog(page.overlay[-1])

    schedule_button = ft.ElevatedButton(text="Agendar Cita", on_click=add_or_update_appointment)
    clear_button = ft.ElevatedButton(text="Limpiar Citas", on_click=lambda e: clear_appointments())

    main_content.controls.clear()
    main_content.controls.append(
        ft.Column([
            ft.Text("Agenda de Citas - Manicura y Pedicura", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
            name_input,
            phone_input,
            date_input,
            time_input,
            service_input,
            status_input,
            day_of_week_text,  # Añadir el texto del día de la semana
            schedule_button,
            clear_button,
            appointment_table,
            ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view(main_content, page))
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)  # Alineación centrada
    )


    load_appointments()  # Cargar citas al iniciar la vista
    page.update()

    def clear_appointments():
        today = datetime.now().strftime('%d/%m/%Y')
        database.clear_appointments(today)  # Asumiendo que tienes una función para limpiar citas
        load_appointments()  # Recargar citas después de limpiar



            # Crear dos filas para los inputs
            # ft.Row([
              #   ft.Column([
          #           name_input,
            #         phone_input,
              #       date_input,
                # ], alignment=ft.MainAxisAlignment.START),  # Alinear a la izquierda
                
                # ft.Column([
                  #   time_input,
                    # service_input,
                    # status_input,
                # ], alignment=ft.MainAxisAlignment.END),  # Alinear a la derecha
            # ], alignment=ft.MainAxisAlignment.CENTER),  # Centrar la fila principal
            