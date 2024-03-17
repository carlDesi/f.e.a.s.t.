$(document).ready(function() {
    $('#add_room').click(function(e) {
        e.preventDefault();
        var roomName = $('.room_name').val();
        if (roomName) {
            $.ajax({
                url: '/teacher_main/create-room/',
                method: 'POST',
                data: {
                    name: roomName,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(data) {
                    // create a new div and button element for the new room
                    var newRoom = $('<div>').addClass('container').appendTo('.center-panel');
                    var newButton = $('<button>').text(roomName).addClass('btn').appendTo(newRoom);

                    // clear the room_name input
                    $('.room_name').val('');
                }
            });
        }
    });
});