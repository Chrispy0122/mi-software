import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    import flet as ft
    print("flet imported")
    from desktop_app.views.crm import crm_view
    print("crm_view imported")
    from desktop_app.views.placeholders import kpi_view
    print("placeholders imported")
    from desktop_app.views.client_management import client_management_view
    print("client_management_view imported")
    print("All imports successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
