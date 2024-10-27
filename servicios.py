import flet as ft
import database  # Importar las funciones del archivo de base de datos

editing_service_id = None  # Variable global para la edición

def load_services_view(main_content, page, load_main_view):
    global editing_service_id
    editing_service_id = None  # Reiniciar ID de edición

    service_input = ft.TextField(label="Servicio", width=300)
    price_input = ft.TextField(label="Precio (Gs)", width=300)  # Indicar que el precio es en guaraníes

    services_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Servicio")),
            ft.DataColumn(ft.Text("Precio (Gs)")),  # Modificar para mostrar en guaraníes
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
                    ft.DataCell(ft.Text(f"Gs {row[2]:,.0f}")),  # Mostrar precio formateado con guaraníes
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
        price_input.value = str(row[2])  # Precio como texto para el input

        # Guardar el ID del servicio que se está editando
        editing_service_id = row[0]
        page.update()

    # Función para agregar o actualizar un servicio
    def add_or_update_service(e):
        global editing_service_id  # Referencia a la variable global

        service_name = service_input.value
        price = price_input.value

        if service_name and price:
            try:
                price_float = float(price.replace('.', '').replace(',', ''))  # Convertir a float
            except ValueError:
                # Mostrar advertencia si el precio no es un número válido
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("El precio debe ser un número válido."),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())]
                )
                page.dialog.open = True
                page.update()
                return
            
            if editing_service_id:
                # Actualizar servicio existente
                database.update_service(editing_service_id, service_name, price_float)
                editing_service_id = None  # Resetear después de editar
            else:
                # Agregar un nuevo servicio
                database.insert_service(service_name, price_float)

            load_services()

            # Limpiar campos de entrada
            service_input.value = ""
            price_input.value = ""
            page.update()
        else:
            # Mostrar advertencia si faltan campos
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Por favor, llena todos los campos antes de continuar."),
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

    # Botón para agregar o actualizar servicio
    add_update_button = ft.ElevatedButton(text="Agregar/Actualizar Servicio", on_click=add_or_update_service)

    # Agregar controles a la vista de servicios
    main_content.controls.clear()
    main_content.controls.append(
        ft.Column([
            ft.Text("Gestión de Servicios", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
            service_input,
            price_input,
            add_update_button,
            services_table,
            ft.ElevatedButton(text="Volver", on_click=lambda e: load_main_view(main_content, page))  # Botón para volver
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)  # Alineación centrada)
    )
    page.update()
