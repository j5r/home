const  P = [//probabilidade acumulada
                [.5, .7, 1],
                [.3, .6, 1],
                [.1,  1, 1]
            ]
let PI0
let TTESTADOS
let X =[]
let TTSIMULACOES
let SIMULACOES

function getData(){
    try{
    pi0 = JSON.parse(sessionStorage.getItem("pi0"))
    getId("pi1").value = pi0.a
    getId("pi2").value = pi0.b
    getId("pi3").value = pi0.c
    }catch{}

    }


function begin(){
    getId("botaoIniciar").innerText = "Reiniciar"
    getId("botaoIniciar").setAttribute("onclick","location.reload()")
    PI0 = [parseFloat(getId("pi1").value),
            parseFloat(getId("pi2").value),
            parseFloat(getId("pi3").value)]

    sessionStorage.setItem("pi0",JSON.stringify({
        a: getId("pi1").value,
        b: getId("pi2").value,
        c: getId("pi3").value})
        )

    TTESTADOS = parseInt(getId("nestados").value)
    TTSIMULACOES = parseInt(getId("nsimulacoes").value)

    let bool = 1
    let soma = 0
    for(let i=0; i<3; i++){
        bool = bool * (PI0[i] >=0) *(PI0[i] <= 100)
        soma = soma + PI0[i]
        }
    if(!(soma===100)){
        alert("A distribuição de X(0) precisa somar 100%! >:(\n"+
        "A soma foi de "+soma+
        ".\n Dados entrados são inválidos.")
        }
        //erro
    else if(!bool){
            alert("As probabilidades não podem ser negativas! >:(\n Dados entrados são inválidos.")
            //erro
        }
    else if(!(TTESTADOS>0)){
            console.table({TTESTADOS})
            alert("O número de estados precisa ser\n inteiro positivo! >:(")
            //erro
        }
    else if(TTESTADOS>1000){
            console.table({TTESTADOS})
            alert("O número de estados precisa ser\n no máximo 1000! >:(")
            //erro
        }
    else if(!(TTSIMULACOES>0)){
            console.table({TTSIMULACOES})
            alert("O número de simulações precisa ser\n inteiro positivo! >:(")
            //erro
        }
    else if(TTSIMULACOES>10000000){
            console.table({TTSIMULACOES})
            alert("O número de simulações precisa ser\n no máximo 10e7! >:(")
            //erro
        }
    else{
        //ok
        for(i=0; i<3; i++)
            PI0[i] = PI0[i]/100

        PI0[1] = PI0[1]+PI0[0]
        PI0[2] = PI0[2]+PI0[1]


        for(i=0; i<TTESTADOS;i++){
            X=X.concat([[0,0,0]])
            X[i][sorteio(PI0)-1] += 1

            const div = document.createElement("div")
            div.setAttribute("id","div-"+i)
            div.setAttribute("class","dados")

            const divk = document.createElement("div")
            divk.setAttribute("id","div-"+i+"-k")
            divk.innerText = "k = "+(i+1)

            const divx1 = document.createElement("div")
            divx1.setAttribute("id","div-"+i+"-x1")

            const divx2 = document.createElement("div")
            divx2.setAttribute("id","div-"+i+"-x2")

            const divx3 = document.createElement("div")
            divx3.setAttribute("id","div-"+i+"-x3")





            div.appendChild(divk)
            div.appendChild(divx1)
            div.appendChild(divx2)
            div.appendChild(divx3)
            getId("conteudo").appendChild(div)

            }


            main()

        }
    }




function print(){
    for(i=0; i<TTESTADOS;i++){
        for(j=1; j<=3; j++){
        const xj = getId("div-"+i+"-x"+j)
            xj.innerText = X[i][j-1].toFixed(4)
        }
    }
}




function main(){

    for(w=1;w<TTSIMULACOES;w++){
    update()
    }
    for(i=0;i<TTESTADOS;i++){
        for(j=0;j<3;j++){
            X[i][j] /= TTSIMULACOES
            }
    }

    print()
}


function update(){
    theta = sorteio(PI0)
    X[0][theta-1] += 1

    for(i=1;i<TTESTADOS;i++){
        theta = transicao(theta)
            X[i][theta-1] +=1
    }
    console.table(X)
}











function getId(id){
    return document.getElementById(id)
    }

function transicao(estado){
    return sorteio(P[estado-1])
}


function sorteio(distribuicao){
    const r = Math.random() //sorteio
    for(let i=0; i < distribuicao["length"]; i++){
        if(r <= distribuicao[i]){
            return i+1//retorno
        }
    }
}
