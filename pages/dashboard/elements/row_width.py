

class RowWidth_Admin:
    def __init__(self):
        self._telegram_id = 1
        self._role = 1
        self._name = 1
        self._phone = 1
        self._email = 1
        self._login = 1

        self.letter_size = 9

    @property
    def telegram_id(self):
        return self._telegram_id
    @telegram_id.setter
    def telegram_id(self, value):
        self._telegram_id = max(self._telegram_id, len(str(value))*self.letter_size)


    @property
    def role(self):
        return self._role
    @role.setter
    def role(self, value):
        self._role = max(self._role, len(str(value))*self.letter_size)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = max(self._name, len(str(value))*self.letter_size)

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = max(self._phone, len(str(value))*self.letter_size)

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = max(self._email, len(str(value))*self.letter_size)

    @property
    def login(self):
        return self._login
    @login.setter
    def login(self, value):
        self._login = max(self._login, len(str(value))*self.letter_size)


class A:

    def __init__(self, r: RowWidth_Admin):
        self.r = r

    def get_r(self):
        return self.r.telegram_id
