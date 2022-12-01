
// Importando dependências do node
const fs = require('fs');
const path = require('path');
const { mainModule } = require('process');
const spawn = require("child_process").spawn;
const exec = require("child_process").exec;

// Encontrando caminho do interpretador python
const pyVersao = 310;
var pythonPath;

var dict = {
    "nome" : "cpuPercent",
    "componente": 106
};

function iniciar(nome, componente){
    acharPython();
    setTimeout(()=>{
        ativarPython(nome, componente);
    }, 1000);
}

function acharPython(){
    exec('python -c "import os, sys; print(os.path.dirname(sys.executable))"', function(error, stdout, stderr){
        console.log('stdout: ' + stdout);
        console.log('stderr: ' + stderr);
        if (error != null) {
            console.log('exec error: ' + error);
        } else {
            pythonPath = stdout.replace(/(\r\n|\n|\r)/gm,"") + "\\python.exe";
            console.log("pythonPath:", pythonPath);
        }
    });

    
}



// Executando python com parâmetros

function ativarPython(){

    console.log("ATIVANDO O PYTHON");
    
    mudarVersaoPython(pyVersao);
    setTimeout(()=>{
        spawn(pythonPath, ["public/main.py", dict.nome, dict.componente]);
        apagarImagens();
    }, 1000);
}

function mudarVersaoPython(versao){
    var novaVersao = "Python" + versao

    console.log(novaVersao)

    if(pythonPath.indexOf(novaVersao) < 0){
        var separador;

        if(pythonPath.indexOf("/") >= 0){
            separador = "/";
        }else{
            separador = "\\";
        }
        
        pythonPath = pythonPath.split(separador);
        pythonPath[pythonPath.length - 2] = novaVersao;
        pythonPath = pythonPath.join(separador);

        console.log(pythonPath);
    }
}


// Apagando imagens desnecessárias 

function apagarImagens(){

const diretorioGraficos = "./public/graficos"

fs.readdir(diretorioGraficos, function (err, files) {
    if (err) {
        return console.log('Não foi possível escanear o diretório: ' + err);
    } 
    files.forEach(function (file) {
            console.log(file); 
            fs.unlink(diretorioGraficos + "/" + file, function(err){
                if(err != null){
                    console.log("Não foi possível excluir o arquivo:", file)
                }else{
                    console.log("Arquivo excluido com sucesso:", file)
                }
            });
        
        });
    });
}










