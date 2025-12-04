import flet as ft

def client_management_view(page: ft.Page):
    # Colors
    TURQUOISE = "#64FFDA"
    WHITE = "#FFFFFF"
    DARK_BLUE = "#0A192F"

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Manejo de Clientes", size=30, weight=ft.FontWeight.BOLD, color=TURQUOISE),
                ft.Text("Aquí podrás ver y gestionar tus clientes y proyectos.", color=WHITE),
                # Placeholder for table
                ft.Container(
                    content=ft.Text("Tabla de Clientes (Próximamente)", color=DARK_BLUE),
                    bgcolor=TURQUOISE,
                    padding=20,
                    border_radius=10,
                    alignment=ft.alignment.center,
                )
            ],
            spacing=20,
        ),
        padding=30,
        expand=True,
    )
