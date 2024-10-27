import flet as ft
import database  # Importar las funciones del archivo de base de datos
from datetime import datetime

# Crear las tablas al iniciar la aplicación
database.create_tables()

editing_appointment_id = None  # Variable global
editing_service_id = None  # Variable global para editar servicios

def main(page: ft.Page):
    page.title = "Gestión de Citas - Manicura y Pedicura"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    # Contenedor principal para la vista
    main_content = ft.Column()
    page.add(main_content)  # Agregar el contenedor principal a la página

    # Función para cargar la vista principal
    def load_main_view():
        main_content.controls.clear()
        main_content.controls.append(
            ft.Column([
                ft.Text("Bienvenido al sistema de gestión de citas", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                ft.Text("Seleccione una opción para continuar:", text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Citas",
                        on_click=lambda e: load_appointments_view(),
                        width=150,
                        height=60,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor=ft.colors.BLUE
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Clientes",
                        on_click=lambda e: load_customers_view(),
                        width=150,
                        height=60,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor=ft.colors.GREEN
                        ),
                    ),
                    ft.ElevatedButton(
                        text="Servicios",
                        on_click=lambda e: load_services_view(),
                        width=150,
                        height=60,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor=ft.colors.ORANGE
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ])
        )
        page.update()

    load_main_view()  # Cargar la vista principal al inicio

    # Vista de Citas
    def load_appointments_view():
        global editing_appointment_id
        editing_appointment_id = None  # Reiniciar ID de edición

        # Campos de entrada para citas
        name_input = ft.TextField(label="Nombre del Cliente", width=300)
        phone_input = ft.TextField(label="Teléfono", width=300)
        date_input = ft.TextField(label="Fecha (DD/MM/AAAA)", width=300, value=datetime.now().strftime('%d/%m/%Y'))
        time_input = ft.TextField(label="Hora (HH:MM)", width=300)
        service_input = ft.Dropdown(
            label="Servicio",
            options=[ft.dropdown.Option("Manicura"), ft.dropdown.Option("Pedicura"), ft.dropdown.Option("Manicura + Pedicura")],
            width=300
        )

        # Tabla de citas
        appointment_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Hora")),
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )

        # Cargar citas desde la base de datos
        def load_appointments():
            appointment_table.rows.clear()
            appointments = database.get_all_appointments()
            for row in appointments:
                appointment_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row[1])),  # Nombre
                        ft.DataCell(ft.Text(row[2])),  # Teléfono
                        ft.DataCell(ft.Text(row[3])),  # Fecha
                        ft.DataCell(ft.Text(row[4])),  # Hora
                        ft.DataCell(ft.Text(row[5])),  # Servicio
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, row=row: edit_appointment(row)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, row=row: delete_appointment(row[0]))
                            ])
                        )
                    ])
                )
            page.update()

        def edit_appointment(row):
            global editing_appointment_id  # Referencia a la variable global

            # Cargar los valores actuales en los campos de entrada para edición
            name_input.value = row[1]  # Nombre
            phone_input.value = row[2]  # Teléfono
            date_input.value = row[3]  # Fecha
            time_input.value = row[4]  # Hora
            service_input.value = row[5]  # Servicio

            # Guardar el ID de la cita que se está editando
            editing_appointment_id = row[0]
            page.update()

        # Función para agregar o actualizar una cita
        def add_or_update_appointment(e):
            global editing_appointment_id  # Referencia a la variable global

            name = name_input.value
            phone = phone_input.value
            date = date_input.value
            time = time_input.value
            service = service_input.value

            if name and phone and date and time and service:
                customer = database.find_customer(name, phone)
                if customer is None:
                    customer_id = database.insert_customer(name, phone)
                else:
                    customer_id = customer[0]

                if editing_appointment_id:
                    # Actualizar cita existente
                    database.update_appointment(editing_appointment_id, customer_id, date, time, service)
                    editing_appointment_id = None  # Resetear después de editar
                else:
                    # Agregar una nueva cita
                    database.insert_appointment(customer_id, date, time, service)

                load_appointments()

                # Limpiar campos de entrada
                name_input.value = ""
                phone_input.value = ""
                time_input.value = ""
                service_input.value = None
                page.update()
            else:
                # Mostrar advertencia si faltan campos
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Por favor, llena todos los campos antes de agendar."),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())]
                )
                page.dialog.open = True
                page.update()

        # Función para eliminar una cita
        def delete_appointment(appointment_id):
            database.delete_appointment(appointment_id)
            load_appointments()

        # Cargar las citas existentes al iniciar
        load_appointments()

        # Botón para agendar cita
        schedule_button = ft.ElevatedButton(text="Agendar Cita", on_click=add_or_update_appointment)

        # Agregar controles a la vista de citas
        main_content.controls.clear()
        main_content.controls.append(
            ft.Column([
                ft.Text("Agenda de Citas - Manicura y Pedicura", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                name_input,
                phone_input,
                date_input,
                time_input,
                service_input,
                schedule_button,
                appointment_table,
                ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view())  # Botón para volver
            ])
        )
        page.update()

    # Vista de Clientes
    def load_customers_view():
        customers_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Historial de Servicios"))
            ],
            rows=[]
        )

        # Cargar clientes desde la base de datos
        def load_customers():
            customers_table.rows.clear()
            customers = database.get_all_customers()
            for row in customers:
                service_history = database.get_service_history(row[0])  # Obtener historial de servicios
                customers_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row[1])),  # Nombre
                        ft.DataCell(ft.Text(row[2])),  # Teléfono
                        ft.DataCell(ft.Text(service_history))  # Historial de servicios
                    ])
                )
            page.update()

        # Cargar los clientes existentes al iniciar
        load_customers()

        # Agregar controles a la vista de clientes
        main_content.controls.clear()
        main_content.controls.append(
            ft.Column([
                ft.Text("Clientes", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                customers_table,
                ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view())  # Botón para volver
            ])
        )
        page.update()

    # Vista de Servicios
    def load_services_view():
        global editing_service_id
        editing_service_id = None  # Reiniciar ID de edición

        service_input = ft.TextField(label="Servicio", width=300)
        price_input = ft.TextField(label="Precio", width=300)

        services_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )

        # Cargar servicios desde la base de datos
        def load_services():
            services_table.rows.clear()
            services = database.get_all_services()
            for row in services:
                services_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row[1])),  # Servicio
                        ft.DataCell(ft.Text(row[2])),  # Precio
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, row=row: edit_service(row)),
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, row=row: delete_service(row[0]))
                            ])
                        )
                    ])
                )
            page.update()

        def edit_service(row):
            global editing_service_id  # Referencia a la variable global

            # Cargar los valores actuales en los campos de entrada para edición
            service_input.value = row[1]  # Servicio
            price_input.value = row[2]  # Precio

            # Guardar el ID del servicio que se está editando
            editing_service_id = row[0]
            page.update()

        # Función para agregar o actualizar un servicio
        def add_or_update_service(e):
            global editing_service_id  # Referencia a la variable global

            service = service_input.value
            price = price_input.value

            if service and price:
                if editing_service_id:
                    # Actualizar servicio existente
                    database.update_service(editing_service_id, service, price)
                    editing_service_id = None  # Resetear después de editar
                else:
                    # Agregar un nuevo servicio
                    database.insert_service(service, price)

                load_services()

                # Limpiar campos de entrada
                service_input.value = ""
                price_input.value = ""
                page.update()
            else:
                # Mostrar advertencia si faltan campos
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Por favor, llena todos los campos antes de agregar."),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())]
                )
                page.dialog.open = True
                page.update()

        # Función para eliminar un servicio
        def delete_service(service_id):
            database.delete_service(service_id)
            load_services()

        # Cargar los servicios existentes al iniciar
        load_services()

        # Botón para agregar servicio
        add_service_button = ft.ElevatedButton(text="Agregar Servicio", on_click=add_or_update_service)

        # Agregar controles a la vista de servicios
        main_content.controls.clear()
        main_content.controls.append(
            ft.Column([
                ft.Text("Servicios", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                service_input,
                price_input,
                add_service_button,
                services_table,
                ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view())  # Botón para volver
            ])
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
