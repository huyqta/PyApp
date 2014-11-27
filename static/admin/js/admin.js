/**
 * Created by HUYQTA on 10/21/14.
 */

$(document).ready(function () {

//    $('#form-category').addClass('active-tab');
    $('#form-category').removeClass('active-tab');
    $('#form-item').removeClass('active-tab');
    ////////////// CATEGORY SCRIPTS //////////////
    $('#list-category').click(function () {
        console.log('cat click');
        $('#form-category').addClass('active-tab');
        $('#form-item').removeClass('active-tab');
    })
    $('#list-item').click(function () {
        console.log('item click');
        $('#form-category').removeClass('active-tab');
        $('#form-item').addClass('active-tab');
    })
    $('#list-discount').click(function () {
        $('#form-discount').addClass('active-tab');
    })

    ////////////// CATEGORY SCRIPTS //////////////

    $('.cat-data-row').click(function () {
        $('#new-cat-id').val(this.children[0].innerHTML);
        $('#new-cat-name').val(this.children[1].innerHTML);
        $('#new-cat-des').val(this.children[2].innerHTML);
        $('#new-cat-act').val(this.children[3].innerHTML);
        $('#new-cat-par').val(this.children[4].innerHTML);
    })

    $('#create-cate, #update-cate, #delete-cate').click(function () {
        $.post('/admin/category', {
            new_cat_id: $('#new-cat-id').val(),
            new_cat_name: $('#new-cat-name').val(),
            new_cat_des: $('#new-cat-des').val(),
            new_cat_act: $('#new-cat-act').val(),
            new_cat_par: $('#new-cat-par').val(),
            new_cat_type: this.value
        }).done(function (response) {
            location.reload();
            $('#form-item').removeClass('active-tab');
            $('#form-category').addClass('active-tab');
        })
    })

    ////////////// TRADEMARK SCRIPTS //////////////

    $('.trm-data-row').click(function () {
        $('#new-trm-id').val(this.children[0].innerHTML);
        $('#new-trm-name').val(this.children[1].innerHTML);
        $('#new-trm-des').val(this.children[2].innerHTML);
        $('#new-trm-par').val(this.children[4].innerHTML);
        $('#new-trm-act').val(this.children[3].innerHTML);
        $('#new-trm-cat').val(this.children[5].innerHTML);
    })

    $('#create-trme, #update-trme, #delete-trme').click(function () {
        $.post('/admin/trademark', {
            new_trm_id: $('#new-trm-id').val(),
            new_trm_name: $('#new-trm-name').val(),
            new_trm_des: $('#new-trm-des').val(),
            new_trm_par: $('#new-trm-par').val(),
            new_trm_act: $('#new-trm-act').val(),
            new_trm_cat: $('#new-trm-cat').val(),
            new_trm_type: this.value
        }).done(function (response) {
            location.reload();
            $('#form-item').removeClass('active-tab');
            $('#form-trademark').addClass('active-tab');
        })
    })

    ////////////// PRODUCT SCRIPTS //////////////

    $('.prd-data-row').click(function () {
        var prd_id = this.children[0].innerHTML;
        $('#new-prd-id').val(prd_id);
        $('#new-prd-name').val(this.children[1].innerHTML);
//        var oEditor = CKEDITOR.instances[0];
//        oEditor.insertHtml( this.children[2].innerHTML );
        for(var i in CKEDITOR.instances){
            console.log(CKEDITOR.instances[i].name);
            if (CKEDITOR.instances[i].name == "new-prd-des"){
                CKEDITOR.instances[i].setData(this.children[2].innerHTML);
            }
            if (CKEDITOR.instances[i].name == "new-prd-tech"){
                CKEDITOR.instances[i].setData(this.children[3].innerHTML);
            }
        }
        $('#new-prd-img').attr('src', this.children[4].children[0].src);
        $('#new-prd-price').val(this.children[5].innerHTML);
        $('#new-prd-cat').val(this.children[6].title);
        $('#new-prd-dis').val(this.children[7].innerHTML);
        $('#new-prd-act').val(this.children[8].innerHTML);
        $('#new-prd-disprice').val(this.children[9].innerHTML);
        if (this.children[10].innerHTML.substring(0,1) == 1){
            $('#new-prd-option-1').attr('checked', true);
        }
        else{
            $('#new-prd-option-1').attr('checked', false);
        }
        if (this.children[10].innerHTML.substring(1,2) == 1){
            $('#new-prd-option-2').attr('checked', true);
        }
        else{
            $('#new-prd-option-2').attr('checked', false);
        }
        if (this.children[10].innerHTML.substring(2,3) == 1){
            $('#new-prd-option-3').attr('checked', true);
        }
        else{
            $('#new-prd-option-3').attr('checked', false);
        }
        $('#new-prd-option-1').val(this.children[10].innerHTML.substring(0,1));
        $('#new-prd-option-2').val(this.children[10].innerHTML.substring(1,2));
        $('#new-prd-option-3').val(this.children[10].innerHTML.substring(2,3));
        $('#product-image-select img').each(function(){
            if ($(this)[0].title == prd_id){
                $(this).show();
            }
            else{
                $(this).hide();
            }
        })
        $('#new-prd-trm').val(this.children[11].title);
    })

    $('#product-image-select img').click(function(){
        $('#new-prd-img').attr('src',$(this).attr('src'));
    })

    $('#create-prd, #update-prd, #delete-prd').click(function () {
        var desc = "";
        var tech = "";
        var option = "";
        for(var i in CKEDITOR.instances){
            if (CKEDITOR.instances[i].name == "new-prd-des"){
                desc = CKEDITOR.instances[i].getData();
            }
            if (CKEDITOR.instances[i].name == "new-prd-tech"){
                tech = CKEDITOR.instances[i].getData();
            }
//            var oEditor = CKEDITOR.instances[i];
//            desc = CKEDITOR.instances[i].getData();
        }
        var option1 = $('#new-prd-option-1')[0].checked ? 1 : 0;
        var option2 = $('#new-prd-option-2')[0].checked ? 1 : 0;
        var option3 = $('#new-prd-option-3')[0].checked ? 1 : 0;
        option = option1 + '' + option2 + '' + option3;
        $.post('/admin/product', {
            new_prd_id: $('#new-prd-id').val(),
            new_prd_name: $('#new-prd-name').val(),
            new_prd_des: desc,
            new_prd_tech: tech,
            new_prd_price: $('#new-prd-price').val(),
            new_prd_img: $('#new-prd-img').attr('src'),
            new_prd_cate: $('#new-prd-cat').val(),
            new_prd_dis: $('#new-prd-dis').val(),
            new_prd_act: $('#new-prd-act').val(),
            new_prd_disprice: $('#new-prd-disprice').val(),
            new_prd_option: option,
            new_prd_trm: $('#new-prd-trm').val(),
            new_prd_type: this.value
        }).done(function (response) {
            location.reload();
            $('#form-category').removeClass('active-tab');
            $('#form-item').addClass('active-tab');
        })
    })

    $('#list-product ul li').each(function () {
        var href = $(this).find('a').attr('href');
        if (href === window.location.pathname) {
            $(this).addClass('selected-product');
            $('#refproduct').val($(this).val());
        }

    })

})