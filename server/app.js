var express = require('express');
var app = express();
var http = require('http').Server(app);

// Pour gérer les requêtes et réponses JSON
var bodyparser = require('body-parser');
var routes = require('./routes/event.js');
app.use(bodyparser.json());
app.use(bodyparser.urlencoded({ extended: false}));

// Fichiers statiques situés dans /public/*
app.use(express.static('public'));

/* SOCKET.IO */
const io = require('socket.io')(http);
io.on('connection',function(socket){
    console.log('a user connected');
    socket.on('disconnect',function(){
        console.log('user disconnected');
    });
     socket.on('looking at', function(msg){
     console.log(msg);
     })
});

/* ROUTES */
listPersons = [];
app.post('/allocateId',function(req,res){
    if(!req.body.hasOwnProperty('name')){
        req.statusCode = 400;
        return res.send("Error 400: Post syntax incorrect.");
    }
    var name = req.body.name;
    console.log("Ajout d'une personne Nom : {" + name + "}");
    listPersons.push(name);
    io.emit('new member',name);

    res.type('text/plain');
    res.send(name + " a bien été ajouté.");
});

app.get('/allocateId',function(req,res){
    res.type('text/html');
    res.render('allocateId.jade');
});

// main root
app.get('/',function(req,res){
    res.type('text/html');
    res.render('index.jade');
});

app.post('/event',function(req,res){
    console.log("POST !");
    console.log(req.body);
    if(!req.body.hasOwnProperty('ownId') || !req.body.hasOwnProperty('otherId')){
        req.statusCode = 400;
        return res.send("Error 400: Post syntax incorrect.");
    }
    var ownId = req.body.ownId;
    var otherId = req.body.otherId;
    io.emit('looking at', ownId + " regarde " +  otherId);
    res.type('text/plain');
    res.send(ownId + " regarde " +  otherId);
});

app.get('/event',function(req,res){
    res.type('text/html');
    res.render('eventSubmit.jade');
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});