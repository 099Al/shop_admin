import flet as ft

from pages.config.style import inputBgErrorColor


error_message_categtory = ft.SnackBar(
            content=ft.Text('Категория с таким названием уже существует'),
            bgcolor=inputBgErrorColor
        )
error_message_category_validate_order = ft.SnackBar(
            content=ft.Text('Неверный формат данных. Нужно задать число'),
            bgcolor=inputBgErrorColor
)

error_message_pk_name = ft.SnackBar(
            content=ft.Text('Продукт с таким названием уже существует'),
            bgcolor=inputBgErrorColor
        )

error_message_pk_item_no = ft.SnackBar(
            content=ft.Text('Продукт с таким артикулом уже существует'),
            bgcolor=inputBgErrorColor
        )

error_message_validation = ft.SnackBar(
            content=ft.Text('Неверный формат данных'),
            bgcolor=inputBgErrorColor
        )

error_message_image = ft.SnackBar(
            content=ft.Text('Неверный формат изображения'),
            bgcolor=inputBgErrorColor
        )

error_insert_product = ft.SnackBar(
            content=ft.Text('Ошибка при добавлении в базу данных'),
            bgcolor=inputBgErrorColor
        )

d_error_messages = {"error_pk_item_no": error_message_pk_item_no,
                    "error_pk_name": error_message_pk_name,
                    "validation_error": error_message_validation,
                    "image_error": error_message_image,
                    "insert_error": error_insert_product
                    }


d_error_messages_ctg_prod = ft.SnackBar(content=ft.Text(f"Товар уже находится в категории"), bgcolor=inputBgErrorColor)