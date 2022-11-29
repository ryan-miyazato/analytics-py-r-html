var dict = {
    "nome" : 'cpu_percent',
    "componente": 'cpu_intel'
};

var jsonDict = JSON.stringify(dict);

var fs = require('fs');
fs.writeFile("parametros.json", jsonDict, function(err, result){
    if(err) console.log("error", err);
});

// execute