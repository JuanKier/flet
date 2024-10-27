import flet as ft
from citas import load_appointments_view
from clientes import load_customers_view
from servicios import load_services_view

def load_main_view(main_content, page):
    main_content.controls.clear()
    
    # Contenedor para centrar todo el contenido
    main_container = ft.Container(
        alignment=ft.alignment.center,  # Alineación central
        padding=20,  # Agregar un poco de espacio alrededor
        
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Añadir la imagen como cabecera
                ft.Image(
                    src="logo.png",  # Reemplaza con la ruta a tu imagen
                    width=200,  # Ajusta el ancho según sea necesario
                    height=200,  # Ajusta la altura según sea necesario
                    fit=ft.ImageFit.COVER,  # Ajuste de la imagen
                ),
                ft.Text("May Scheroch Nails", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                ft.Text("Sistema de Gestión", theme_style="headlineMedium", text_align=ft.TextAlign.CENTER),
                ft.Text("Seleccione una opción para continuar:", text_align=ft.TextAlign.CENTER),
                
                # Usar un Column para los botones
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            text="Citas",
                            on_click=lambda e: load_appointments_view(main_content, page, load_main_view),
                            width=150,
                            height=60,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.colors.BLUE
                            ),
                        ),
                        ft.ElevatedButton(
                            text="Clientes",
                            on_click=lambda e: load_customers_view(main_content, page, load_main_view),
                            width=150,
                            height=60,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.colors.GREEN
                            ),
                        ),
                        ft.ElevatedButton(
                            text="Servicios",
                            on_click=lambda e: load_services_view(main_content, page, load_main_view),
                            width=150,
                            height=60,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.colors.ORANGE
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alineación de botones
                    spacing=10  # Espacio entre los botones
                ),
            ]
        )
    )
    
    # Añadir el contenedor centrado al main_content
    main_content.controls.append(main_container)
    page.update()
