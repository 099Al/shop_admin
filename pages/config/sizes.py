# Настройки окна
defaultWidthWindow = '1600'
defaultHeightWindow = '800'
page_min_width = 1200
page_min_height = 600

#Настройка размеров полей
pr_name_max_length = 150
pr_item_no_max_length = 25
pr_description_max_length = 350
pr_promo_desc_max_length = 350


#Названия должны совпадать с названиями в классе  self.name -> c_name  иначе не будет работать фильтр

d_category_width = {"edit": 80,
                   "name": 300,
                   "product_cnt": 150,
                   "order_sort": 130,
                   "el_height": 40
                    }

d_product_column_size = {"edit": 100,
                         "image": 100,
                         "name": 150,
                         "item_no": 100,
                         "price": 80,
                         "desc": 150,
                         "promo_price": 90,
                         "promo_end": 100,
                         "promo_desc": 150,
                         "category_name": 300,
                         "el_height": 40
                         }

d_category_product_column_size = {"edit": 100,
                                  "category_name": 300,
                                  "image": 70,
                                  "name": 300,
                                  "item_no": 100,
                                  "dell_add": 100,
                                  "el_height": 40
                                  }


d_admin_column_size = {"edit": 100,
                       "telegram_name": 130,
                        "role": 100,
                       "telegram_link": 100,
                       "phone": 130,
                       "email": 200,
                       "name": 100,
                       "password": 100,
                        "el_height": 40

                       }




d_client_column_size = {"edit": 100,
                        "telegram_name": 130,
                        "role": 100,
                        "telegram_link": 100,
                        "phone": 130,
                        "email": 200,
                        "name": 100,
                        "is_banned": 90,
                        "ban_reason": 200,
                        "dell": 50,
                        "el_height": 40

                        }

d_order_column_size = {"edit": 100,
                       "phone": 130,
                        "telegram_link": 100,
                       "created_at": 100,
                       "order_sum": 200,
                       "status": 100,
                       "payment_status": 100,
                       "order_id": 100,
                       "order_products": 100,
                       "delivery_address": 200,
                       "comment": 300,
                        "el_height": 40

                       }