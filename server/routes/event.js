// Fonction appellée par les ESP8266 lorsqu'ils savent qu'ils sont regardés.

// Exemple de requête : jean est regardé par pierre
// On effectue la requete suivante :
// POST : ownId=jean&otherId=pierre
exports.event = function(io) {
    return function(req,res){
        if(!req.body.hasOwnProperty('ownId') || !req.body.hasOwnProperty('otherIds')){
            req.statusCode = 400;
            return res.send("Error 400: Post syntax incorrect.");
        }
        var ownId = req.body.ownId;
        var otherIds = req.body.otherIds;
        res.type('text/plain');
        io.socket.emit('looking at',ownId + "est regardé par" +  otherIds);
        res.send(ownId + " est regardé par " +  otherIds);
    };
};

