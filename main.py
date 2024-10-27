import flet as ft
from views import load_main_view

def main(page: ft.Page):
    page.title = "Gestión de Citas - Manicura y Pedicura"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "auto"

    # Contenedor principal para la vista
    main_content = ft.Column()
    page.add(main_content)

    # Cargar vista principal
    load_main_view(main_content, page)

if __name__ == "__main__":
    ft.app(target=main)
