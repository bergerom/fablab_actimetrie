// Fonction a appeller pour ajouter une nouvelle personne (= un ESP8266)
// L'identifiant de la personne est donné en paramêtre
exports.allocate = function(app) {
    var nbPersons = 0;
    // Permet de donner un identifiant à une personne (= ESP8266)
    app.get('/allocateId', function (req, res) {
        console.log("GET /allocateId");
        res.render(++nbPersons);
        return nbPersons;
    });
};
