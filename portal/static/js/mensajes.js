// jquery code

//===== Función para que desaparezcan los mensajes a los 4segundos o 4000
setTimeout(function(){
    $('#message').fadeOut('slow')
    }, 4000)

    $(document).ready(function() {

        $('.counter').each(function () {
            $(this).prop('Counter',0).animate({
                Counter: $(this).text()
        }, {
        duration: 4000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
        });
        });

    });  