class BaseMixin:
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)