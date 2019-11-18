class InventoryAllocator(object):

    def __init__(self, order={}, warehouses=[]):
        """
        Constructor for the allocator. If order or warehouses is empty,
        not given, or warehouse has repeat names, self.cheapest_shipment will
        be an empty list.

        Parameters:

        order (dic): A dictionary of orders with item names as keys and
        non-negative integers as the values. Example format:
            { 'apple': 1, 'orange':2, 'berry': 4}

        warehouses (list): A list of dictionaries with warehouse names as keys
        and dictionaries with the same format as order values. Example format:
            [{ 'name': 'owd', 'inventory': { 'apple': 1 } },
             { 'name': 'dm', 'inventory': { 'orange':2 }}]
        """
        self._cheapest_shipment = []
        self._warehouses = warehouses
        wh_names = list(map(lambda x: x['name'], warehouses))
        if order and warehouses and len(wh_names) == len(set(wh_names)):
            self._cheapest_shipment =  self.cheapest_shipment(order)

    def get_cheapest_shipment(self):
        """
        Getter function for the cheapest shipment order list.
        The list is sorted from most to least expensive.

        Returns:
        list: List of dictionaries where the only key is the name of the
            warehouse and the values are dictionaries of item names paired with
            the number ordered. Example format:
                [{ 'amz': { 'orange':2, 'berry': 4 }},
                 { 'owd': { 'apple': 1 } }]
        """
        return self._cheapest_shipment

    def cheapest_shipment(self, order):
        """
        Calculates the cheapest shipment for an order in the form of a list
        ordered by most expensive warehouse to least expensive. Method works
        destructively on the parameter order

        Parameters:

        order (dic): A dictionary of orders with item names as keys and
            non-negative integers as the values. Example format:
                 { 'apple': 1, 'orange':2, 'berry': 4}

        Returns:
        list: List of dictionaries where the only key is the name of the
            warehouse and the values are dictionaries of item names paired with
            the number ordered. The list is sorted from most to least expensive.
            Example format:
                 [{ 'amz': { 'orange':2, 'berry': 4 }},
                  { 'owd': { 'apple': 1 } }]
        """
        output = []
        for wh in self._warehouses:
            wh_order = {wh['name']:{}}
            wh_inv = wh['inventory']

            for item in order:
                if item in wh_inv:
                    ord_amt = min(wh_inv[item], order[item])
                    wh_order[wh['name']][item] = ord_amt
                    order[item] -= ord_amt

            if wh_order[wh['name']]:
                output += [wh_order]
                for item in [key for key in order if order[key] == 0]:
                    del order[item]
                if not order:
                    break

        if order:
            return []

        l = len(output)
        for i in range(2, l+1):
            output[l-i:] = self.redistribute(output[l-i:])

        return output[::-1]

    def redistribute(self, orders):
        """
        Attempts to redistribute all of the items in the order from the first warehouse
        to orders from all the others. If all the items cannot be redistributed,
        this returns the original list of orders.

        Parameters:

        order (list): A list of dictionaries where the only key is the name of
            the warehouse and the values are dictionaries of item names paired
            with the number ordered. Example format:
                [{ 'amz': { 'orange':2, 'berry': 4 }},
                 { 'owd': { 'apple': 1 } }]

        Returns:
        list: List of dictionaries where the only key is the name of the
            warehouse and the values are dictionaries of item names paired with
            the number ordered. Example format:
                [{ 'apple': 1, 'amz': { 'orange':2, 'berry': 4 }}]
        """
        orig_orders = orders.copy()
        first_order  = orders[0][list(orders[0])[0]]
        other_orders =  orders[1:]

        for wh in other_orders:
            wh_name = list(wh)[0]
            orig_wh = next(wh['inventory'] for wh in self._warehouses if wh['name'] == wh_name)

            for item in first_order:
                if item in orig_wh:
                    ord_amt = 0
                    req_amt = first_order[item]
                    if item in wh[wh_name]:
                        ord_amt = min(orig_wh[item] - wh[wh_name][item], req_amt)
                        wh[wh_name][item] += ord_amt
                    else:
                        ord_amt = min(orig_wh[item], req_amt)
                        wh[wh_name][item] = ord_amt
                    first_order[item] -= ord_amt

            for item in [key for key in first_order if first_order[key] == 0]:
                del first_order[item]

        if first_order:
            return orig_orders

        return other_orders
