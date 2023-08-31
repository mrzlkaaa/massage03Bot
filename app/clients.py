
class Clients:
    def __init__(
        self,
        db
    ):
        self.db = db

    def _isexists(self):
        return
    
    def _client_pattern(self, client: object):
        #* client is User objcet from TG
        return {
            "tg_id": client.id,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "username": client.username,
        }

    def _contact_pattern(self, contact: object):
        return

    def add_client(self, client):
        parsed_client = self._client_pattern(client)
        res = self.db.insert(
            parsed_client,
            "clients"
        )
        return res

    def get_by_tgid(self, tg_id: int):
        res = self.db.select_by_tgid(tg_id)
        return res

    def get_by_phone_number(self):
        return

    def update(
        self, 
        tg_id: int,
        data: dict
    ):
        res = self.db.update(
            tg_id,
            data,
            "clients"
        )
        return res

    def delete(self):
        return