import flet as ft
import database  # Importar las funciones del archivo de base de datos

editing_customer_id = None  # Variable global para la edición

def load_customers_view(main_content, page, load_main_view):
    global editing_customer_id
    editing_customer_id = None  # Reiniciar ID de edición

    name_input = ft.TextField(label="Nombre del Cliente", width=300)
    phone_input = ft.TextField(label="Teléfono", width=300)

    customers_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones"))
        ],
        rows=[]
    )

    def load_customers():
        customers_table.rows.clear()
        customers = database.get_all_customers()
        for row in customers:
            customers_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(
                        ft.TextButton(
                            row[1],  # Nombre del cliente
                            on_click=lambda e, customer_id=row[0]: show_customer_history(customer_id)  # Pasa el ID correcto
                        )
                    ),
                    ft.DataCell(ft.Text(row[2])),  # Teléfono
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(ft.icons.EDIT, on_click=lambda e, row=row: edit_customer(row)),
                            ft.IconButton(ft.icons.DELETE, on_click=lambda e, row=row: delete_customer(row[0]))
                        ])
                    )
                ])
            )
        page.update()

    def show_customer_history(customer_id):
        history = database.get_service_history(customer_id)

        # Crear un ListView para el historial de servicios
        history_items = [ft.Text(f"Servicio: {service[0]}, Fecha: {service[1]}, Hora: {service[2]}") for service in history]
        
        history_list_view = ft.ListView(
            controls=history_items,
            height=300,  # Aumentar la altura del ListView
            spacing=10  # Espaciado entre elementos
        )

        # Contenedor que permitirá establecer el tamaño del diálogo
        content_container = ft.Container(
            content=history_list_view,
            width=600,  # Establecer un ancho personalizado
            height=400,  # Establecer una altura personalizada
        )

        def clear_history():
            # Llamar a la función de la base de datos para limpiar el historial
            database.clear_service_history(customer_id)  # Asegúrate de implementar esta función en tu módulo de base de datos
            history_list_view.controls.clear()  # Limpiar los elementos del ListView
            page.update()  # Actualizar la página

        # Botón para limpiar historial
        clear_button = ft.TextButton(
            "Limpiar Historial",
            on_click=lambda e: clear_history()  # Llamar a la función para limpiar el historial
        )

        history_dialog = ft.AlertDialog(
        title=ft.Text("Historial de Servicios"),
        content=ft.Column(  # Usar un Column para añadir el ListView y el botón
            controls=[content_container, clear_button],
        ),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: close_dialog(history_dialog))]
    )

        page.overlay.append(history_dialog)  # Añade el diálogo al overlay
        history_dialog.open = True  # Abre el diálogo
        page.update()

    def close_dialog(dialog):
        dialog.open = False  # Cierra el diálogo
        page.update()

    def edit_customer(row):
        global editing_customer_id
        name_input.value = row[1]  # Nombre del cliente
        phone_input.value = row[2]  # Teléfono del cliente
        editing_customer_id = row[0]  # ID del cliente
        page.update()

    def add_or_update_customer(e):
        global editing_customer_id
        name = name_input.value
        phone = phone_input.value

        if name and phone:
            if editing_customer_id is not None:
                # Llamar a la función de base de datos para actualizar
                database.insert_or_update_customer(name, phone, editing_customer_id)
            else:
                # Llamar a la función de base de datos para agregar
                database.insert_or_update_customer(name, phone)

            load_customers()  # Recargar la tabla de clientes
            name_input.value = ""
            phone_input.value = ""
            editing_customer_id = None
            page.update()
        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Por favor, llena todos los campos antes de continuar."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(page.dialog))]
            )
            page.dialog.open = True
            page.update()

    def delete_customer(customer_id):
        database.delete_customer(customer_id)
        load_customers()

    load_customers()

    add_update_button = ft.ElevatedButton(text="Agregar/Actualizar Cliente", on_click=add_or_update_customer)

    main_content.controls.clear()
    main_content.controls.append(
        ft.Column([
            ft.Text("Gestión de Clientes", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
            name_input,
            phone_input,
            add_update_button,
            customers_table,
            ft.Container(height=20),
            ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view(main_content, page))
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)  # Alineación centrada
    )
    page.update()
