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

    var production_select = $('select').first();
    select_items_height = (production_select.children().length * production_select.children().height()) + 20;
    $(production_select).height(select_items_height);

});