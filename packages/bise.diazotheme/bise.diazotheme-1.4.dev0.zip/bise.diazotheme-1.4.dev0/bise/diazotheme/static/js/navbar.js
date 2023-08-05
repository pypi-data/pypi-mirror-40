$(document).ready(function() {

    var search = document.querySelector('.search');
    var submit = document.querySelector('.search-submit');
    var input = document.getElementById('search-input');

    var toggleSearch = function() {
        search.classList.toggle('open');
    }

    input.addEventListener('focus', toggleSearch);
    input.addEventListener('blur', toggleSearch);
    submit.addEventListener('focus', toggleSearch);
    submit.addEventListener('blur', toggleSearch);


    var navmenu = document.querySelector('#navmenu-items');
    var triggers = document.querySelectorAll('.navmenu-item'); //navmenu.children; 
    var menuIsOpen = false;
    var menuToOpen;
    var mobileicon = document.querySelector('.fa-angle-down');
    var mobilemenu = document.querySelectorAll('.navgroups-body');

    clickoutside = function(e) {
        e.stopPropagation();
    }

    openNavMenu = function(menu) {
        menuIsOpen = menu;
        menuToOpen = undefined;

        menu.classList.add('is-open');

        navmenu.addEventListener('click', clickoutside, false);
        document.documentElement.addEventListener('click', closeNavMenu, false);

        // console.log('openNavMenu');
    }
    closeNavMenu = function() {
        menu = menuIsOpen;
        menuIsOpen = false;

        menu.classList.remove('is-open');

        navmenu.removeEventListener('click', clickoutside, false);
        document.documentElement.removeEventListener('click', closeNavMenu, false);

        // console.log('closeNavMenu');
    }
    if (window.matchMedia("(min-width: 600px)").matches) {
        Array.prototype.forEach.call(triggers, function(trigger, index) {
            trigger.addEventListener('mouseenter', function() {
                menuToOpen = setTimeout(function() {
                    openNavMenu(trigger)
                }, 100);
            }, false);
            trigger.addEventListener('mouseleave', function() {
                if (menuToOpen)
                    clearTimeout(menuToOpen);
                else {
                    closeNavMenu();
                }
            }, false);

            trigger.addEventListener('click', function(e) {
                target = e.target;


                if (trigger.id !== 'navitem-research' && target !== mobileicon) {
                    // Naugthy exception from lazy developers. Tsst tsst!
                    if ((target.matches('.navitem-header a')) && !menuIsOpen) {
                        openNavMenu(trigger);
                        e.preventDefault();
                    }
                }
            }, false);
        });
    }

    var mobiletrigger = document.querySelector('#navitem-toggle');
    var indexcounter = undefined;


    Array.prototype.forEach.call(triggers, function(trigger, index) {
        trigger.addEventListener('click', function(e) {
            trigger = e.target;
            triggerparent = trigger.parentNode.parentNode;


            if (e.target.matches('#navitem-toggle')) {
                if (!menuIsOpen) {
                    openNavMenu(triggerparent);
                    // e.preventDefault();
                    indexcounter = index;
                } else if (menuIsOpen) {
                    closeNavMenu(triggerparent);
                    if (index !== indexcounter) {
                        openNavMenu(triggerparent);
                        indexcounter = index;
                        // e.preventDefault();
                    }

                }
            }




        }, false);
    });


    var navbrandtitle = document.querySelector('.navbrand-title');
    var navcontainer = document.querySelector(".nav-container");
    var navbrand = document.querySelector(".navbrand .navbrand-logo");
    var searchandlogin = document.querySelector('.search-and-login');
    var body = document.querySelector("body");
    var backdrop = document.querySelector('#backdrop');
    var navmenuopen = document.querySelector("#navmenu-open");
    var navmenuclose = document.querySelector("#navmenu-close");
    var navmenubody = document.querySelector(".navmenu-body");
    var asidetrigger = document.querySelector('.asidetrigger');
    var aside = document.querySelector("aside");
    var section = document.querySelector(".section");
    var asideclass = document.querySelector(".aside")
    var asidebutton = document.querySelector("#aside-button");
    var homepage_navtrigger = document.querySelector('.page-homepage .navmenu-trigger');
    var homepage_navbrand = document.querySelector('.page-homepage .navbrand');

    //opening and closing of mobile menu

    navmenuopen.addEventListener('click', function() {
        navmenubody.classList.add('open');
        navmenuopen.classList.add('hidden');
        navmenuclose.classList.remove('hidden');
        searchandlogin.classList.add('open');
        navbrand.classList.add('hidden');
        navbrandtitle.classList.add('open');
        homepage_navtrigger.classList.add('relative');
        homepage_navbrand.classList.add('relative');
        body.classList.add('no-ovf');
    });



    navmenuclose.addEventListener('click', function() {
        navmenubody.classList.remove('open');
        navmenuclose.classList.add('hidden');
        navmenuopen.classList.remove('hidden');
        searchandlogin.classList.remove('open');
        navbrand.classList.remove('hidden');
        navbrandtitle.classList.remove('open');
        homepage_navtrigger.classList.remove('relative');
        homepage_navbrand.classList.remove('relative');
        body.classList.remove('no-ovf');
    });

    // Set window.location.origin for IE
    if (!window.location.origin) {
      window.location.origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
    }

    // set the navbrand link to bise homepage
    $('.navbrand')[0].href = window.location.origin

    //call for sidebar plugin
    sidebarplugin(asidetrigger, aside, asidebutton);

    // hide sidebar trigger if there is no sidebar
    if (!aside && asidetrigger) {
        asidetrigger.style.display = 'none';
    }

$('.mtrTargetDiv').append('<div class="close-dialog btn btn-default">Close</div>');
$('.target-nav a').click(function(){
    $(this).addClass('no-events')
});




var $loading = $('#ajax-spinner').hide();
$(document)
  .ajaxStart(function () {
    $('#ajax-spinner').css('display','block');
  })
  .ajaxStop(function () {
 $('#ajax-spinner').css('display','none');
  });

    // Create search params
    function getURLParameter(name) {
        return decodeURI(
            (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) || [, ''])[1]
        );
    }
    var q = getURLParameter("q");
    q = q.replace("+", " ");
    if (q != '') { $("#catalogue-app").attr("data-query", q); }


    if ($('.modal-container').length > 0) {

        loadmodaldata()
        $('.close-dialog, #backdrop').click(function() {
            modalclose();
        })
    }

});


var modal_link = 0;

$modal = $('.modal-container');



function modalopen() {
    $('.modal-container').addClass('open');
    $('body').addClass('sidebaropen');

}


function modalclose() {
    $('.modal-container').removeClass('open');
    $('body').removeClass('sidebaropen');
    $('.targetDiv').removeClass('element-nav');
    $('.mtractive').removeClass('mtractive');
history.replaceState({}, document.title, ".");

}

function loadmodaldata() {
    $mtrmenu = 0;
    var linkindex;
    $click_item = $('.targetDiv.mtrTargetDiv a');
if (window.matchMedia("(min-width: 600px)").matches) {
    $click_item.click(function(event) {

        event.preventDefault();


        var link = $(this).attr("href");
        if (!$(this).parent().hasClass('target-nav')) {
            $mtrmenu = $(this).parent();
        } else if ($(this).parent().hasClass('target-nav')) {
            //target 1
            if ($(this).parent().parent().hasClass('target1Bg') && $(this).hasClass('next')) {
                $mtrmenu = $('.target2Bg');
            }
            //target 2
            if ($(this).parent().parent().hasClass('target2Bg') && $(this).hasClass('next')) {
                $mtrmenu = $('.t3a');
            }
            if ($(this).parent().parent().hasClass('target2Bg') && $(this).hasClass('previous')) {
                $mtrmenu = $('.target1Bg');
            }
            //target 3a
            if ($(this).parent().parent().hasClass('t3a') && $(this).hasClass('next')) {
                $mtrmenu = $('.t3b');
            }
            if ($(this).parent().parent().hasClass('t3a') && $(this).hasClass('previous')) {
                $mtrmenu = $('.target2Bg');
            }
            //target 3b
            if ($(this).parent().parent().hasClass('t3b') && $(this).hasClass('next')) {
                $mtrmenu = $('.target4Bg');
            }
            if ($(this).parent().parent().hasClass('t3b') && $(this).hasClass('previous')) {
                $mtrmenu = $('.t3a');
            }
            //targer 4
            if ($(this).parent().parent().hasClass('target4Bg') && $(this).hasClass('next')) {
                $mtrmenu = $('.target5Bg');
            }
            if ($(this).parent().parent().hasClass('target4Bg') && $(this).hasClass('previous')) {
                $mtrmenu = $('.target3Bg');
            }
            //target 5 
            if ($(this).parent().parent().hasClass('target5Bg') && $(this).hasClass('next')) {
                $mtrmenu = $('.target6Bg');
            }
            if ($(this).parent().parent().hasClass('target5Bg') && $(this).hasClass('previous')) {
                $mtrmenu = $('.target4Bg');
            }
            //target 6 
            if ($(this).parent().parent().hasClass('target6Bg') && $(this).hasClass('previous')) {
                $mtrmenu = $('.target5Bg');
            }
        }
        if (linkindex == link) {
            modalopen();
            $mtrmenu.addClass('element-nav');
        } else {
            $('.modal-content').empty();
            var request = $.ajax({
                url: link,
                type: "GET",
                data: { id: link },
                dataType: "html",
                success: function(data) {
                    var $response = $(data);
                    var data1 = $response.find('#content-core').html();
                    $('.modal-content').append(data1);
                    modalopen();
                    $('.targetDiv').removeClass('element-nav');
                    $mtrmenu.addClass('element-nav');
                    $mtrmenu = 0;
                    linkindex = link;
                    modal_link = link.substring(57);;
                        $('.target-nav a').removeClass('no-events')
                            $('.mtractive').removeClass('mtractive');
                    // var active_link = document.querySelectorAll("a[href=" + link + "]");
                    var active_link = $('a[href="'+link+'"] > div');
                    active_link.addClass('mtractive');
                    // window.location.hash = link;

                    // link_id = window.location.replace(('' + window.location).split('#')[0] + '#' + modal_link);
                    // window.location.hash = '#!' + link_id;
                    window.history.replaceState( {} , window.location, link );
                },
                failure: function(data) {
                    alert('Got an error dude');
                }
            });
        }
    });
    }
};
