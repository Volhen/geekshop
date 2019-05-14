var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
var quantity_arr = [];
var price_arr = [];
var $orderForm, $orderTotalQuantity, $orderTotalCost;
var totalForms, order_total_quantity, order_total_cost;


function orderSummaryUpdate(orderitem_price, delta_quantity) {
    delta_cost = orderitem_price * delta_quantity;

    order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
    order_total_quantity = order_total_quantity + delta_quantity;

    $('.order_total_cost').html(order_total_cost.toString().replace('.', ','));
    $('.order_total_quantity').html(order_total_quantity.toString());
}

function orderSummaryRecalc() {
    order_total_quantity = 0;
    order_total_cost = 0;

    for (var i = 0; i < totalForms; i++) {
        order_total_quantity += quantity_arr[i];
        order_total_cost += quantity_arr[i] * price_arr[i];
    }
    $('.order_total_quantity').html(order_total_quantity.toString());
    $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
}

function deleteOrderItem(row) {
    target_name = row[0].querySelector('input[type="number"]').name;
    orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
    delta_quantity = -quantity_arr[orderitem_num];

    quantity_arr[orderitem_num] = 0;
    if (!isNaN(price_arr[orderitem_num]) && !isNaN(delta_quantity)) {
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }
}


window.onload = function () {
    $orderForm = $('.order_form');
    $orderTotalQuantity = $('.order_total_quantity');
    $orderTotalCost = $('.order_total_cost');
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    order_total_quantity = parseInt($orderTotalQuantity.text()) || 0;
    order_total_cost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;

    for (i = 0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        price_arr[i] = _price || 0;
    }

    if (!order_total_quantity) {
        orderSummaryRecalc();
    }

    console.log(order_total_cost);
    // console.log(price_arr)

    $orderForm.on('change', 'input[type="number"]', function (event) {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });

    $orderForm.on('click', 'input[type="checkbox"]', function (event) {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    $('.order_form select').change(function (event) {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        var orderitem_product_pk = target.options[target.selectedIndex].value;

        if (orderitem_product_pk) {
            $.ajax({
                url: "/order/product/" + orderitem_product_pk + "/price/",
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        var price_html = '<span>' + data.price.toString().replace('.', ',') + '</span> &euro;';
                        var current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');

                        current_tr.find('td:eq(2)').html(price_html);

                        if (isNaN(current_tr.find('input[type="number"]').val())) {
                            current_tr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                }
            });
        }
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });
};