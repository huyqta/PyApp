$(window).load(function () {

    var product_count = $('#product_count').text();
    console.log(product_count);
    initpaginator(product_count, $('.item-per-page').val());
    function initpaginator(product_count, perpage) {
        $("#paging").paging(product_count, {
            format: "[ < nncnn > ]  ",
            perpage: perpage,
            lapping: 0,
            page: 1,
            onSelect: function (page) {
                for (i = 0; i < $('.product-items > ul').find('li').length; i++) {
                    var item = $('.product-items > ul').find('li')[i];
                    if (i >= this.slice[0] && i < (this.slice[1])) {
                        $(item).removeClass('hide-product');
                    }
                    else {
                        $(item).addClass('hide-product');
                    }
                }
            },
            onFormat: function (type) {

                switch (type) {

                    case 'block':

                        if (!this.active)
                            return '<span class="disabled">' + this.value + '</span>';
                        else if (this.value != this.page)
                            return '<a href="#' + this.value + '"><span>' + this.value + '</span></a>';
                        return '<span class="current">' + this.value + '</span>';

                    case 'next':

                        if (this.active)
                            return '<a href="#' + this.value + '" class="next"><span><i class="fa fa-forward"></i></span></a>';
                        return '<span class="disabled"><i class="fa fa-forward"></i></span>';

                    case 'prev':

                        if (this.active)
                            return '<a href="#' + this.value + '" class="prev"><span><i class="fa fa-backward"></i></span></a>';
                        return '<span class="disabled"><i class="fa fa-backward"></i></span>';

                    case 'first':

                        if (this.active)
                            return '<a href="#' + this.value + '" class="first"><span><i class="fa fa-fast-backward"></i></span></a>';
                        return '<span class="disabled"><i class="fa fa-fast-backward"></i></span>';

                    case 'last':

                        if (this.active)
                            return '<a href="#' + this.value + '" class="last"><span><i class="fa fa-fast-forward"></i></span></a>';
                        return '<span class="disabled"><i class="fa fa-fast-forward"></i></span>';

                    case "leap":

                        if (this.active)
                            return "   ";
                        return "";

                    case 'fill':

                        if (this.active)
                            return "...";
                        return "";
                }
            }
        });
    }

    $('.item-per-page').change(function () {
        initpaginator(product_count, $('.item-per-page').val());
    })
    $('.marquee').marquee({
        //speed in milliseconds of the marquee
        duration: 15000,
        //gap in pixels between the tickers
        gap: 50,
        //time in milliseconds before the marquee will start animating
        delayBeforeStart: 0,
        //'left' or 'right'
        direction: 'left',
        //true or false - should the marquee be duplicated to show an effect of continues flow
        duplicated: true
    });

    $('#slideshowHolder').jqFancyTransitions({
        effect: 'wave', // wave, zipper, curtain
        width: 1440, // width of panel
        height: 500, // height of panel
        strips: 15, // number of strips
        delay: 3000, // delay between images in ms
        stripDelay: 20, // delay beetwen strips in ms
        titleOpacity: 0.8, // opacity of title
        titleSpeed: 2000, // speed of title appereance in ms
        position: 'curtain', // top, bottom, alternate, curtain
        direction: 'fountainAlternate', // left, right, alternate, random, fountain, fountainAlternate
        navigation: true, // prev and next navigation buttons
        links: false, // show images as links
        pagination: false
    });

    $('.item-box').hover(function () {
        $(this).addClass('show-box-shadow', 2000);
    });

    $('.menu  ul  li').each(function () {
        var href = $(this).find('a').attr('href');
        if (href === window.location.pathname) {
            $(this).addClass('menu-selected');
            if ($(this).parent().attr('class') == 'clearfix') {
                $('.product-path a').text($(this).find('a').first().text());
            }
            else {
                $('.product-path a').text($(this).parent().parent().find('a').first().text() + " > " + $(this).find('a').first().text());
            }

        }

    })
});
/**
 * Created by HUYQTA on 10/18/14.
 */
