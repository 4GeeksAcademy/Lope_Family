"""
This module contains the FamilyStructure class
"""

import random

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []
        self._id_counter = 1

    def get_all_members(self):
        return self._members

    
    def get_member(self, member_id):
        for member in self._members:
            if member["id"] == member_id:
                return member
        return None

    
    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._id_counter
            self._id_counter += 1
        self._members.append(member)
        return member
    
    def delete_member(self, member_id):
        for i, member in enumerate(self._members):
            if member["id"] == member_id:
                del self._members[i]
                return True
        return False
