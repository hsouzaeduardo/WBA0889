from flask import jsonify
from app import add_item
 
def test_add_item(self, mock_add):
    mock_add.return_value = jsonify({'status': 'success', 'name': 'Teste'}), 201
    response = add_item('NomeTeste', 'DataTeste', 'QuartoTeste', 'AvaliaçãoTeste', 5)
    self.assertEqual(response[0].json, {'status': 'success', 'name': 'Teste'})
    self.assertEqual(response[1], 201)