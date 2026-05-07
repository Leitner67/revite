import flet as ft
from core.constants import AppColors
from data.database import guardar_cliente


def perfil_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Mi Perfil"
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
    
    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)
    
    def actualizar_vista():
        page.controls.clear()
        renderizar_vista()
        page.update()
    
    def mostrar_mensaje(mensaje, es_error=False):
        page.overlay.append(
            ft.SnackBar(
                content=ft.Text(mensaje, color=AppColors.TEXT_PRIMARY),
                bgcolor=AppColors.ERROR if es_error else AppColors.SUCCESS,
            )
        )
        page.overlay[-1].open = True
        page.update()
    
    def editar_perfil(e):
        nombres_field = ft.TextField(
            label="Nombres",
            value=cliente.get_nombres(),
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.PERSON,
            autofocus=True,
        )
        
        apellidos_field = ft.TextField(
            label="Apellidos",
            value=cliente.get_apellidos(),
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.PERSON_OUTLINE,
        )
        
        celular_field = ft.TextField(
            label="Celular",
            value=cliente.get_celular(),
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.PHONE,
            keyboard_type=ft.KeyboardType.PHONE,
        )
        
        contraseña_field = ft.TextField(
            label="Contraseña",
            value=cliente.get_contraseña(),
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
        )
        
        foto_field = ft.TextField(
            label="Foto del Cliente",
            value=cliente.get_foto(),
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            prefix_icon=ft.Icons.PHOTO,
            hint_text="Ruta local de la foto",
        )
        
        error_text = ft.Text("", color=AppColors.ERROR, size=12)
        
        def guardar_cambios(e):
            try:
                if not nombres_field.value or not apellidos_field.value or not celular_field.value:
                    error_text.value = "Nombres, apellidos y celular son obligatorios"
                    page.update()
                    return
                
                if not contraseña_field.value or len(contraseña_field.value) < 4:
                    error_text.value = "La contraseña debe tener al menos 4 caracteres"
                    page.update()
                    return

                cliente.set_nombres(nombres_field.value)
                cliente.set_apellidos(apellidos_field.value)
                cliente.set_celular(celular_field.value)
                cliente.set_contraseña(contraseña_field.value)
                cliente.set_foto(foto_field.value)

                if guardar_cliente(cliente):
                    dialog.open = False
                    actualizar_vista()
                    mostrar_mensaje("✓ Perfil actualizado exitosamente")
                else:
                    error_text.value = "Error al guardar los cambios"
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
                ft.Icon(ft.Icons.EDIT, color=AppColors.PRIMARY),
                ft.Text("Editar Perfil", size=20),
            ]),
            content=ft.Container(
                width=400,
                content=ft.Column([
                    nombres_field,
                    apellidos_field,
                    celular_field,
                    contraseña_field,
                    foto_field,
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
                    on_click=guardar_cambios,
                    bgcolor=AppColors.BUTTON_PRIMARY_BG,
                    color=AppColors.BUTTON_TEXT,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def renderizar_vista():
        title = ft.Container(
            padding=20,
            border=ft.Border.all(2, AppColors.BORDER),
            border_radius=15,
            bgcolor=AppColors.CARD,
            shadow=glow_shadow,
            content=ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=35, color=AppColors.PRIMARY),
                ft.Text("Mi Perfil", size=30, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        foto_cliente = (cliente.get_foto() or "").strip()

        if foto_cliente:
            foto_control = ft.Image(
                src=foto_cliente,
                width=150,
                height=150,
                fit=ft.BoxFit.COVER,
                border_radius=ft.border_radius.all(75),
                error_content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=120, color=AppColors.TEXT_SECONDARY),
            )
        else:
            foto_control = ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=120, color=AppColors.TEXT_SECONDARY)
        
        foto_container = ft.Container(
            padding=20,
            margin=ft.margin.only(top=20),
            bgcolor=AppColors.CARD,
            border_radius=15,
            width=400,
            shadow=glow_shadow,
            content=ft.Column([
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=foto_control,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text(
                    f"{cliente.get_nombres()} {cliente.get_apellidos()}",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.TEXT_PRIMARY,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"CC: {cliente.get_cedula()}",
                    size=14,
                    color=AppColors.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        info_card = ft.Container(
            padding=20,
            margin=ft.margin.only(top=15),
            bgcolor=AppColors.CARD,
            border_radius=15,
            width=400,
            shadow=glow_shadow,
            content=ft.Column([
                ft.Text("Información de Contacto", size=18, weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY),
                ft.Divider(height=1, color=AppColors.BORDER),
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, color=AppColors.PRIMARY, size=20),
                    ft.Text("Celular:", size=14, color=AppColors.TEXT_SECONDARY),
                    ft.Text(cliente.get_celular(), size=14, color=AppColors.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.LOCK, color=AppColors.SECONDARY, size=20),
                    ft.Text("Contraseña:", size=14, color=AppColors.TEXT_SECONDARY),
                    ft.Text("•" * len(cliente.get_contraseña()), size=14, color=AppColors.TEXT_PRIMARY),
                ]),
            ],
            spacing=10,
            )
        )

        botones = ft.Container(
            padding=ft.padding.only(top=20),
            content=ft.Column([
                ft.ElevatedButton(
                    "Editar Perfil",
                    icon=ft.Icons.EDIT,
                    on_click=editar_perfil,
                    bgcolor=AppColors.BUTTON_PRIMARY_BG,
                    color=AppColors.BUTTON_TEXT,
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(shadow_color=AppColors.GLOW_PRIMARY, elevation=6),
                ),
                ft.Button(
                    "Volver al Menú",
                    icon=ft.Icons.ARROW_BACK,
                    color=AppColors.BUTTON_NEUTRAL_BG,
                    on_click=volver_menu,
                    width=250,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            )
        )
        
        page.add(
            title,
            foto_container,
            info_card,
            botones
        )
    
    renderizar_vista()
    page.update()
