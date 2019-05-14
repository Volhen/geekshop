window.onload = function () {
    $("a.bt-01, #product > div > div > a.btn.btn-primary").on("click", function (event) {
        var target = event.target;
        $.ajax({
            url: "/basket/add/" + target.name + "/",
            success: function (data) {

                var basket_total_quantity = (data.basket_total_quantity).toString();
                var basket_total_cost = ('&euro; ' + parseInt(data.basket_total_cost)).toString();
                
                $('#list-menu > li:nth-child(3) > span > span').html(data.basket_total_quantity);
                $('#list-menu > li:nth-child(3) > a > span > span').html(basket_total_cost);
            }
        });
        event.preventDefault();
    });
};
