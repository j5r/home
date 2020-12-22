
/* *********************** TITULO ****************************** */
function cabecalho(){
    /* CABEÇALHO */
    /* criar cabeçalho */

    /* li nome */
    var _a_nome = document.createElement("a")
    _a_nome.setAttribute("id","nome")
    _a_nome.setAttribute("href","https://tiny.cc/j5rw")
    _a_nome.innerText = "Junior Rodrigues Ribeiro"

    var _li_nome = document.createElement("li")
    _li_nome.setAttribute("name","nome")
    _li_nome.appendChild(_a_nome)


    /* li formacao1 */
    var _li_formacao1 = document.createElement("li")
    _li_formacao1.innerText = "Licenciado em Matemática - UEMS 2015"
    _li_formacao1.setAttribute("name","formacao")

    /* li formacao2 */
    var _li_formacao2 = document.createElement("li")
    _li_formacao2.innerText ="Mestre em Ciências: Matemática Computacional - ICMC/USP 2019"
    _li_formacao2.setAttribute("name","formacao")

    /* li formacao3 */
    var _li_formacao3 = document.createElement("li")
    _li_formacao3.innerText = "Doutorando em Ciências: Matemática Computacional - ICMC/USP 2019 - atual"
    _li_formacao3.setAttribute("name","formacao")

    /* anexando lis à ul */
    var _ul = document.createElement("ul")
    _ul.appendChild(_li_nome)
    _ul.appendChild(_li_formacao1)
    _ul.appendChild(_li_formacao2)
    _ul.appendChild(_li_formacao3)


    /* criando div-avatar */
    var _img = document.createElement("img")
    _img.setAttribute("id","avatar")
    _img.setAttribute("src","./public/eu.svg")

    var _div_avatar = document.createElement("div")
    _div_avatar.setAttribute("name","avatar")
    _div_avatar.appendChild(_img)


    /* anexando ul, div_avatar à div-titulo */
    var _cabecalho = document.createElement("div")
    _cabecalho.setAttribute("name","titulo")
    _cabecalho.appendChild(_ul)
    _cabecalho.appendChild(_div_avatar)

    /* anexando div-titulo à DOM*/
    var div_corpo = document.getElementById("corpo")
    div_corpo.insertAdjacentElement("beforebegin",_cabecalho)

    var _head = document.getElementsByTagName("head")[0]
    var _title = document.createElement("title")
    _title.innerText = "j5r"


    var _favicon = document.createElement("link")
    _favicon.setAttribute("rel","icon")
    _favicon.setAttribute("type","image/svg")
    _favicon.setAttribute("href","./favicon.svg")

    _head.appendChild(_title)
    _head.appendChild(_favicon)



}

/* ******************** MENU ************************************* */
function menu(){
    var menu = document.createElement("div")
    menu.setAttribute("id","menu")

    var div_corpo = document.getElementById("corpo")
    div_corpo.insertAdjacentElement("afterbegin",menu)

    var ul = document.createElement("ul")
    menu.appendChild(ul)

    addMenu("menu_links","HOME","#","")
    changeAttr("menu_links_a","style","color:#fff;text-decoration:none")

    addMenu("menu_producoes","Produções","./producoes/producoes.html")

    addMenu("menu_arquivos","Arquivos","./arquivos/index.html")

    addMenu("menu_listaafazeres","Lista de afazeres","https://j5r.github.io/afazeres")
    }




function changeAttr(id,attr,value){
    var item = document.getElementById(id)
    item.setAttribute(attr,value)
    }

function changeText(id,text){
    var item = document.getElementById(id)
    item.innerText = text
    }

function addMenu(id,texto,url="#", name="name"){
    var a_id = id + "_a"
    var a = document.createElement("a")
    a.setAttribute("href",url)
    a.setAttribute("id",a_id)
    a.innerText = texto


    var item = document.createElement("li")
    item.setAttribute("id",id)
    if(name){
    item.setAttribute("name",name)
    }
    item.appendChild(a)

    // appending
    var menu = document.getElementById("menu")
    var ul = menu.getElementsByTagName("ul")[0]
    ul.appendChild(item)
    }




function useLatex(){
    var _script1 = document.createElement("script")
    _script1.setAttribute("type","text/x-mathjax-config")
    var _t_script1 = document.createTextNode("MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$']]}});")
    _script1.appendChild(_t_script1)

    var _script2 = document.createElement("script")
    _script2.setAttribute("type","text/javascript")
    _script2.setAttribute("src","https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML")

    var _head = document.getElementsByTagName("head")[0]
    _head.appendChild(_script1)
    _head.appendChild(_script2)
    }


function j5rcopy(idd){
        var copyText = document.getElementById(idd).innerText;
        var ta = document.createElement("textarea");

        ta.value = copyText;
        document.getElementById(idd).appendChild(ta);
        ta.select()

        /* Copy the text inside the text field */
        var sim = document.execCommand('copy');
        ta.remove();

        /* Alert the copied text */
        alert("O conteúdo foi copiado!\n\n" + ta.value);
        }







window.onscroll = function(){
        var botao = document.getElementById("botao-topo")
        if(document.getElementsByTagName("body")[0].scrollTop > 250){
            botao.style.display = "block"
        }
        else{
            botao.style.display = "none"
        }
    }


function rolarParaTopo(){
    var h = document.getElementsByTagName("body")[0]
    h.scroll(0,-h.scrollTop)
    }





