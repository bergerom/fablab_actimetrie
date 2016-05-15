/**
 * Created by matthieu on 19/03/16.
 * Sends a message to the server
 */

var port = 4730;
var url =  'http://localhost' + port;
var socket = io.connect(url);

socket.on('message',function(data){
    console.log(data);
    socket.emit('',{message: 'data'})
});


