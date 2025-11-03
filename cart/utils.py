
def _cart(request):
    """This function gets the creates a unique session ID for guest user's cart"""

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart