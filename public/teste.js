
    var dict = {
    "nome" : 'cpuPercent',
    "componente": '69'
    };

    var jsonDict = JSON.stringify(dict);

    const fs = require('fs');
    fs.writeFile("./public/parametros.json", jsonDict, function(err, result){
        if(err) console.log("error", err);
    });

    const spawn = require("child_process").spawn;
    var pyProcess = spawn('python', ["main.py", dict.nome, dict.componente]);

    

    
// execute