import flet as ft
from data.database import guardar_cliente


def perfil_view(page: ft.Page, cliente):
    page.controls.clear()
    page.title = "Mi Perfil"
    page.window_resizable = True
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    editando = False

    nombres_field = ft.TextField(
        label="Nombres",
        value=cliente.get_nombres(),
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        read_only=True,
    )

    apellidos_field = ft.TextField(
        label="Apellidos",
        value=cliente.get_apellidos(),
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        read_only=True,
    )

    celular_field = ft.TextField(
        label="Celular",
        value=cliente.get_celular(),
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        read_only=True,
    )

    contraseña_field = ft.TextField(
        label="Contraseña",
        value=cliente.get_contraseña(),
        width=300,
        password=True,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        read_only=True,
    )

    foto_field = ft.TextField(
        label="URL Foto",
        value=cliente.get_foto(),
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        read_only=True,
    )

    mensaje_estado = ft.Text("", size=14, color=ft.Colors.GREEN)

    def editar_perfil(e):
        nonlocal editando
        editando = True
        nombres_field.read_only = False
        apellidos_field.read_only = False
        celular_field.read_only = False
        contraseña_field.read_only = False
        foto_field.read_only = False
        boton_editar.visible = False
        boton_guardar.visible = True
        boton_cancelar.visible = True
        page.update()

    def guardar_cambios(e):
        nonlocal editando
        
        if not nombres_field.value or not apellidos_field.value or not celular_field.value:
            mensaje_estado.value = "Completá todos los campos obligatorios"
            mensaje_estado.color = ft.Colors.RED
            page.update()
            return

        cliente.set_nombres(nombres_field.value)
        cliente.set_apellidos(apellidos_field.value)
        cliente.set_celular(celular_field.value)
        cliente.set_contraseña(contraseña_field.value)
        cliente.set_foto(foto_field.value)

        if guardar_cliente(cliente):
            mensaje_estado.value = "¡Perfil actualizado!"
            mensaje_estado.color = ft.Colors.GREEN
            editando = False
            nombres_field.read_only = True
            apellidos_field.read_only = True
            celular_field.read_only = True
            contraseña_field.read_only = True
            foto_field.read_only = True
            boton_editar.visible = True
            boton_guardar.visible = False
            boton_cancelar.visible = False
        else:
            mensaje_estado.value = "Error al guardar"
            mensaje_estado.color = ft.Colors.RED

        page.update()

    def cancelar_edicion(e):
        nonlocal editando
        editando = False
        nombres_field.value = cliente.get_nombres()
        apellidos_field.value = cliente.get_apellidos()
        celular_field.value = cliente.get_celular()
        contraseña_field.value = cliente.get_contraseña()
        foto_field.value = cliente.get_foto()
        nombres_field.read_only = True
        apellidos_field.read_only = True
        celular_field.read_only = True
        contraseña_field.read_only = True
        foto_field.read_only = True
        boton_editar.visible = True
        boton_guardar.visible = False
        boton_cancelar.visible = False
        mensaje_estado.value = ""
        page.update()

    def volver_menu(e):
        from views.home_view import menu_principal_view
        menu_principal_view(page, cliente)

    title = ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Mi Perfil", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
    )

    info_basica = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            padding=15,
            border_radius=10,
            content=ft.Column([
                ft.Text("Información Personal", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row([
                    ft.Text("Cédula:", size=14, color=ft.Colors.WHITE70),
                    ft.Text(cliente.get_cedula(), size=14, color=ft.Colors.WHITE),
                ]),
            ])
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    campos_editables = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        nombres_field,
        apellidos_field,
        celular_field,
        contraseña_field,
        foto_field,
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    boton_editar = ft.Button(
        color=ft.Colors.BLUE, 
        content=ft.Text("Editar Perfil", color=ft.Colors.WHITE, size=16), 
        on_click=editar_perfil,
        width=250
    )

    boton_guardar = ft.Button(
        color=ft.Colors.GREEN, 
        content=ft.Text("Guardar Cambios", color=ft.Colors.WHITE, size=16), 
        on_click=guardar_cambios,
        width=250,
        visible=False
    )

    boton_cancelar = ft.Button(
        color=ft.Colors.ORANGE, 
        content=ft.Text("Cancelar", color=ft.Colors.WHITE, size=14), 
        on_click=cancelar_edicion,
        width=250,
        visible=False
    )

    botones = ft.Column([
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        boton_editar,
        boton_guardar,
        boton_cancelar,
        mensaje_estado,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Button(
            color=ft.Colors.GREY, 
            content=ft.Text("Volver al Menú", color=ft.Colors.WHITE, size=14), 
            on_click=volver_menu,
            width=250
        ),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(title, info_basica, campos_editables, botones)
    page.update()