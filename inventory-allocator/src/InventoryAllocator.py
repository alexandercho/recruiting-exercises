class InventoryAllocator(object):

    def __init__(self, order={}, warehouses=[]):
        self._cheapest_shipment = []
        self._warehouses = warehouses
        if order and warehouses:
            self._cheapest_shipment =  self.cheapest_shipment(order)

    def get_cheapest_shipment(self):
        return self._cheapest_shipment

    #Destructive method finds the cheapest shipment for an order
    #and returns an empty list if such an order cannot be made
    def cheapest_shipment(self, order):
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

            for item in [key for key  in first_order if first_order[key] == 0]:
                del first_order[item]

        if first_order:
            return orig_orders

        return other_orders
