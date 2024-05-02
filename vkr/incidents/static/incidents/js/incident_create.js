$(document).ready(function() {
    if ($('.expert-form').length == 6) {
        $('#add-expert').hide();
    }
    if ($('.basis-form').length == 7) {
        $('#add-basis').hide();
    }
    if ($('.strategy-form').length == 5) {
        $('#add-strategy').hide();
    }

    $('#add-expert').click(function() {
        var form_idx = $('.expert-form').length;
        if(form_idx + 1 == 6) {$('#add-expert').hide();}
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
            cur_el.children('select').attr('id', 'id_incidentexpert_set-' + (i - 1) + '-expert');
            cur_el.children('select').attr('name', 'incidentexpert_set-' + (i - 1) + '-expert');
        }

        $('#id_incidentexpert_set-TOTAL_FORMS').val(form_idx);
        if(form_idx < 6) {$('#add-expert').show();}
    });

    $('#add-basis').click(function() {
        var form_idx = $('.basis-form').length;
        if(form_idx + 1 == 7) {$('#add-basis').hide();}
        var form = $('#empty-basis-form').html().replace(/__prefix__/g, form_idx);
        $(
            '<div class="basis-form d-flex flex-column gap-3"'
            + ' id="basis-form-' + form_idx + '">'
            + '<div class="d-flex gap-2 align-items-center justify-content-center">'
            + '<h5 class="text-center m-0">Базис ' + (form_idx + 1) + '</h5>'
            + '<button type="button" class="remove-basis btn btn-sm btn-danger">Удалить</button>'
            + '</div>' + form + '</div>'
        ).insertBefore('#add-basis');
        $('#id_basis_set-TOTAL_FORMS').val(form_idx + 1);
    });

    $(document).on("click", ".remove-basis", function() {
        parent = $(this).closest('.basis-form');
        parent_id = parseInt(parent.attr("id").split('-')[2]);
        parent.remove();

        var form_idx = $('.basis-form').length;
        for (var i = parent_id + 1; i <= form_idx; ++i) {
            cur_el = $('#basis-form-' + i);
            cur_el.attr('id', 'basis-form-' + (i - 1));
            cur_el.find('h5').text(cur_el.find('h5').text().replace(i + 1, i));
            cur_el.find('input').attr('id', 'id_basis_set-' + (i - 1) + '-name');
            cur_el.find('input').attr('name', 'basis_set-' + (i - 1) + '-name');
            cur_el.find('textarea').attr('id', 'id_basis_set-' + (i - 1) + '-description');
            cur_el.find('textarea').attr('name', 'basis_set-' + (i - 1) + '-description');
            cur_el.find('label').each(function() {
                $(this).attr('for', $(this).attr('for').replace(i, i - 1));
            });
        }

        $('#id_basis_set-TOTAL_FORMS').val(form_idx);
        if(form_idx < 7) {$('#add-basis').show();}
    });

    $('#add-strategy').click(function() {
        var form_idx = $('.strategy-form').length;
        if(form_idx + 1 == 5) {$('#add-strategy').hide();}
        var form = $('#empty-strategy-form').html().replace(/__prefix__/g, form_idx);
        $(
            '<div class="strategy-form d-flex flex-column gap-3"'
            + ' id="strategy-form-' + form_idx + '">'
            + '<div class="d-flex gap-2 align-items-center justify-content-center">'
            + '<h5 class="text-center m-0">Стратегия ' + (form_idx + 1) + '</h5>'
            + '<button type="button" class="remove-strategy btn btn-sm btn-danger">Удалить</button>'
            + '</div>' + form + '</div>'
        ).insertBefore('#add-strategy');
        $('#id_strategy_set-TOTAL_FORMS').val(form_idx + 1);
    });

    $(document).on("click", ".remove-strategy", function() {
        parent = $(this).closest('.strategy-form');
        parent_id = parseInt(parent.attr("id").split('-')[2]);
        parent.remove();

        var form_idx = $('.strategy-form').length;
        for (var i = parent_id + 1; i <= form_idx; ++i) {
            cur_el = $('#strategy-form-' + i);
            cur_el.attr('id', 'strategy-form-' + (i - 1));
            cur_el.find('h5').text(cur_el.find('h5').text().replace(i + 1, i));
            cur_el.find('input').attr('id', 'id_strategy_set-' + (i - 1) + '-name');
            cur_el.find('input').attr('name', 'strategy_set-' + (i - 1) + '-name');
            cur_el.find('textarea').attr('id', 'id_strategy_set-' + (i - 1) + '-description');
            cur_el.find('textarea').attr('name', 'strategy_set-' + (i - 1) + '-description');
            cur_el.find('label').each(function() {
                $(this).attr('for', $(this).attr('for').replace(i, i - 1));
            });
        }

        $('#id_strategy_set-TOTAL_FORMS').val(form_idx);
        if(form_idx < 5) {$('#add-strategy').show();}
    });
});