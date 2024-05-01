$(document).ready(function() {
    $('#add-expert').click(function() {
        var form_idx = $('.expert-form').length;
        if(form_idx + 1 == 6) {$('#add-expert').hide();}
        var form_row = $()
        var form = $('#empty-expert-form').html().replace(/__prefix__/g, form_idx);
        $(
            '<div class="expert-form d-flex align-items-center gap-3"'
            + ' id="expert-form-' + form_idx + '">'
            + '<span>Эксперт ' + (form_idx + 2) + ':</span>' + form
            + '<button type="button" class="remove-expert btn btn-sm btn-danger">Удалить</button>'
            + '</div>'
        ).insertBefore('#add-expert');
        $('#id_incidentexpert_set-TOTAL_FORMS').val(form_idx + 1);
    });

    $(document).on("click", ".remove-expert", function() {
        parent = $(this).closest('.expert-form');
        parent_id = parseInt(parent.attr("id").split('-')[2]);
        parent.remove();

        var form_idx = $('.expert-form').length;
        for (var i = parent_id + 1; i <= form_idx; ++i) {
            cur_el = $('#expert-form-' + i);
            cur_el.attr('id', 'expert-form-' + (i - 1));
            cur_el.children('span').text(cur_el.children('span').text().replace(i + 2, i + 1));
            cur_el.children('select').attr('id', 'incidentexpert_set-' + (i - 1) + '-expert');
            cur_el.children('select').attr('name', 'incidentexpert_set-' + (i - 1) + '-expert');
        }

        $('#id_incidentexpert_set-TOTAL_FORMS').val(form_idx);
        if(form_idx < 6) {$('#add-expert').show();}
    });

    $('#add-basis').click(function() {
        var form_idx = $('.basis-form').length;
        var form = $('#empty-basis-form').html().replace(/__prefix__/g, form_idx);
        $('.basis-formset').append('<div class="basis-form">' + form + '</div>');
        $('#id_basis_set-TOTAL_FORMS').val(form_idx + 1);
    });

    $('.remove-basis').click(function() {
        $('.basis-form').last().remove();
        var forms = $('.basis-form').length;
        $('#id_basis_set-TOTAL_FORMS').val(forms);
    });

    $('#add-strategy').click(function() {
        var form_idx = $('.strategy-form').length;
        var form = $('#empty-strategy-form').html().replace(/__prefix__/g, form_idx);
        $('.strategy-formset').append('<div class="strategy-form">' + form + '</div>');
        $('#id_strategy_set-TOTAL_FORMS').val(form_idx + 1);
    });

    $('.remove-strategy').click(function() {
        $('.strategy-form').last().remove();
        var forms = $('.strategy-form').length;
        $('#id_strategy_set-TOTAL_FORMS').val(forms);
    });
});