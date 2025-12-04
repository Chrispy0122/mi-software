import flet as ft
from desktop_app.crm_frontend.crm import crm_view
from desktop_app.crm_frontend.placeholders import kpi_view, agenda_view, ia_view
from desktop_app.crm_frontend.client_management import client_management_view

def main(page: ft.Page):
    # Colors
    DARK_BLUE = "#0A192F"
    NAVY_BLUE = "#112240"
    TURQUOISE = "#64FFDA"
    WHITE = "#FFFFFF"
    LIGHT_GREY = "#CCD6F6"

    page.title = "CRM Desktop App"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = DARK_BLUE
    page.padding = 0

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, color=TURQUOISE),
        leading_width=40,
        title=ft.Text("SEÑU", weight=ft.FontWeight.BOLD, color=WHITE),
        center_title=False,
        bgcolor=NAVY_BLUE,
        actions=[
            ft.Container(
                content=ft.Text("CRM", weight=ft.FontWeight.BOLD, color=TURQUOISE),
                padding=ft.padding.only(right=20)
            )
        ],
    )

    # Content area that will change based on selection
    content_area = ft.Container(expand=True)

    def set_content(view_func):
        content_area.content = view_func(page)
        content_area.update()

    # Sidebar Item Helper
    def sidebar_item(icon, label, on_click):
        return ft.ListTile(
            leading=ft.Icon(icon, color=TURQUOISE),
            title=ft.Text(label, color=WHITE),
            on_click=on_click,
            hover_color="#1A64FFDA",
        )

    # Custom Sidebar
    sidebar = ft.Container(
        width=250,
        bgcolor=NAVY_BLUE,
        padding=10,
        content=ft.Column(
            [
                sidebar_item(ft.Icons.DASHBOARD, "KPI", lambda e: set_content(kpi_view)),
                
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.PEOPLE, color=TURQUOISE),
                    title=ft.Text("CRM", color=WHITE),
                    collapsed_icon_color=TURQUOISE,
                    icon_color=TURQUOISE,
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Formulario", color=LIGHT_GREY),
                            leading=ft.Icon(ft.Icons.DESCRIPTION, color=LIGHT_GREY, size=20),
                            on_click=lambda e: set_content(crm_view),
                            content_padding=ft.padding.only(left=30),
                        ),
                        ft.ListTile(
                            title=ft.Text("Manejo de Clientes", color=LIGHT_GREY),
                            leading=ft.Icon(ft.Icons.TABLE_CHART, color=LIGHT_GREY, size=20),
                            on_click=lambda e: set_content(client_management_view),
                            content_padding=ft.padding.only(left=30),
                        ),
                    ]
                ),

                sidebar_item(ft.Icons.CALENDAR_TODAY, "AGENDA", lambda e: set_content(agenda_view)),
                sidebar_item(ft.Icons.SMART_TOY, "IA", lambda e: set_content(ia_view)),
            ],
            spacing=5,
        )
    )

    # Set initial content to CRM
    content_area.content = crm_view(page)

    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1, color=TURQUOISE),
                content_area,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
