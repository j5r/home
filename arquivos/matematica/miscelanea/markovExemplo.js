let STATE
let OLDSTATE
let OLDOLDSTATE
let TIME
let ID
const  P = [//probabilidade acumulada
                [.5, .7, 1],
                [.3, .6, 1],
                [.1,  1, 1]
            ]




function begin(){
    const input = document.getElementById("primeiroEstado")
    const button = document.getElementById("btnprimeiroEstado")

    STATE = parseInt(input.value)
    if([1,2,3].includes(STATE)){

        //document.getElementById("estado"+STATE).setAttribute("name","selected")

        post("transicao",
            get("transicao")
            + " >> "
            + STATE)

        start()
        button.innerText = "Parar animação"
        button.setAttribute("onclick","stop()")
        input.remove()
        auxTIME = new Date()
        TIME = new Date(auxTIME.getTime()+1000*60*5)
        //repeticao
    }else{
        alert("Valor não permitido >:(\nEscolha um entre 1,2,3.")
        }
}













function stop(){
    clearInterval(ID)
    const button = document.getElementById("btnprimeiroEstado")
    button.innerText = "Reiniciar animação"
    button.setAttribute("onclick","location.reload()")
    post("transicao",
            get("transicao")
            + " > FIM. ")
}









function start(){ // start
    ID = setInterval(()=>{
        OLDOLDSTATE = OLDSTATE
        OLDSTATE = STATE
        obj = transicao(STATE)
        STATE = obj.state
        random = obj.random
        //document.getElementById("oldestado").innerText = OLDSTATE
        document.getElementById("oldestado").innerText = OLDSTATE //O estado atual é
        document.getElementById("estado").innerText = STATE //Portanto o próximo estado será
        document.getElementById("random").innerText = random.toPrecision(5)

        document.getElementById("m1"+OLDOLDSTATE).setAttribute("class","")//matriz original
        document.getElementById("m1"+OLDSTATE).setAttribute("class","selected")//matriz original
        document.getElementById("m2"+OLDOLDSTATE).setAttribute("class","")//matriz acumulada
        document.getElementById("m2"+OLDSTATE).setAttribute("class","selected")//matriz acumulada


        document.getElementById("m1"+OLDOLDSTATE+OLDSTATE).setAttribute("class","")//matriz original
        document.getElementById("m1"+OLDSTATE+STATE).setAttribute("class","selectedin")//matriz original
        document.getElementById("m2"+OLDOLDSTATE+OLDSTATE).setAttribute("class","")//matriz acumulada
        document.getElementById("m2"+OLDSTATE+STATE).setAttribute("class","selectedin")//matriz acumulada




        post("transicao",
            get("transicao")
            + " > "
            + STATE)


        //bullets
        if(OLDOLDSTATE+1){
            document.getElementById("estado"+OLDOLDSTATE).setAttribute("name","")
            document.getElementById("estado"+OLDSTATE).setAttribute("name","selected")
        }

        if(new Date() > TIME){
            stop()
            alert("Tempo de 5 minutos expirado!")
            }
        },1500)

}




function post(id,valor){
    const tag = document.getElementById(id)
    tag.innerText = "" + valor
}

function get(id){
    return document.getElementById(id).innerText
}



function transicao(oldestado){
    const r = Math.random() //sorteio
    for(let i=0; i < P["length"]; i++){
        if(r <= P[oldestado-1][i]){
            return {state:i+1,random:r}//retorno
            }
    }
}



