#!/usr/bin/env python3
"""Main module of the netorcai library."""
import json
import socket
import struct

import netorcai.message

def recvall(sock, size, flags=0):
    '''Receive exactly the requested size on a socket.'''
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data), flags)
        if not packet:
            raise RuntimeError("Could not read on socket. Connection closed by remote?")
        data += packet
    return data

class Client:
    """A netorcai Client.

    Handles client-side communications of the netorcai metaprotocol.
    Most of the time, only the following methods should be called:
    - connect() and close(), to connect to or disconnect from netorcai
    - send_<MESSAGE_TYPE>, to send a message to netorcai
    - recv_<MESSAGE_TYPE>, to blockingly receive a message from netorcai
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.close()

    def connect(self, hostname="localhost", port=4242):
        self.socket.connect((hostname, port))

    def close(self):
        self.socket.close()

    def send_string(self, string):
        send_buffer = (string + "\n").encode('utf-8')

        # Send string size, as a little-endian uint16
        binary_size = struct.pack("<H", len(send_buffer))
        self.socket.sendall(binary_size)

        # Send string content
        self.socket.sendall(send_buffer)

    def send_json(self, j):
        self.send_string(json.dumps(j))

    def recv_string(self):
        # Read string size, as a little-endian uint16
        raw_bytes = recvall(self.socket, 2)
        content_size = struct.unpack('<H', raw_bytes)[0]

        # Read string content
        string = recvall(self.socket, content_size)
        return string.decode('utf-8')

    def recv_json(self):
        string = self.recv_string()
        return json.loads(string)

    def send_login(self, nickname, role):
        self.send_json({
            "message_type": "LOGIN",
            "nickname": nickname,
            "role": role
        })

    def send_turn_ack(self, turn_number, actions):
        self.send_json({
            "message_type": "TURN_ACK",
            "turn_number": turn_number,
            "actions": actions
        })

    def send_do_init_ack(self, initial_game_state):
        self.send_json({
            "message_type": "DO_INIT_ACK",
            "initial_game_state": initial_game_state
        })

    def send_do_turn_ack(self, game_state, winner_player_id):
        self.send_json({
            "message_type": "DO_TURN_ACK",
            "game_state": game_state,
            "winner_player_id": winner_player_id
        })

    def read_login_ack(self):
        msg = self.recv_json()
        if msg["message_type"] == "LOGIN_ACK":
            return netorcai.message.LoginAckMessage()
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))

    def read_game_starts(self):
        msg = self.recv_json()
        if msg["message_type"] == "GAME_STARTS":
            return netorcai.message.GameStartsMessage(msg)
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))

    def read_turn(self):
        msg = self.recv_json()
        if msg["message_type"] == "TURN":
            return netorcai.message.TurnMessage(msg)
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        elif msg["message_type"] == "GAME_ENDS":
            raise RuntimeError("Game over!")
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))

    def read_game_ends(self):
        msg = self.recv_json()
        if msg["message_type"] == "GAME_ENDS":
            return netorcai.message.GameEndsMessage(msg)
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))

    def read_do_init(self):
        msg = self.recv_json()
        if msg["message_type"] == "DO_INIT":
            return netorcai.message.DoInitMessage(msg)
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))

    def read_do_turn(self):
        msg = self.recv_json()
        if msg["message_type"] == "DO_TURN":
            return netorcai.message.DoTurnMessage(msg)
        elif msg["message_type"] == "KICK":
            raise RuntimeError("Kicked from netorcai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise RuntimeError("Unexpected message type received: {}".format(msg["message_type"]))
