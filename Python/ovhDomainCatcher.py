import ovh
import ovh.exceptions
import json
import time


# This scirpt tries to snipe domain when it is released to the pool
# You have to set up default payment method and billing address
# Uses OVH Api - https://github.com/ovh/python-ovh


## DOMAIN TO REGISTER
domain = '<domain>'
time_between_API_calls = 2 # in seconds

try:
    client = ovh.Client()


    # creating a new cart and assign to current user
    cart = client.post("/order/cart", ovhSubsidiary="PL", _need_auth=False)
    client.post("/order/cart/{0}/assign".format(cart.get("cartId")))

    # add domain item to the cart
    big_loop = True
    while big_loop:
        infos = client.get("/order/cart/{0}/domain"
                            .format(cart.get("cartId")), domain=domain)

        #print(json.dumps(infos, indent=4))
        if(infos[0]['action'] == 'transfer'):
            print('domain not purchasable (transfer)')
            time.sleep(time_between_API_calls)
            continue
        if(infos[0]['action'] == 'create'):
            print('domain available')

        index = 0
        offer = infos[index]
        if not offer["orderable"]:
            print("This domain is not available")
            continue

        total_price = None
        for price in offer["prices"]:
            if price["label"] == "TOTAL":
                total_price = price["price"]["text"]
                break
        print(u"Offer selected: {0} (phase : {1}) => {2}"
              .format(domain, infos[index]["phase"], total_price))

        # adding domain to cart
        try:
            domain_2_cart = client.post("/order/cart/{0}/domain"
                        .format(cart.get("cartId")),
                        domain=domain,
                        offerId=offer["offerId"])
            big_loop = False
        except ovh.exceptions.APIError as e:
            print(e)


    # generate a salesorder
    # switch GET to POST to make a REAL CART
    try:
        salesorder = client.post("/order/cart/{0}/checkout"
                                 .format(cart.get("cartId")))
        print(u"Order #{0} ({1}) has been generated : {2}"
              .format(salesorder["orderId"],
                      salesorder["prices"]["withTax"]["text"],
                      salesorder.get("url")))
        #print(json.dumps(salesorder, indent=4))
    except ovh.exceptions.APIError as e:
        print("Unable to generate the order: " + str(e))
        exit(1)

    

    # retrieve available payment means
    print("Preparing for payment")
    order_payment_means = ['CREDIT_CARD']
    
    try:
        print("payment is happening rn")
        client.post("/me/order/{0}/payWithRegisteredPaymentMean".format(salesorder.get("orderId")), paymentMean=prepaid_payment_means[0])
    except ovh.exceptions.APIError as e:
        print("Payment of your order haven't been succesful: " + str(e))
        exit(1)

except ovh.exceptions.APIError as e:
    print(e)