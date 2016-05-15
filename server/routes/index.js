// Page principale
exports.index = function(app){
    app.get('/',function(req,res){
        console.log("GET home page");
        res.type('text/html');
        res.render('index.jade');
    });
};
