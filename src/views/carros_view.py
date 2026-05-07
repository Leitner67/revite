import flet as ft
from core.constants import AppColors
from data.database import cargar_carros, guardar_carro, eliminar_carro
from models.carros import Carro


def ver_carros_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Gestión de Carros"
    page.window_resizable = True
    page.bgcolor = AppColors.BACKGROUND
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    glow_shadow = ft.BoxShadow(
        spread_radius=0,
        blur_radius=16,
        color=AppColors.GLOW_PRIMARY,
        offset=ft.Offset(0, 0),
    )

    carro_editando = {"placa": None}
    
    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)
    
    def actualizar_lista():
        carros = cargar_carros()
        carros_container.controls.clear()
        
        if not carros:
            carros_container.controls.append(
                ft.Container(
                    padding=30,
                    content=ft.Column([
                        ft.Icon(ft.Icons.DIRECTIONS_CAR_OUTLINED, size=80, color=AppColors.TEXT_SECONDARY),
                        ft.Text("No hay carros registrados", size=18, color=AppColors.TEXT_SECONDARY),
                        ft.Text("Agregá tu primer carro usando el botón de arriba", size=14, color=AppColors.TEXT_SECONDARY),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            )
        else:
            for carro in carros:
                carros_container.controls.append(crear_carro_card(carro))
        
        page.update()
    
    def mostrar_dialog_carro(e, carro=None):
        es_edicion = carro is not None

        marca_field = ft.TextField(
            label="Marca",
            hint_text="Ej: Toyota, Chevrolet, Mazda",
            value=carro.get_marca() if es_edicion else "",
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.BUSINESS,
            autofocus=True,
        )
        
        modelo_field = ft.TextField(
            label="Modelo",
            hint_text="Ej: Corolla, Spark, 3",
            value=carro.get_modelo() if es_edicion else "",
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.DIRECTIONS_CAR,
        )
        
        ano_field = ft.TextField(
            label="Año",
            hint_text="Ej: 2024",
            value=str(carro.get_ano()) if es_edicion else "",
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        placa_field = ft.TextField(
            label="Placa",
            hint_text="Ej: ABC123",
            value=carro.get_placa() if es_edicion else "",
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.PIN,
            capitalization=ft.TextCapitalization.CHARACTERS,
            disabled=es_edicion,
        )
        
        error_text = ft.Text("", color=AppColors.ERROR, size=12)
        
        def guardar_carro_action(e):
            try:
                if not marca_field.value or not modelo_field.value or not ano_field.value or not placa_field.value:
                    error_text.value = "Todos los campos son obligatorios"
                    page.update()
                    return

                nuevo_carro = Carro(
                    marca=marca_field.value,
                    modelo=modelo_field.value,
                    ano=int(ano_field.value),
                    placa=placa_field.value
                )
                
                if guardar_carro(nuevo_carro):
                    dialog.open = False
                    actualizar_lista()

                    page.overlay.append(
                        ft.SnackBar(
                            content=ft.Text(
                                f"✓ Carro {'actualizado' if es_edicion else 'agregado'} exitosamente",
                                color=AppColors.TEXT_PRIMARY
                            ),
                            bgcolor=AppColors.SUCCESS,
                        )
                    )
                    page.overlay[-1].open = True
                    page.update()
                else:
                    error_text.value = "Error al guardar el carro"
                    page.update()
                    
            except ValueError as ve:
                error_text.value = str(ve)
                page.update()
            except Exception as ex:
                error_text.value = f"Error: {str(ex)}"
                page.update()
        
        def cerrar_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.EDIT if es_edicion else ft.Icons.ADD_CIRCLE, color=AppColors.PRIMARY),
                ft.Text(f"{'Editar' if es_edicion else 'Agregar'} Carro", size=20),
            ]),
            content=ft.Container(
                width=400,
                content=ft.Column([
                    marca_field,
                    modelo_field,
                    ano_field,
                    placa_field,
                    error_text,
                ],
                tight=True,
                spacing=15,
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialog),
                ft.ElevatedButton(
                    "Guardar",
                    icon=ft.Icons.SAVE,
                    on_click=guardar_carro_action,
                    bgcolor=AppColors.BUTTON_PRIMARY_BG,
                    color=AppColors.BUTTON_TEXT,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def confirmar_eliminar_carro(e, carro):
        def eliminar_action(e):
            if eliminar_carro(carro.get_placa()):
                dialog_confirm.open = False
                actualizar_lista()

                page.overlay.append(
                    ft.SnackBar(
                        content=ft.Text("✓ Carro eliminado exitosamente", color=AppColors.TEXT_PRIMARY),
                        bgcolor=AppColors.WARNING,
                    )
                )
                page.overlay[-1].open = True
                page.update()
        
        def cerrar_confirm(e):
            dialog_confirm.open = False
            page.update()
        
        dialog_confirm = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=AppColors.WARNING),
                ft.Text("Confirmar Eliminación", size=20),
            ]),
            content=ft.Text(
                f"¿Estás seguro que querés eliminar el carro {carro.get_marca()} {carro.get_modelo()} ({carro.get_placa()})?",
                size=16
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_confirm),
                ft.ElevatedButton(
                    "Eliminar",
                    icon=ft.Icons.DELETE,
                    on_click=eliminar_action,
                    bgcolor=AppColors.BUTTON_DANGER_BG,
                    color=AppColors.BUTTON_TEXT,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog_confirm)
        dialog_confirm.open = True
        page.update()
    
    def crear_carro_card(carro):
        return ft.Container(
            bgcolor=AppColors.CARD,
            padding=20,
            margin=ft.margin.only(bottom=15),
            border_radius=15,
            width=600,
            shadow=glow_shadow,
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        bgcolor=AppColors.SURFACE,
                        padding=15,
                        border_radius=10,
                        content=ft.Icon(ft.Icons.DIRECTIONS_CAR, color=AppColors.TEXT_PRIMARY, size=35),
                    ),
                    ft.Column([
                        ft.Text(
                            f"{carro.get_marca()} {carro.get_modelo()}",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.TEXT_PRIMARY
                        ),
                        ft.Text(
                            f"Placa: {carro.get_placa()}",
                            size=14,
                            color=AppColors.SECONDARY,
                            weight=ft.FontWeight.W_500
                        ),
                    ],
                    spacing=5,
                    expand=True,
                    ),
                    ft.Container(
                        bgcolor=AppColors.SURFACE,
                        padding=10,
                        border_radius=8,
                        content=ft.Text(
                            str(carro.get_ano()),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.TEXT_PRIMARY
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(height=1, color=AppColors.BORDER),
                ft.Row([
                    ft.TextButton(
                        "Editar",
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, c=carro: mostrar_dialog_carro(e, c),
                        style=ft.ButtonStyle(color=AppColors.PRIMARY),
                    ),
                    ft.TextButton(
                        "Eliminar",
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, c=carro: confirmar_eliminar_carro(e, c),
                        style=ft.ButtonStyle(color=AppColors.HIGHLIGHT),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=10,
            )
        )

    title = ft.Container(
        padding=20,
        border=ft.Border.all(2, AppColors.BORDER),
        border_radius=15,
        bgcolor=AppColors.CARD,
        shadow=glow_shadow,
        content=ft.Row([
            ft.Icon(ft.Icons.DIRECTIONS_CAR, size=35, color=AppColors.PRIMARY),
            ft.Text("Gestión de Carros", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
    
    boton_agregar = ft.Container(
        padding=ft.padding.only(top=20, bottom=10),
        content=ft.ElevatedButton(
            "Agregar Nuevo Carro",
            icon=ft.Icons.ADD_CIRCLE,
            on_click=mostrar_dialog_carro,
            bgcolor=AppColors.BUTTON_PRIMARY_BG,
            color=AppColors.BUTTON_TEXT,
            height=50,
            width=250,
            style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
        ),
    )
    
    carros_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    boton_volver = ft.Container(
        padding=ft.padding.only(top=20),
        content=ft.Button(
            "Volver al Menú",
            icon=ft.Icons.ARROW_BACK,
            color=AppColors.BUTTON_NEUTRAL_BG,
            on_click=volver_menu,
            width=250,
        ),
    )

    actualizar_lista()

    page.add(
        title,
        boton_agregar,
        carros_container,
        boton_volver
    )
    page.update()
