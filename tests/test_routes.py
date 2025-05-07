from flask import Flask, jsonify
import pytest

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the AI Chatbot' in response.data

def test_chat_route(client):
    response = client.post('/chat', json={'message': 'Hello'})
    assert response.status_code == 200
    assert 'response' in response.json

def test_invalid_chat_route(client):
    response = client.post('/chat', json={})
    assert response.status_code == 400
    assert b'Invalid input' in response.data