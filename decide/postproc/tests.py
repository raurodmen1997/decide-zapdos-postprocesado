from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from postproc import views

class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.views = views.PostProcView()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    ## Tests realizados modificando la variable (temporal) 'numSeats' con los valores: 2,3,5,12,21

    # Testeo de un caso sencillo con las opciones no ordenadas segun votos
    def test_hare_01(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 245034 },
                { 'option': 'Option 2', 'number': 2, 'votes': 98562 },
                { 'option': 'Option 3', 'number': 3, 'votes': 391000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200001 },
                { 'option': 'Option 5', 'number': 5, 'votes': 312000 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 245034, 'seats': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes': 98562, 'seats': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 391000, 'seats': 7 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'seats': 3 },
            { 'option': 'Option 5', 'number': 5, 'votes': 312000, 'seats': 5 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Caso en el que existe gran disparidad en los votos de las opciones
    def test_hare_02(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Option 2', 'number': 2, 'votes': 300 },
                { 'option': 'Option 3', 'number': 3, 'votes': 245034 },
                { 'option': 'Option 4', 'number': 4, 'votes': 200001 },
                { 'option': 'Option 5', 'number': 5, 'votes': 14 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'seats': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 300, 'seats': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 245034, 'seats': 11 },
            { 'option': 'Option 4', 'number': 4, 'votes': 200001, 'seats': 9 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'seats': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 1 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    # Testeo del comportamiento del código con una opción con 0 votos
    def test_hare_03(self):
        data = {
            'type': 'HARE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 2510 },
                { 'option': 'Option 2', 'number': 2, 'votes': 6540 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 12046 },
                { 'option': 'Option 5', 'number': 5, 'votes': 14 },
                { 'option': 'Option 6', 'number': 6, 'votes': 20145 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 2510, 'seats': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 6540, 'seats': 4 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'seats': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 12046, 'seats': 6 },
            { 'option': 'Option 5', 'number': 5, 'votes': 14, 'seats': 0 },
            { 'option': 'Option 6', 'number': 6, 'votes': 20145, 'seats': 10 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_huntington_hill1(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','votes': 100000},
                {'option':'PSOE', 'votes': 80000},
                {'option':'Podemos', 'votes': 30000},
                {'option':'Cs', 'votes': 20000}
            ],
            'escaños': 8
        }

        expected_result = [
            {'option':'PP','numEscaños': 4},
            {'option':'PSOE','numEscaños': 3},
            {'option':'Podemos','numEscaños': 1},
            {'option':'Cs','numEscaños': 0}
        ]

        result = self.views.metodoHuntington_Hill(data)

        print('Ejemplo 1')
        print(data)
        print(result)
        self.assertEqual(result, expected_result)

    def test_huntington_hill2(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','votes': 126837},
                {'option':'PSOE', 'votes': 71804},
                {'option':'Podemos', 'votes': 25880},
            ],
            'escaños': 4
        }

        expected_result = [
            {'option':'PP','numEscaños': 3},
            {'option':'PSOE','numEscaños': 1},
            {'option':'Podemos','numEscaños': 0},
        ]

        result = self.views.metodoHuntington_Hill(data)

        print('Ejemplo 2')
        print(data)
        print(result)
        self.assertEqual(result, expected_result)

    def test_huntington_hill3(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'Marta','votes': 380},
                {'option':'Jose', 'votes': 240},
                {'option':'Pedro', 'votes': 105},
                {'option':'Ana', 'votes': 55}
            ],
            'escaños': 22
        }

        expected_result = [
            {'option':'Marta','numEscaños': 10},
            {'option':'Jose','numEscaños': 7},
            {'option':'Pedro','numEscaños': 3},
            {'option':'Ana','numEscaños': 2}
        ]

        result = self.views.metodoHuntington_Hill(data)

        print('Ejemplo 3')
        print(data)
        print(result)
        self.assertEqual(result, expected_result)

    def test_huntington_hill4(self):
        data = {
            'type': 'HUNTINGTON_HILL',
            'options': [
                {'option':'PP','votes': 162310},
                {'option':'PSOE', 'votes': 538479},
                {'option':'Podemos', 'votes': 197145},
            ],
            'escaños': 41
        }

        expected_result = [
            {'option':'PP','numEscaños': 7},
            {'option':'PSOE','numEscaños': 25},
            {'option':'Podemos','numEscaños': 9},
        ]

        result = self.views.metodoHuntington_Hill(data)

        print('Ejemplo 4')
        print(data)
        print(result)
        self.assertEqual(result, expected_result)

    def test_imperiali_1(self):
        data = {
            'type': 'COCIENTE_IMPERIALI1',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 9},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 7},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 4},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 1},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]


    #Test recuento BORDA. Realizado por Raúl. VARIOS VOTANTES, EN ESTE CASO, 4 VOTANTES
    def test_borda(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1,1,3,2]},
                {'option': 'Psoe', 'positions': [2,3,4,3]},
                {'option': 'Podemos', 'positions': [3,4,1,4]},
                {'option': 'Ciudadanos', 'positions': [4,2,2,1]},
            ]
        }

        expected_result = {
            'Popular': 13,
            'Psoe': 8,
            'Podemos': 8,
            'Ciudadanos': 11
            }
        

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_2(self):
        #Test 2: Más partidos que escaños a repartir
        data = {
            'type': 'COCIENTE_IMPERIALI2',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 3},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 2},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 1},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_3(self):
        #Test 3: Repartir 0 escaños entre todos los partidos
        data = {
            'type': 'COCIENTE_IMPERIALI3',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanyos': 0},
        ]


    #Test recuento BORDA. Realizado por Raúl. SOLO UN VOTANTE
    def test_borda2(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1]},
                {'option': 'Psoe', 'positions': [2]},
                {'option': 'Podemos', 'positions': [3]},
                {'option': 'Ciudadanos', 'positions': [4]},
            ]
        }

        expected_result = {
            'Popular': 4,
            'Psoe': 3,
            'Podemos': 2,
            'Ciudadanos': 1
            }
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_imperiali_4(self):
        #Test 4: Repartir escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI4',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_4(self):
        #Test 4: Repartir escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI4',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]


    #Test recuento BORDA. Realizado por Raúl. SI NADIE HA VOTADO A NINGÚN REPRESENTANTE
    def test_borda3(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': []},
                {'option': 'Psoe', 'positions': []},
                {'option': 'Podemos', 'positions': []},
                {'option': 'Ciudadanos', 'positions': []},
            ]
        }

        expected_result = {}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_imperiali_5(self):
        #Test 5: Repartir 0 escaños para partidos con 0 votos
        data = {
            'type': 'COCIENTE_IMPERIALI5',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanyos': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanyos': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanyos': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanyos': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanyos': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_imperiali_6(self):
        #Test 6: Partidos con el mismo numero de votos y con 20 escaños a repartir
        data = {
            'type': 'COCIENTE_IMPERIALI6',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 10 },
                { 'option': 'B', 'number': 2, 'votes': 20 },
                { 'option': 'C', 'number': 3, 'votes': 60 },
                { 'option': 'D', 'number': 4, 'votes': 20 },
                { 'option': 'E', 'number': 5, 'votes': 1 },
                { 'option': 'F', 'number': 6, 'votes': 20 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'C', 'number': 3, 'votes': 60, 'escanyos': 10},
            { 'option': 'B', 'number': 2, 'votes': 20, 'escanyos': 3},
            { 'option': 'D', 'number': 4, 'votes': 20, 'escanyos': 3},
            { 'option': 'F', 'number': 6, 'votes': 20, 'escanyos': 3},
            { 'option': 'A', 'number': 1, 'votes': 10, 'escanyos': 1},
            { 'option': 'E', 'number': 5, 'votes': 1, 'escanyos': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanyos': 0},
        ]


    #Test recuento BORDA. Realizado por Raúl. TODOS LOS VOTANTES NO HAN VOTADO A UN REPRESENTANTE,
    #EN ESTE CASO, AL REPRESENTANTE 'Podemos'
    def test_borda4(self):
        data = {
            'type': 'BORDA',
            'options': [
                {'option': 'Popular', 'positions': [1,3,3,4]},
                {'option': 'Psoe', 'positions': [2,2,1,1]},
                {'option': 'Podemos', 'positions': []},
                {'option': 'Ciudadanos', 'positions': [3,4,2,2]},
            ]
        }

        expected_result = {}
        


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        self.assertEqual(values, expected_result)



        self.assertEqual(values, expected_result)

