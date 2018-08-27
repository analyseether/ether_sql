from decimal import Decimal
import datetime

EXPECTED_META_INFO = {'last_pushed_block': Decimal('56170'),
                      'current_state_block': None}


EXPECTED_BLOCK_PROPERTIES = {'block_number': Decimal('56160'),
                             'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
                             'transaction_count': Decimal('1'),
                             'block_hash': u'0x685b2226cbf6e1f890211010aa192bf16f0a0cba9534264a033b023d7367b845',
                             'difficulty': Decimal('1640036045719'),
                             'uncle_count': Decimal('1'),
                             'sha3uncles': u'0x8a67da3121c69b45a19f4674a7272ebad677f9775ca6b35d79067974ca687a64',
                             'miner': u'0x3F98e477a361F777DA14611a7e419A75Fd238b6b',
                             'gas_used': Decimal('50290'),
                             'parent_hash': u'0x071218ca3c6549337289e5e0e78227f59a82d62a972d6d73e6b8e55dcbaa65eb',
                             'extra_data': u'0x476574682f76312e302e312f6c696e75782f676f312e342e32',
                             'gas_limit': Decimal('3141592')}

EXPECTED_UNCLE_PROPERTIES = {'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
                             'current_blocknumber': Decimal('56160'),
                             'difficulty': u'1640036436734',
                             'sha3uncles': u'0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
                             'uncle_blocknumber': Decimal('56158'),
                             'miner': u'0xbe4532E1B1Db5c913Cf553be76180c1777055403',
                             'gas_used': Decimal('0'),
                             'uncle_hash': u'0xc78c35720d930f9ef34b4e6fb9d02ffec936f9b02a8f0fa858456e4afd4d5614',
                             'parent_hash': u'0xcc30e8a9b15c548d5bf113c834143a8f0e1909fbfea96b2a208dc154293a78cf',
                             'extra_data': u'0x476574682f686261722f76312e302e312f6c696e75782f676f312e342e32',
                             'gas_limit': Decimal('3141592')}

EXPEXTED_TRANSACTION_PROPERTIES = {'nonce': Decimal('6'),
                                   'block_number': Decimal('56160'),
                                   'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
                                   'transaction_hash': u'0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
                                   'transaction_index': Decimal('0'),
                                   'data': u'0x90b98a110000000000000000000000006463f715d594a1a4ace4bb9c3b288a74decf294d00000000000000000000000000000000000000000000000000000000000003e8',
                                   'gas_price': Decimal('57105088684'),
                                   'sender': u'0x9B2c46642CAF6B936dc0633da521f1E946B7e18F',
                                   'value': Decimal('0'),
                                   'receiver': u'0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
                                   'start_gas': Decimal('90000')}

EXPECTED_RECEIPT_PROPERTIES = {'status': None,
                               'block_number': Decimal('56160'),
                               'contract_address': None,
                               'transaction_index': Decimal('0'),
                               'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
                               'cumulative_gas_used': Decimal('50290'),
                               'transaction_hash': u'0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
                               'gas_used': Decimal('50290')}

EXPECTED_LOG_PROPERTIES = {'block_number': Decimal('56160'),
                           'topics_count': Decimal('1'),
                           'log_index': Decimal('0'),
                           'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
                           'transaction_hash': u'0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
                           'topic_4': u'',
                           'topic_3': u'',
                           'topic_2': u'',
                           'topic_1': u'0x16cdf1707799c6655baac6e210f52b94b7cec08adcaf9ede7dfe8649da926146',
                           'address': u'0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
                           'transaction_index': Decimal('0'),
                           'data': u'0x0000000000000000000000009b2c46642caf6b936dc0633da521f1e946b7e18f0000000000000000000000006463f715d594a1a4ace4bb9c3b288a74decf294d00000000000000000000000000000000000000000000000000000000000003e8'}

EXPECTED_TRACE_PROPERTIES = {'subtraces': Decimal('0'),
                             'output': '0x0000000000000000000000000000000000000000000000000000000000000001',
                             'gas_used': Decimal('27354'),
                             'trace_address': '{}',
                             'contract_address': '',
                             'error': '',
                             'receiver': '0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
                             'sender': '0x9B2c46642CAF6B936dc0633da521f1E946B7e18F',
                             'start_gas': Decimal('67064'),
                             'value': Decimal('0'),
                             'trace_type': 'call',
                             'input_data': '0x90b98a110000000000000000000000006463f715d594a1a4ace4bb9c3b288a74decf294d00000000000000000000000000000000000000000000000000000000000003e8',
                             'transaction_index': Decimal('0'),
                             'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
                             'block_number': Decimal('56160')}


EXPECTED_STATE_DIFF_PROPERTIES = []
EXPECTED_STATE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
    'transaction_index': Decimal('0'),
    'address': '0x3F98e477a361F777DA14611a7e419A75Fd238b6b',
    'balance_diff': Decimal('2871814909918360'),
    'nonce_diff': None,
    'code_from': None,
    'code_to': None,
    'state_diff_type': 'fees'}
)
EXPECTED_STATE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
    'transaction_index': Decimal('0'),
    'address': '0x9B2c46642CAF6B936dc0633da521f1E946B7e18F',
    'balance_diff': Decimal('-2871814909918360'),
    'nonce_diff': 1,
    'code_from': None,
    'code_to': None,
    'state_diff_type': 'sender'})
EXPECTED_STATE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
    'transaction_index': Decimal('0'),
    'address': '0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
    'balance_diff': None,
    'nonce_diff': None,
    'code_from': None,
    'code_to': None,
    'state_diff_type': None})
EXPECTED_STATE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': None,
    'transaction_index': None,
    'address': '0x3F98e477a361F777DA14611a7e419A75Fd238b6b',
    'balance_diff': Decimal('5156250000000000000'),
    'nonce_diff': None,
    'code_from': None,
    'code_to': None,
    'state_diff_type': 'miner'})
EXPECTED_STATE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': None,
    'transaction_index': None,
    'address': '0xbe4532E1B1Db5c913Cf553be76180c1777055403',
    'balance_diff': Decimal('3750000000000000000'),
    'nonce_diff': None,
    'code_from': None,
    'code_to': None,
    'state_diff_type': 'uncle'})

EXPECTED_STORAGE_DIFF_PROPERTIES = []
EXPECTED_STORAGE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
    'transaction_index': Decimal('0'),
    'state_diff_id': 3,
    'address': '0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
    'position': '0x176f28426fded76854a5a0a4c618c35554983e8a7e93abf0310b736ef509d29e',
    'storage_from': '0x0000000000000000000000000000000000000000000000000000000000000000',
    'storage_to': '0x00000000000000000000000000000000000000000000000000000000000003e8'})
EXPECTED_STORAGE_DIFF_PROPERTIES.append({
    'block_number': Decimal('56160'),
    'timestamp': datetime.datetime(2015, 8, 9, 1, 14, 50),
    'transaction_hash': '0x8696c8669e07ae7e4ceef43945fe9c78252ab76f1a3c16658a04a644b8329736',
    'transaction_index': Decimal('0'),
    'state_diff_id': 3,
    'address': '0xDBB576b5B0e7BF0570A981AAb3AD39A0c5F19EB1',
    'position': '0x8627c64ae2959fac7fcf3b7380ff296fe9a6472ae59b0a5fd22f1e5b88614aea',
    'storage_from': '0x0000000000000000000000000000000000000000000000000000000000002710',
    'storage_to': '0x0000000000000000000000000000000000000000000000000000000000002328'
    })

EXPECTED_BLOCK_HASHES = {
    56160: '0x685b2226cbf6e1f890211010aa192bf16f0a0cba9534264a033b023d7367b845',
    56161: '0xb51b0bce38d2742b9285aa2a6f632ee6691da41052c67a1d5ee34ae2edc814ea',
    56162: '0x4510dc791170b38d7a2c4f57627f0dd8c466c0f8a56dafab0e6f6588f182f4d2',
    56163: '0x4c5109f7c6277f2440eb06b72a95ce809cf137e01425f696fe4a3dd17c99fda5',
    56164: '0x356bb1f4e5219fc2a60ff0ca4e1d18e4c84a07866e9298fa3b7d855b086ae1c8',
    56165: '0xd9728379c91556439281ecdb5884565a8da3bdf97c06ef56b3445e5c47111b4e',
    56166: '0x5922c7db70870fee474289f79649218615ecd7582e21628af63b8c3fa1ccca5d',
    56167: '0x21e67edf92cd0d05b5c8a4a841419fd1e85ae4ffb481efe13d32964d98e82467',
    56168: '0x4096087da344b12939dfe9ce7158a9677e65f6cd526e1de89caabace60f12e1c',
    56169: '0x0d2c248710ee59c79e9aa2c02eff7de404a6e709d2feaee628d5ee74c1b69748',
    56170: '0x1d82d2ed544f5cab0bdff8c67443d1a25eaca5c241ce30b80347169b7e5c32a9',
    56171: '0x4db2e7b879582426583be908909526aadc3d0f4d4da2c1ea7a2f581a6cbe7c64',
    56172: '0xe4f85d305b1632c8d30e544e5d0654371c79fa0f43e1c1225b896d05d3745386',
    56173: '0x774d658a615a10d2cd5e4d3b950624a312a146234a6e794affefd62a9d9426d7',
    56174: '0x8941150dd196af9de8d104ddc9eeb44f0ab6937c776027592b5fd068dab639b4',
}
