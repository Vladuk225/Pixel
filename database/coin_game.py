# import sqlite3


# class CoinPVPGame:
#     def __init__(self, db_path='database.db'):
#         self.conn = sqlite3.connect(db_path)
#         self.cursor = self.conn.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cursor.execute("""
#         CREATE TABLE IF NOT EXISTS coin_pvp_games (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             initiator_id INTEGER,
#             opponent_id INTEGER,
#             bet INTEGER DEFAULT 0,
#             initiator_choice TEXT DEFAULT NULL,
#             opponent_choice TEXT DEFAULT NULL,
#             result TEXT DEFAULT NULL,
#             active INTEGER DEFAULT 1
#         )
#         """)
#         self.conn.commit()

#     def create_game(self, initiator_id: int, opponent_id: int):
#         self.cursor.execute("""
#         INSERT INTO coin_pvp_games (initiator_id, opponent_id)
#         VALUES (?, ?)
#         """, (initiator_id, opponent_id))
#         self.conn.commit()
#         return self.cursor.lastrowid

#     def set_bet(self, game_id: int, bet: int):
#         self.cursor.execute("""
#         UPDATE coin_pvp_games SET bet = ?
#         WHERE id = ? AND active = 1
#         """, (bet, game_id))
#         self.conn.commit()

#     def set_choice(self, game_id: int, user_id: int, choice: str):
#         if self.is_initiator(game_id, user_id):
#             self.cursor.execute("""
#             UPDATE coin_pvp_games SET initiator_choice = ?
#             WHERE id = ? AND active = 1
#             """, (choice, game_id))
#         else:
#             self.cursor.execute("""
#             UPDATE coin_pvp_games SET opponent_choice = ?
#             WHERE id = ? AND active = 1
#             """, (choice, game_id))
#         self.conn.commit()

#     def is_initiator(self, game_id: int, user_id: int):
#         self.cursor.execute("""
#         SELECT initiator_id FROM coin_pvp_games
#         WHERE id = ?
#         """, (game_id,))
#         row = self.cursor.fetchone()
#         return row and row[0] == user_id

#     def get_game(self, game_id: int):
#         self.cursor.execute("""
#         SELECT * FROM coin_pvp_games WHERE id = ?
#         """, (game_id,))
#         return self.cursor.fetchone()

#     def both_choices_made(self, game_id: int):
#         self.cursor.execute("""
#         SELECT initiator_choice, opponent_choice FROM coin_pvp_games
#         WHERE id = ?
#         """, (game_id,))
#         row = self.cursor.fetchone()
#         return row and row[0] and row[1]

#     def set_result(self, game_id: int, result: str):
#         self.cursor.execute("""
#         UPDATE coin_pvp_games SET result = ?, active = 0
#         WHERE id = ?
#         """, (result, game_id))
#         self.conn.commit()

#     def delete_game(self, game_id: int):
#         self.cursor.execute("DELETE FROM coin_pvp_games WHERE id = ?", (game_id,))
#         self.conn.commit()