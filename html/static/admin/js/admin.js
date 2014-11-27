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

    ////////////// PRODUCT SCRIPTS //////////////

    $('.prd-data-row').click(function () {
        $('#new-prd-id').val(this.children[0].innerHTML);
        $('#new-prd-name').val(this.children[1].innerHTML);
        $('#new-prd-des').val(this.children[2].innerHTML);
        // console.log(this.children[3].children[0].src);
        $('#new-prd-img').attr('src', this.children[3].children[0].src);
        $('#new-prd-price').val(this.children[4].innerHTML);
        $('#new-prd-cat').val(this.children[5].innerHTML);
        $('#new-prd-dis').val(this.children[6].innerHTML);
        $('#new-prd-act').val(this.children[7].innerHTML);
        $('#new-prd-disprice').val(this.children[8].innerHTML);
    })

    $('#create-prd, #update-prd, #delete-prd').click(function () {
        $.post('/admin/product', {
            new_prd_id: $('#new-prd-id').val(),
            new_prd_name: $('#new-prd-name').val(),
            new_prd_des: $('#new-prd-des').val(),
            new_prd_img: $('#new-prd-img').attr('src'),
            new_prd_price: $('#new-prd-price').val(),
            new_prd_cate: $('#new-prd-cat').val(),
            new_prd_dis: $('#new-prd-dis').val(),
            new_prd_act: $('#new-prd-act').val(),
            new_prd_disprice: $('#new-prd-disprice').val(),
            new_prd_type: this.value
        }).done(function (response) {
            location.reload();
            $('#form-category').removeClass('active-tab');
            $('#form-item').addClass('active-tab');
        })
    })

})