class FamilyStructure:

    def __init__(self, last_name: str):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

        # Miembros iniciales (John, Jane, Jimmy)
        self.add_member({
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        self.add_member({
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        self.add_member({
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        })

    # NO TOCAR: genera IDs únicos
    def _generate_id(self) -> int:
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member: dict) -> dict:
        """
        Agrega un nuevo miembro a la familia.
        Si no trae id, se genera uno.
        El last_name SIEMPRE es el de la familia.
        """
        if member.get("id") is None:
            member["id"] = self._generate_id()

        member["last_name"] = self.last_name

        self._members.append(member)
        return member

    def delete_member(self, id: int) -> bool:
        """
        Elimina el miembro cuyo id coincida.
        Devuelve True si se ha eliminado, False si no existía.
        """
        original_len = len(self._members)
        self._members = [m for m in self._members if m["id"] != id]
        return len(self._members) != original_len

    def get_member(self, id: int) -> dict | None:
        """
        Devuelve el miembro con ese id o None si no existe.
        """
        for m in self._members:
            if m["id"] == id:
                return m
        return None

    def get_all_members(self) -> list[dict]:
        """
        Devuelve la lista completa de miembros.
        """
        return self._members
