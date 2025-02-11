$(document).ready(function() {
   
    $('.carousel').carousel({
        interval: 3000,  
        pause: "hover"   
    });

    $('a.color_animation').click(function(e) {
        e.preventDefault();
        var target = $($(this).attr('href'));
        
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });


    $('#filter-list li').click(function() {
        const value = $(this).attr('data-filter');
        
       
        $('#filter-list li').removeClass('active');
        $(this).addClass('active');
        
        if (value === 'all') {
            
            $('#portfolio li').each(function(index) {
                $(this).fadeOut(400).delay(200 * index).fadeIn(400);
            });
        } else {
            
            $('#portfolio li').fadeOut(400);
            
         
            setTimeout(function() {
                $('#portfolio li').each(function() {
                    if ($(this).hasClass(value)) {
                        $(this).fadeIn(400);
                    }
                });
            }, 400);
        }
    });

    
    $('#portfolio li').hover(
        function() {
            $(this).find('img').css({
                'transform': 'scale(1.1)',
                'transition': 'transform 0.3s ease'
            });
            $(this).find('.white').css({
                'background': 'rgba(46, 204, 113, 0.9)',
                'transition': 'background 0.3s ease'
            });
        },
        function() {
            $(this).find('img').css({
                'transform': 'scale(1.0)',
                'transition': 'transform 0.3s ease'
            });
            $(this).find('.white').css({
                'background': 'rgba(0, 0, 0, 0.7)',
                'transition': 'background 0.3s ease'
            });
        }
    );

  
    $('#portfolio li').each(function(index) {
        $(this).hide().delay(200 * index).fadeIn(400);
    });
});