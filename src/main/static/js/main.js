$( document ).ready(function() {
    $('form button[value="reset"]').click(function(e) {
       $('div.alert').hide('slow', function(e) {
           $(this).remove();
       });
    });

    // Can be done in html, but then we would have to add each element ourself with certain classes
    $('.formset .form-group').has('[type="checkbox"]').css(
        {
            'display': 'inline-block',
            'margin-bottom': '0',
            'width': '45%'
        }
    );
    
    var product = $("#id_form-0-products");
    var product_selections = $("#id_form-0-products option");
    for (var i = 0; i < product_selections.length; i++) {
        var selection = $(product_selections[i]);
        product_name = $(selection).html().toLowerCase();
        console.log(product_name.search('xs4all'));
        if (product_name.search('xs4all') != -1) {
            $(selection).attr('data-imagesrc', 'http://www.furorteutonicus.eu/wp-content/uploads/2013/06/XS4ALL_avatar.jpg');
        }
        if (product_name.search('kpn') != -1) {
            $(selection).attr('data-imagesrc', 'http://www.gsmstunts.nl/images/provider/kpn-info-icon.jpg');
        }
        if (product_name.search('telfort') != -1) {
            $(selection).attr('data-imagesrc', 'https://pbs.twimg.com/profile_images/789889749/icon_normal.png');
        }
        if (product_name.search('reggefiber') != -1) {
            $(selection).attr('data-imagesrc', 'http://www.klachtenkompas.nl/sites/default/files/styles/icon_large_logo/public/reggefiber.png');
        }
    }
    
    product.ddslick({
        width: "100%",
        onSelected: function(selectedData){
            //callback function: do something with selectedData;
        }   
    });

    // var production_select = $('select').first();
    // select_items_height = (production_select.children().length * production_select.children().height()) + 20;
    // console.log(select_items_height);
    // if (select_items_height > 150) {
    //     select_items_height = 150;
    // }
    // $(production_select).height(select_items_height);

});