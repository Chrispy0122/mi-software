import flet as ft
import requests
import json

API_BASE_URL = "http://127.0.0.1:8000/v1/crm"

def crm_view(page: ft.Page):
    # Colors
    TURQUOISE = "#64FFDA"
    WHITE = "#FFFFFF"
    DARK_BLUE = "#0A192F"
    NAVY_BLUE = "#112240"
    LIGHT_GREY = "#8892b0"
    
    # Style helpers
    def styled_textfield(label, icon, width=None, expand=1, multiline=False, keyboard_type=None):
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            expand=expand,
            width=width,
            multiline=multiline,
            keyboard_type=keyboard_type,
            border_color=TURQUOISE,
            cursor_color=TURQUOISE,
            focused_border_color=TURQUOISE,
            color=WHITE,
            label_style=ft.TextStyle(color=TURQUOISE),
            text_style=ft.TextStyle(color=WHITE),
            border_radius=10,
            bgcolor=DARK_BLUE,
        )

    def styled_dropdown(label, icon, options, expand=1):
        return ft.Dropdown(
            label=label,
            prefix_icon=icon,
            expand=expand,
            options=options,
            border_color=TURQUOISE,
            focused_border_color=TURQUOISE,
            color=WHITE,
            label_style=ft.TextStyle(color=TURQUOISE),
            text_style=ft.TextStyle(color=WHITE),
            border_radius=10,
            bgcolor=DARK_BLUE,
        )

    def section_header(text):
        return ft.Container(
            content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color=LIGHT_GREY),
            padding=ft.padding.only(top=10, bottom=5),
        )

    def show_dialog(title, message, is_error=False):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        icon = ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=50) if is_error else ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=TURQUOISE, size=50)

        page.dialog = ft.AlertDialog(
            title=ft.Column([
                ft.Container(content=icon, alignment=ft.alignment.center),
                ft.Container(content=ft.Text(title, color=ft.Colors.RED if is_error else TURQUOISE, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center)
            ], spacing=10, tight=True),
            content=ft.Container(
                content=ft.Text(message, color=WHITE, size=16, text_align=ft.TextAlign.CENTER),
                padding=10,
                alignment=ft.alignment.center
            ),
            actions=[
                ft.Container(
                    content=ft.ElevatedButton("OK", on_click=close_dialog, bgcolor=TURQUOISE, color=DARK_BLUE),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=10)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=NAVY_BLUE,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        page.dialog.open = True
        page.update()

    # --- Client Form ---
    client_name = styled_textfield("Name", ft.Icons.PERSON)
    business_name = styled_textfield("Business Name", ft.Icons.BUSINESS)
    industry = styled_textfield("Industry", ft.Icons.FACTORY)
    
    country = styled_textfield("Country", ft.Icons.PUBLIC)
    city = styled_textfield("City", ft.Icons.LOCATION_CITY)
    
    email = styled_textfield("Email", ft.Icons.EMAIL)
    phone = styled_textfield("Phone", ft.Icons.PHONE)
    
    instagram = styled_textfield("Instagram", ft.Icons.CAMERA_ALT)
    tiktok = styled_textfield("TikTok", ft.Icons.MUSIC_NOTE)
    website = styled_textfield("Website", ft.Icons.LANGUAGE)
    
    status = styled_dropdown(
        "Status",
        ft.Icons.TOGGLE_ON,
        options=[
            ft.dropdown.Option("Active"),
            ft.dropdown.Option("Inactive"),
            ft.dropdown.Option("Lead"),
        ],
    )
    notes = styled_textfield("Notes", ft.Icons.NOTE, multiline=True)

    def save_client(e):
        data = {
            "name": client_name.value,
            "business_name": business_name.value,
            "industry": industry.value,
            "country": country.value,
            "city": city.value,
            "email": email.value,
            "phone": phone.value,
            "instagram_handle": instagram.value,
            "tiktok_handle": tiktok.value,
            "website": website.value,
            "status": status.value,
            "notes": notes.value,
        }
        
        # Basic validation
        if not data["name"]:
            show_dialog("Validation Error", "Name is required", is_error=True)
            return

        try:
            print(f"Sending client data: {data}")
            response = requests.post(f"{API_BASE_URL}/clients", json=data)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                show_dialog("Guardado Exitoso", "El cliente se ha guardado correctamente en la base de datos.")
                # Clear form fields
                client_name.value = ""
                business_name.value = ""
                industry.value = ""
                country.value = ""
                city.value = ""
                email.value = ""
                phone.value = ""
                instagram.value = ""
                tiktok.value = ""
                website.value = ""
                notes.value = ""
                page.update()
            else:
                show_dialog("Error al Guardar", f"No se pudo guardar el cliente. Error del servidor: {response.text}", is_error=True)
        except Exception as ex:
            print(f"Exception: {ex}")
            show_dialog("Error de Conexión", f"No se pudo conectar con el servidor. Verifique que el backend esté corriendo. Detalles: {ex}", is_error=True)

    client_form_content = ft.Column(
        [
            ft.Text("Client Details", size=24, weight=ft.FontWeight.BOLD, color=TURQUOISE),
            ft.Divider(color=TURQUOISE, thickness=1),
            
            section_header("Basic Info"),
            ft.Row([client_name, business_name]),
            ft.Row([industry, status]),
            
            section_header("Location"),
            ft.Row([country, city]),
            
            section_header("Contact"),
            ft.Row([email, phone]),
            
            section_header("Social & Web"),
            ft.Row([instagram, tiktok]),
            ft.Row([website]),
            
            section_header("Other"),
            notes,
            
            ft.Container(height=10),
            ft.ElevatedButton(
                "Save Client", 
                icon=ft.Icons.SAVE,
                on_click=save_client,
                bgcolor=TURQUOISE,
                color=DARK_BLUE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                height=50,
                width=200,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
    )

    # --- Project Form ---
    client_id = styled_textfield("Client ID", ft.Icons.NUMBERS)
    project_name = styled_textfield("Project Name", ft.Icons.WORK)
    project_type = styled_textfield("Type", ft.Icons.CATEGORY)
    
    start_date = styled_textfield("Start Date (YYYY-MM-DD)", ft.Icons.CALENDAR_TODAY)
    end_date = styled_textfield("End Date (YYYY-MM-DD)", ft.Icons.EVENT)
    
    project_status = styled_dropdown(
        "Status",
        ft.Icons.FLAG,
        options=[
            ft.dropdown.Option("Planned"),
            ft.dropdown.Option("In Progress"),
            ft.dropdown.Option("Completed"),
            ft.dropdown.Option("On Hold"),
        ],
    )
    
    monthly_fee = styled_textfield("Monthly Fee", ft.Icons.ATTACH_MONEY, keyboard_type=ft.KeyboardType.NUMBER)
    currency = styled_dropdown(
        "Currency",
        ft.Icons.MONEY,
        options=[
            ft.dropdown.Option("USD"),
            ft.dropdown.Option("EUR"),
            ft.dropdown.Option("Local"),
        ],
    )
    
    project_notes = styled_textfield("Notes", ft.Icons.NOTE, multiline=True)
    sdlc_id = styled_textfield("SDLC ID", ft.Icons.CODE)

    def save_project(e):
        try:
            fee = float(monthly_fee.value) if monthly_fee.value else 0.0
        except ValueError:
            show_dialog("Error de Validación", "La tarifa mensual debe ser un número", is_error=True)
            return

        data = {
            "client_id": client_id.value, # Needs to be int
            "name": project_name.value,
            "type": project_type.value,
            "start_date": start_date.value if start_date.value else None,
            "end_date": end_date.value if end_date.value else None,
            "status": project_status.value,
            "monthly_fee": fee,
            "currency": currency.value,
            "notes": project_notes.value,
            "sdlc_id": int(sdlc_id.value) if sdlc_id.value else None,
        }

        if not data["client_id"]:
             show_dialog("Error de Validación", "El ID del Cliente es obligatorio", is_error=True)
             return
        
        try:
             data["client_id"] = int(data["client_id"])
        except ValueError:
             show_dialog("Error de Validación", "El ID del Cliente debe ser un número entero", is_error=True)
             return

        if not data["name"]:
            show_dialog("Error de Validación", "El Nombre del Proyecto es obligatorio", is_error=True)
            return

        try:
            print(f"Sending project data: {data}")
            response = requests.post(f"{API_BASE_URL}/projects", json=data)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                show_dialog("Guardado Exitoso", "El proyecto se ha guardado correctamente.")
            else:
                show_dialog("Error", f"Error del servidor: {response.text}", is_error=True)
        except Exception as ex:
            print(f"Exception: {ex}")
            show_dialog("Error de Conexión", f"No se pudo conectar con el servidor: {ex}", is_error=True)


    project_form_content = ft.Column(
        [
            ft.Text("Project Details", size=24, weight=ft.FontWeight.BOLD, color=TURQUOISE),
            ft.Divider(color=TURQUOISE, thickness=1),
            
            section_header("Project Info"),
            ft.Row([client_id, project_name]),
            ft.Row([project_type, project_status]),
            
            section_header("Timeline"),
            ft.Row([start_date, end_date]),
            
            section_header("Financials"),
            ft.Row([monthly_fee, currency]),
            
            section_header("Technical"),
            ft.Row([sdlc_id]),
            
            section_header("Other"),
            project_notes,
            
            ft.Container(height=10),
            ft.ElevatedButton(
                "Save Project", 
                icon=ft.Icons.SAVE,
                on_click=save_project,
                bgcolor=TURQUOISE,
                color=DARK_BLUE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                height=50,
                width=200,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
    )

    # Main Layout: Split Screen with Cards
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=client_form_content, 
                    expand=True, 
                    padding=30,
                    bgcolor=NAVY_BLUE,
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color="#4D000000",
                    )
                ),
                ft.Container(width=20), # Spacer
                ft.Container(
                    content=project_form_content, 
                    expand=True, 
                    padding=30,
                    bgcolor=NAVY_BLUE,
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color="#4D000000",
                    )
                ),
            ],
            expand=True,
        ),
        expand=True,
        padding=20,
    )
