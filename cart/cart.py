from products.models import Product


class Cart:

    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add the specified product to the cart if it exists
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        """
        This will give us the power to iterate on the objects of class cart
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            yield item

    def __len__(self):
        """
        will return the number of products(product_ids) in the cart
        """
        return len(self.cart.keys())

    def clear(self):
        """
        Will delete the cart from session and clear it after payment
        """
        del self.session['cart']
        self.save()

    def get_total_price(self):
        """
        will show total price that you are going to pay
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        price_list = []

        for product in products:
            for item in self.cart.values():
                price_list.append(item['quantity']*float(product.price))

        return sum(price_list)
