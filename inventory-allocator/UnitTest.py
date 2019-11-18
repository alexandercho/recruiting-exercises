from src.InventoryAllocator import *
import unittest

class TestInventoryAllocator(unittest.TestCase):

    #Very basic testing given in the readme
    def testGivenExamples(self):
        example_inputs = [({ 'apple': 1 }, [{ 'name': 'owd', 'inventory': { 'apple': 1 } }]),
                          ({ 'apple': 1 }, [{ 'name': 'owd', 'inventory': { 'apple': 0 } }]),
                          ({ 'apple': 10 }, [{ 'name': 'owd', 'inventory': { 'apple': 5 } },
                                             { 'name': 'dm', 'inventory': { 'apple': 5 }}
                                            ]
                          )
                         ]
        example_outputs = [[{ 'owd': { 'apple': 1 } }],
                           [],
                           [{ 'dm': { 'apple': 5 }}, { 'owd': { 'apple': 5 } }]
                          ]

        for i in range(len(example_inputs)):
            self.assertEqual(InventoryAllocator(example_inputs[i][0], example_inputs[i][1]).get_cheapest_shipment(), example_outputs[i])

    #Test contain warehouses in the middle of the list that can be redistributed
    #to order from less warehouses. Also tests for cases where the most expensive
    #warehouse contains all the items (Assumption: each warehouse costs more than
    #all the previous ones combined)
    def testOptimalShipment(self):
        example_inputs = [({ 'apple': 1, 'orange':2, 'berry': 4},
                           [{ 'name': 'owd', 'inventory': { 'apple': 1 } },
                            { 'name': 'dm', 'inventory': { 'orange':2 }},
                            { 'name': 'amz', 'inventory': { 'orange':2, 'berry': 4 }}]),
                          ({'apple': 1, 'orange':1},
                           [{ 'name': 'amz', 'inventory': { 'apple': 1 } },
                            { 'name': 'dm', 'inventory': { 'orange': 1 } },
                            { 'name': 'owd', 'inventory': {'apple': 1, 'orange':1} }
                           ])
                          ]
        example_outputs = [
                           [{ 'amz': { 'orange':2, 'berry': 4 }},
                            { 'owd': { 'apple': 1 } }],
                           [{ 'dm': { 'orange': 1 } },
                            { 'amz' : { 'apple': 1 } }]
                          ]

        for i in range(len(example_inputs)):
            self.assertEqual(InventoryAllocator(example_inputs[i][0],
                                                example_inputs[i][1]).get_cheapest_shipment(),
                             example_outputs[i])

    #Test contain empty warehouses and orders. Should return empty lists
    def testEmptyShipment(self):
        example_inputs = [({},[]),
                          ({ 'apple': 1, 'orange':2, 'berry': 4},[]),
                          ({},[{ 'name': 'owd', 'inventory': { 'apple': 1 } },
                                { 'name': 'dm', 'inventory': { 'orange':2 }},
                                { 'name': 'amz', 'inventory': { 'orange':2, 'berry': 4 }}]),
                          ]
        example_outputs = [[],
                           [],
                           []]

        for i in range(len(example_inputs)):
            self.assertEqual(InventoryAllocator(example_inputs[i][0],
                                                example_inputs[i][1]).get_cheapest_shipment(),
                             example_outputs[i])

    #Test contain repeat warehouse and orders. Should return empty lists
    def testRepeatWarehouses(self):
        example_inputs = [({'apple': 1, 'orange':1},
                           [{ 'name': 'dm', 'inventory': { 'apple': 1 } },
                            { 'name': 'dm', 'inventory': { 'orange': 1 } },
                            { 'name': 'dm', 'inventory': {'apple': 1, 'orange':1} }
                            ])
                         ]
        example_outputs = [[]
                           ]

        for i in range(len(example_inputs)):
            self.assertEqual(InventoryAllocator(example_inputs[i][0],
                                                example_inputs[i][1]).get_cheapest_shipment(),
                             example_outputs[i])

if __name__ == '__main__':
    unittest.main()
